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
        recipients.append((args.to, {"first_name": "there"}))
    elif args.to_list:
        recipients.extend(((email, {"first_name": "there"}) for email in args.to_list))
    elif args.to_collection:
        if args.to_collection == "accepted":
            application_func = get_accepted_applications
        elif args.to_collection == "confirmed":
            application_func = get_confirmed_applications
        elif args.to_csv:
            recipients = emails.sender.read_csv(args.to_csv)
        else:  # all
            if input("Are you sure you want to send to all applicants? (y/n) ").lower() != "y":
                print("Aborting.")
                sys.exit(0)
            application_func = get_applications

        for _, application_data in application_func().items():
            personal   = application_data.get("personal", {})
            email      = personal.get("email")
            first_name = personal.get("firstName")
            recipients.append((email, {"first_name": first_name or "there"}))

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
    grp.add_argument(
        "--to-csv", "--link-csv",
        metavar="CSV",
        help="""
        Loads recipient emails from a CSV file.
        Sends emails to all addresses in the `email`, `emails`, or `e-mails` column,
        whichever is first. If none of those columns exist, the program exits.
        Using {{col_name}} in the description field will look for a column named
        `col_name` and replace it with the corresponding value for each recipient.
        """
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

    recipients     = get_recipients(args)
    email_template = emails.templates.get_template(args.template)
    build_args     = emails.sender.read_json(args.input)

    DEFAULT_CONTEXT = {"first_name": "there"}
    for to_email, recipient in recipients:
        context = DEFAULT_CONTEXT.copy()

        # Merge context from the recipient with some base default context
        context.update(recipient or {})

        # Render the build args using Jinja2 templating
        rendered   = emails.renderer.render_fields(build_args, context)
        subject    = rendered.pop("subject", "No Subject")
        from_email = rendered.pop("from_email", "team@hackharvard.io")

        emails.sender.send_email(
            email_template=email_template,
            build_args=rendered,
            from_email=from_email,
            to_email=to_email,
            subject=subject,
            silent=args.silent,
            ignore_exceptions=args.ignore_exceptions
        )
        
    if not args.silent:
        print(f"Done! Sent {len(recipients)} emails.")



