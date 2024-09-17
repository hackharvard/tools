from helpers import get_uids, get_applicant_hhid, get_accepted_applications

"""
Associates a uid with a link to check-in
"""

def generate_checkin_links():
    """
    Generate check-in-links for all accepted applicants
    """
    applications = get_accepted_applications()
    checkin_links = {}
    for application_id, application_data in applications.items():
        first_name = application_data["personal"]["firstName"]
        last_name = application_data["personal"]["lastName"]
        uid = application_id
        hhid = application_data["meta"]["hhid"]
        email = application_data["personal"]["email"]
        checkin_links[uid] = {
            "name": f"{first_name} {last_name}",
            "hhid": hhid,
            "email": email,
            "url": f"https://admin.hackharvard.io/user/{hhid}"
        }
            
    return checkin_links

if __name__ == "__main__":
    checkin_links = generate_checkin_links()
    print(checkin_links)
