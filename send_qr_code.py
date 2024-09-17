from postmarker.core import PostmarkClient
import qrcode;
import json;
import os;
import base64;

from check_in_links import generate_checkin_links;

POSTMARK_API_TOKEN = os.getenv("POSTMARK_API_TOKEN")

postmark = PostmarkClient(server_token=POSTMARK_API_TOKEN)

def send_postmark(name:str, email:str, qr_bytes):
    email_content = f"""

<html>
<body><p>
Hi {name}, 
here’s your check in link for checking to the Hackathon!
</p>
<image src="cid:qr_code"/>
</body></html>

"""
    postmark.emails.send(
        From ='',
        To = email,
        Subject ='Hackathon Check-in QR Code',
        HtmlBody =email_content,
        Attachments = [
            {
            "Name": "qr_code.png",
            "Content": qr_bytes,
            "ContentType": "image/png",
            "ContentID": "cid:qr_code"
            }
        ]
    )
    
# msg = EmailMessage()

if __name__ == "__main__":
    checkin_links = generate_checkin_links()
    # with open('./check_in_links.json', 'r') as f:
    #     checkin_links = json.loads(f.read())

    """
    JSON FORMAT:
    uuid |-> <name, hhid, email, url>
    """
    for v in checkin_links.values():
        img = qrcode.make(v['url'])
        type(img)  # qrcode.image.pil.PilImage
        img.save(f"qrcode.png")
        with open(f"qrcode.png", "rb") as f:
            encoded = base64.b64encode(f.read())
            send_postmark(v['name'], v['email'], encoded)

