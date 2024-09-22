from helpers import get_accepted_applications, get_confirmed_participants
import csv

"""
Associates a uid with a firebase storage link to resume
"""

def generate_resume_links():
    """
    Generate resume links for all accepted applicants
    """
    confirmations = get_confirmed_participants()
    resume_links = {}
    for application_id, application_data in confirmations.items():
        first_name = application_data["personal"]["firstName"]
        last_name = application_data["personal"]["lastName"]
        size = application_data["hackathon"]["shirtSize"]

        resume_links[application_id] = {
            "name": f"{first_name} {last_name}",
            "size": size,
        }

    return resume_links

def export_to_csv():
    resume_links = generate_resume_links()
    with open("tshirts.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(["Name", "Shirt Size"])
        for _, application_data in resume_links.items():
            writer.writerow([
                application_data["name"],
                application_data["size"],
            ])

if __name__ == "__main__":
    export_to_csv()