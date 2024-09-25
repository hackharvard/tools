from helpers import get_accepted_applications, export_to_csv

DEFAULT_FOLDER = "csv/demographics/"

def get_accepted_demographics() -> dict: 
    """
    Returns a dictionary of confirmed applicants and their demographics
    Demographics := {Name, Email, Race, Gender, Graduation Year} for each uid
    """
    apps = get_accepted_applications()
    demographics = {} 
    for uid, app_data in apps.items():
        personal = app_data["personal"]
        demographics[uid] = {
            "name": f'{personal["firstName"]} {personal["lastName"]}',
            "email": personal["email"],
            "race": personal['race'], 
            "gender": personal['gender'], 
            "grad_year": app_data["academic"]['graduationYear']
        }

    return demographics

def count_field(demographics: dict, field: str) -> dict:
    """
    Returns a dict of field data and num of people with that field data
    """
    count = {}

    for _, data in demographics.items():
        field_value = data.get(field)

        # Check if the field value is a list
        if isinstance(field_value, list):
            for value in field_value:  
                if value not in count:
                    count[value] = 0
                count[value] += 1  # Increment the count for this value
        elif field_value:  # If it's a single value and not None
            if field_value not in count:
                count[field_value] = 0
            count[field_value] += 1  

    return count

def export_demographic(demographics: dict, field: str, folder: str = DEFAULT_FOLDER):
    count = count_field(demographics, field)
    csv_data = [
        {field: field_data, "count": count}
        for field_data, count in count.items()
    ]
    columns = [field, "count"]

    export_to_csv(csv_data, folder + field + ".csv", columns)

if __name__ == "__main__":
    demographics = get_accepted_demographics()
    export_demographic(demographics, "race")
    export_demographic(demographics, "gender")
    export_demographic(demographics, "grad_year")