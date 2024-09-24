from helpers import get_accepted_applications, get_applicant

def get_race():
    accepted = get_accepted_applications().keys()
    for applicant in accepted:
        app_data = get_applicant(applicant)
        print(app_data)

get_race()