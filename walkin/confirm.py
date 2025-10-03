import os, sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from helpers import get_uid_by_hhid, set_confirmation
import argparse
import webbrowser

import http.server
import socketserver
import threading
import webbrowser

def serve_and_open():
    port = 8000
    handler = http.server.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer(("", port), handler)

    # Serve in a background thread so it doesn’t block your script
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()

    # Open index.html in browser via localhost
    url = f"http://localhost:{port}/index.html"
    print()
    print("Go to the following URL to confirm the applicant. Once they check all boxes, come back.")
    print(url)
    print()
    return httpd

def main():
    parser = argparse.ArgumentParser(description="Confirm a walk-in applicant")
    parser.add_argument("hhid", type=str, help="Household ID of the applicant")

    args = parser.parse_args()

    if not args.hhid:
        raise ValueError("HHID is required")

    hhid = args.hhid
    if not hhid.startswith("HH-"):
        hhid = "HH-" + hhid

    uid = get_uid_by_hhid(hhid)

    if not uid:
        raise ValueError(f"No applicant found with HHID: {hhid}")

    print(f"Confirming applicant with HHID: {hhid}, UID: {uid}")
    print(f"Opening confirmation HTML page...")

    # literally just open the html page which is 
    server = serve_and_open()

    input("Press Enter to confirm everything...")

    set_confirmation(uid)

    print(f"Applicant with HHID: {hhid} has been confirmed.")
    server.shutdown()

if __name__ == "__main__":
    main()