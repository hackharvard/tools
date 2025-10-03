import os, sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from helpers import get_uid_by_hhid, set_confirmation
import argparse
import webbrowser

def main():
    parser = argparse.ArgumentParser(description="Confirm a walk-in applicant")
    parser.add_argument("hhid", type=str, help="Household ID of the applicant")

    args = parser.parse_args()

    if not args.hhid:
        raise ValueError("HHID is required")

    if not args.hhid.startswith("HH-"):
        hhid = "HH-" + args.hhid

    uid = get_uid_by_hhid(hhid)

    if not uid:
        raise ValueError(f"No applicant found with HHID: {hhid}")

    print(f"Confirming applicant with HHID: {hhid}, UID: {uid}")
    print(f"Opening confirmation HTML page...")

    # literally just open the html page which is 
    webbrowser.open("index.html")

    input("Press Enter to confirm everything...")

    set_confirmation(uid)

if __name__ == "__main__":
    main()