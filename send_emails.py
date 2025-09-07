import os
import argparse
import sys

# add project root to path (one level up from this file)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

from helpers import get_accepted_applications, get_confirmed_applications, get_applications
import emails

def get_recipients(args) -> list:
    recipients = []
    if args.to:
        recipients.append((args.to, "there"))
    elif args.to_list:
        recipients.extend(((email, "there") for email in args.to_list))
    elif args.to_collection:
        if args.to_collection == "accepted":
            application_func = get_accepted_applications
        elif args.to_collection == "confirmed":
            application_func = get_confirmed_applications
        else:  # all
            if input("Are you sure you want to send to all applicants? (y/n) ").lower() != "y":
                print("Aborting.")
                sys.exit(0)
            application_func = get_applications

        for _, application_data in application_func().items():
            personal   = application_data.get("personal", {})
            email      = personal.get("email")
            first_name = personal.get("firstName")
            recipients.append((email, first_name))

    return recipients

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate email corrections for accepted applicants")

    grp = parser.add_mutually_exclusive_group(required=True)

    grp.add_argument(
        "--to",
        metavar="EMAIL",
        help="Send a single email to the specified address."
    )

    grp.add_argument(
        "--to-list",
        metavar="EMAIL",
        nargs="+",
        help="Send emails to a list of specified addresses, separated by spaces."
    )

    grp.add_argument(
        "--to-collection",
        choices=["accepted", "confirmed", "all"],
        help="Send to a specific cohort of applicants from the collection defined in helpers.py."
    )

    parser.add_argument(
        "-i", "--input",
        dest="input",
        metavar="JSON",
        required=True,
        help="Path to a JSON file containing the arguments to pass to the email template's build method."
    )
    parser.add_argument(
        "--template",
        choices=["general", "action"],
        required=True,
        help="The email template to use."
    )

    parser.add_argument(
        "--first-name",
        action="store_true",
        help="Personalize the email by including the recipient's first name "
        "(if available). Any instances of {{first_name}} in the description " \
        "field of the build args JSON will be replaced with the first name " \
        "of the recipient, or 'there' (e.g. 'Hello, there')."
    )
    parser.add_argument(
        "--silent",
        action="store_true",
        help="Suppress console output except for errors."
    )
    parser.add_argument(
        "--ignore-exceptions",
        action="store_true",
        help="Continue sending emails even if an error occurs."
    )
    
    args = parser.parse_args()

    recipients = get_recipients(args)
    email_template = emails.templates.get_template(args.template)
    build_args_template = emails.sender.read_json(args.input)

    subject = build_args_template.pop("subject", "No Subject")
    from_email = build_args_template.pop("from_email", "team@hackharvard.io")

    desc_template = build_args_template.get("description", "")

    for to_email, first_name in recipients:
        desc = desc_template
        if args.first_name:
            desc = desc.replace("{{first_name}}", first_name or "there")

        # per-recipient copy
        build_args = {**build_args_template, "description": desc}

        emails.sender.send_email(
            email_template=email_template,
            build_args=build_args,
            from_email=from_email,
            to_email=to_email,
            subject=subject,
            silent=args.silent,
            ignore_exceptions=args.ignore_exceptions
        )
        
    if not args.silent:
        print(f"Done! Sent {len(recipients)} emails.")



