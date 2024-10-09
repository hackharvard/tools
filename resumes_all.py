from helpers import get_applications, export_to_csv

"""
Associates a uid with a firebase storage link to resume
"""

DEFAULT_FILE_PATH = "resumes_all.csv"

def generate_resume_links():
    """
    Generate resume links for all accepted applicants
    """
    applications = get_applications()
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

def export_resume_links(file_path=DEFAULT_FILE_PATH):
    resume_links = generate_resume_links()
    columns = ["name", "school", "graduation_year", "major", "resume_url"]
    csv_data = [
        {"name": data["name"], "school": data["school"], 
         "graduation_year": data["graduation_year"], "major": data["major"], 
         "resume_url": data["resume_url"]}
        for data in resume_links.values()
    ]
    export_to_csv(csv_data, file_path, columns)

if __name__ == "__main__":
    export_resume_links()