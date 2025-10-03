from helpers import get_collection_func, export_to_csv
from dataclasses import dataclass, fields
import argparse

DEFAULT_FILE_PATH = "csv/resumes.csv"

@dataclass(frozen=True)
class RowData:
    first_name: str
    last_name: str
    age: str
    email: str
    school: str
    phone: str
    level_of_study: str
    country: str
    graduation_year: str
    major: str
    codeOfConduct: bool
    mlhEmails: bool
    sharing: bool
    submitting: bool
    resume_url: str

def generate_resume_links(get_applications):
    applications = get_applications()
    resume_links = {}
    for application_id, application_data in applications.items():
        personal   = application_data.get("personal", {})
        academic   = application_data.get("academic", {})
        agreements = application_data.get("agreements", {})

        first_name      = personal.get("firstName")
        last_name       = personal.get("lastName")
        age             = personal.get("age")
        email           = personal.get("email")
        phone           = personal.get("phoneNumber")
        country         = personal.get("countryOfResidence")
        school          = academic.get("currentSchool")
        major           = academic.get("major")
        graduation_year = academic.get("graduationYear")
        level_of_study  = academic.get("levelOfStudy")
        codeOfConduct   = agreements.get("codeOfConduct")
        mlhEmails       = agreements.get("mlhEmails")
        sharing         = agreements.get("sharing")
        submitting      = agreements.get("submitting")
        resume_url      = application_data.get("openResponse", {}) \
                                          .get("resume", {}) \
                                          .get("url", "")

        row = RowData(
            first_name=first_name,
            last_name=last_name,
            age=age,
            email=email,
            school=school,
            phone=phone,
            level_of_study=level_of_study,
            country=country,
            graduation_year=graduation_year,
            major=major,
            codeOfConduct=codeOfConduct,
            mlhEmails=mlhEmails,
            sharing=sharing,
            submitting=submitting,
            resume_url=resume_url
        )

        resume_links[application_id] = row

    return resume_links

def export_resume_links(get_applications, file_path=DEFAULT_FILE_PATH):
    resume_links = generate_resume_links(get_applications)
    columns = [f.name for f in fields(RowData)]
    csv_data = [
        {f.name: getattr(data, f.name) for f in fields(RowData)} 
        for data in resume_links.values()
    ]
    export_to_csv(csv_data, file_path, columns)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate and export resume links for accepted applicants"
    )

    parser.add_argument(
        "-o", "--output",
        dest="output",
        default=DEFAULT_FILE_PATH,
        help=f"Output CSV file path (default: {DEFAULT_FILE_PATH})"
    )

    parser.add_argument(
        "-collection", "-c", "--collection",
        required=True,
        dest="collection",
        choices=["all", "accepted", "confirmed"],
        help="Collection to get resumes from."
    )

    args = parser.parse_args()

    get_applications = get_collection_func(args.collection)
    output = args.output if args.output else DEFAULT_FILE_PATH

    export_resume_links(get_applications, output)
