from helpers import get_accepted_applications

def get_diet_restrictions():
    """
    Returns a dictionary of confirmed applicants and their diet restrictions
    """

    applications = get_accepted_applications()
    for uid, application in applications.items():
        first_name = application["personal"]["firstName"]
        last_name = application["personal"]["lastName"]
        diet_restriction = application["personal"]["dietaryRestrictions"]
        
            
    

if __name__ == "__main__":
    get_diet_restrictions()

