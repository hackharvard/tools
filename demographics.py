from helpers import get_accepted_applications;

def get_accepted_demographics()-> dict : 
    """
    Returns a dictionary of confirmed applicants and their demographics
    Demographics := {Race, Gender, Graduation Year}
    """
    apps = get_accepted_applications();
    ethnicity = {} # app_id |-> demographics information
    for app_id, app_data in apps.items():
        race = app_data["personal"]['race']; gender = app_data["personal"]['gender']; 
        grad_year = app_data["meta"]['graduationYear'];
        name = f'{app_data["personal"]["firstName"]} {app_data["personal"]["lastName"]}'
        uid = app_id
        hhid = app_data["meta"]["hhid"]
        email = app_data["personal"]["email"]
        ethnicity[uid] = {
            "name": name,
            "hhid": hhid,
            "email": email,
            "race": race, "gender": gender, grad_year: grad_year
        }
        print(ethnicity)
        break
if  __name__ == "__main__":
    get_accepted_demographics();