from helpers import get_accepted_applications
import csv

"""
Associates a uid with a firebase storage link to resume
"""

def generate_resume_links():
    """
    Generate resume links for all accepted applicants
    """
    applications = get_accepted_applications()
    resume_links = {}
    for application_id, application_data in applications.items():
        first_name = application_data["personal"]["firstName"]
        last_name = application_data["personal"]["lastName"]
        school = application_data["academic"]["currentSchool"]
        graduation_year = application_data["academic"]["graduationYear"]
        major = application_data["academic"]["major"]
        resume_url = application_data["openResponse"]["resume"]["url"]

        resume_links[application_id] = {
            "name": f"{first_name} {last_name}",
            "school": school,
            "graduation_year": graduation_year,
            "major": major,
            "resume_url": resume_url
        }

    return resume_links

def export_to_csv():
    resume_links = generate_resume_links()
    with open("resumes.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(["Name", "School", "Graduation Year", "Major", "Resume URL"])
        for _, application_data in resume_links.items():
            writer.writerow([
                application_data["name"],
                application_data["school"],
                application_data["graduation_year"],
                application_data["major"],
                application_data["resume_url"]
            ])

if __name__ == "__main__":
    export_to_csv()