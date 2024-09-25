from helpers import get_accepted_applications, export_to_csv

DEFAULT_FILE_PATH = "csv/diet_restrictions.csv"

def get_diet_restrictions() -> dict: 
    """
    Returns a dictionary of confirmed applicants and their diet restrictions
    """
    applications = get_accepted_applications()
    diet_restrictions = {}
    for uid, application in applications.items():
        personal = application["personal"]
        diet_restriction = personal["dietaryRestrictions"]
        # Check if the applicant has any diet restrictions, skip if they don't
        if not diet_restriction:
            continue

        diet_restrictions[uid] = {
            "name": f"{personal['firstName']} {personal['lastName']}",
            "dietaryRestrictions": diet_restriction
        }

    return diet_restrictions

def count_diet_restrictions(diet_restrictions : dict) -> dict:
    """
    Returns a dict of diet restrictions and num of people with that restriction
    """
    count = {}
    for _, restriction in diet_restrictions.items():
        diets = restriction["dietaryRestrictions"]

        # Since all vegans are vegetarians, count them as only vegans, not both
        if "vegan" in diets and "vegetarian" in diets:
            if 'vegan' in count:
                count['vegan'] += 1
            else:
                count['vegan'] = 1
            continue

        # Count all other diet restrictions
        for diet in diets:
            if diet in count:
                count[diet] += 1
            else:
                count[diet] = 1

    return count

def export_diet_restrictions():
    diet_restrictions = get_diet_restrictions()
    count = count_diet_restrictions(diet_restrictions)
    csv_data = [
        {"diet": diet, "count": count}
        for diet, count in count.items()
    ]
    columns = ["diet", "count"]
    export_to_csv(csv_data, "csv/diet_restrictions.csv", columns)
        
if __name__ == "__main__":
    export_diet_restrictions()
