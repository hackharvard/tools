from helpers import get_accepted_applications, export_to_json

"""
Associates a uid with a link to check-in
"""

DEFAULT_FILE_PATH = "json/checkin_links.json"

def generate_checkin_links():
    """
    Generate check-in-links for all accepted applicants
    """
    applications = get_accepted_applications()
    checkin_links = {}
    for uid, application_data in applications.items():
        personal = application_data["personal"]
        hhid = application_data["meta"]["hhid"]
        checkin_links[uid] = {
            "name": f"{personal["firstName"]} {personal["lastName"]}",
            "hhid": hhid,
            "email": personal["email"],
            "url": f"https://admin.hackharvard.io/user/{hhid}"
        }
            
    return checkin_links

def export_checkin_links(file_path=DEFAULT_FILE_PATH):
    checkin_links = generate_checkin_links()
    export_to_json(checkin_links, file_path)

if __name__ == "__main__":
    export_checkin_links()
    