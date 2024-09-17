from helpers import get_uids, get_applicant_hhid, CONFIRMATIONS_COLLECTION

"""
Associates a uid with a link to check-in
"""

def generate_checkin_links():
    """
    Generate check-in-links for all application ids
    """
    uids = get_uids(CONFIRMATIONS_COLLECTION)
    checkin_links = {}
    for uid in uids:
        hhid = get_applicant_hhid(uid)
        checkin_links[uid] = (
            f"https://admin.hackharvard.io/user/{hhid}"
        )

    return checkin_links

if __name__ == "__main__":
    checkin_links = generate_checkin_links()
    print(checkin_links)
