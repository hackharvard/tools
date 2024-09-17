import os
import firebase_admin
from dotenv import load_dotenv
from firebase_admin import credentials, firestore

# Change this to current collections in firestore
APPLICATIONS_COLLECTION = "2024-applications" # has most info, including email
CONFIRMATIONS_COLLECTION = "2024-confirmations" 
DECISIONS_COLLECTION = "2024-decisions" 
USERS_COLLECTION = "2024-users" # has minimal info, but has hhid as well

# Load environment variables
load_dotenv()

# Get firebase env variables
firebase_project_id = os.getenv("FIREBASE_PROJECT_ID")
firebase_private_key = os.getenv("FIREBASE_PRIVATE_KEY")
firebase_client_email = os.getenv("FIREBASE_CLIENT_EMAIL")

# Set up firebase credentials
firebase_credentials = {
    "type": "service_account",
    "project_id": firebase_project_id,
    "private_key": firebase_private_key,
    "client_email": firebase_client_email,
    "auth_url": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": (
        f"https://www.googleapis.com/robot/v1/metadata/x509/{firebase_client_email}"
    ),
}

# Initialize firebase app
cred = credentials.Certificate(firebase_credentials)
firebase_admin.initialize_app(cred)

# Get firestore client
db = firestore.client()

# ----------------------------- #

def get_application_ids(collection_loc: str = APPLICATIONS_COLLECTION) -> list:
    """
    Get all application ids from firestore
    """
    application_ids = []
    applications = db.collection(collection_loc).stream()
    for application in applications:
        application_ids.append(application.id)
    
    return application_ids

def get_applicant(app_id: str, collection_loc: str = USERS_COLLECTION) -> dict:
    """
    Get applicant details based on the application id as a dictionary
    """
    applicant = db.collection(collection_loc).document(app_id).get()
    return applicant.to_dict()

def get_applicant_hhid(app_id: str) -> str:
    """
    Get the applicant hhid based on the application id
    """
    return get_applicant(app_id)["hhid"]

def get_applicant_email(app_id: str) -> str:
    """
    Get the email of the applicant
    """
    return get_applicant(app_id, APPLICATIONS_COLLECTION)["personal"]["email"]

def get_decision(app_id: str) -> str:
    """
    Get the decision of the applicant
    """
    return db.collection(DECISIONS_COLLECTION).document(app_id).get().to_dict()["type"]

def get_decisions() -> dict:
    """
    Get all decisions from firestore
    """
    decisions = {}
    decisions_collection = db.collection(DECISIONS_COLLECTION).stream()
    for decision in decisions_collection:
        decisions[decision.id] = decision.to_dict()["type"]
    
    return decisions

def get_all_applicants_emails(only_accepted: bool = False) -> list:
    """
    Get emails from applicants who have a decision made about them
    """
    print("Getting emails, this may take a while...")
    emails = []
    for application_id, decision in get_decisions().items():
        # Set only_accepted to True if you only want emails of accepted applicants
        if only_accepted:
            if decision == "accepted":
                emails.append(get_applicant_email(application_id))
        else:
            emails.append(get_applicant_email(application_id))

    return emails
