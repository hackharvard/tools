import os
import json
import sys

from dotenv import load_dotenv
from postmarker.core import PostmarkClient

from .email_templates import EmailTemplate

# add project root to path (one level up from this file)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
load_dotenv()
POSTMARK_API_TOKEN = os.getenv("POSTMARK_API_TOKEN")
if not POSTMARK_API_TOKEN:
    raise SystemExit("POSTMARK_API_TOKEN is not set. Add it to your environment or .env file.")

postmark = PostmarkClient(server_token=POSTMARK_API_TOKEN)

def send_email(
    email_template: EmailTemplate,
    build_args: dict,
    from_email: str,
    to_email: str,
    subject: str,
    silent: bool = False,
    ignore_exceptions: bool = False
):
    try:
        postmark.emails.send(
            From=from_email,
            To=to_email,
            Subject=subject,
            HtmlBody=email_template.build(**build_args),
        )
        if not silent:
            print(f"Sent to {to_email}!")
    except Exception as e:
        if not ignore_exceptions:
            raise e
        if not silent:
            print(f"Failed to send to {to_email}: {e}")

def read_json(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

