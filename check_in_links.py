from helpers import get_application_ids, get_applicant_hhid, CONFIRMATIONS_COLLECTION

"""
Associates an application id with a link to check-in
"""

def generate_checkin_links():
    """
    Generate check-in-links for all application ids
    """
    application_ids = get_application_ids(CONFIRMATIONS_COLLECTION)
    checkin_links = {}
    for application_id in application_ids:
        hhid = get_applicant_hhid(application_id)
        checkin_links[application_id] = (
            f"https://admin.hackharvard.io/user/{hhid}"
        )

    return checkin_links

if __name__ == "__main__":
    checkin_links = generate_checkin_links()
    print(checkin_links)
