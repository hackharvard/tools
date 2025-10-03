import os
import firebase_admin
import json
import pandas as pd
from dotenv import load_dotenv
from firebase_admin import credentials, firestore

# Change this to current collections in firestore
APPLICATIONS_COLLECTION = "2025-applications" # has most info, including email
CONFIRMATIONS_COLLECTION = "2025-confirmations" 
DECISIONS_COLLECTION = "2025-decisions" 
USERS_COLLECTION = "2025-users" # has minimal info, but has hhid as well

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

# --------------GET USER DATA--------------- #

def get_applications() -> dict:
    """
    Get all applications from firestore
    """
    applications = {}
    applications_collection = db.collection(APPLICATIONS_COLLECTION).stream()
    for application in applications_collection:
        applications[application.id] = application.to_dict()
    
    return applications

def get_uids(collection_loc: str = APPLICATIONS_COLLECTION) -> list:
    """
    Get all uids from firestore
    """
    uids = []
    applications = db.collection(collection_loc).stream()
    for application in applications:
        uids.append(application.id)
    
    return uids

def get_applicant(uid: str, collection_loc: str = USERS_COLLECTION) -> dict:
    """
    Get applicant details based on the application id as a dictionary
    """
    applicant = db.collection(collection_loc).document(uid).get()
    return applicant.to_dict()

def get_applicant_hhid(uid: str) -> str:
    """
    Get the applicant hhid based on the application id
    """
    return get_applicant(uid)["hhid"]

def get_applicant_email(uid: str) -> str:
    """
    Get the email of the applicant
    """
    return get_applicant(uid, APPLICATIONS_COLLECTION)["personal"]["email"]

def get_decision(uid: str) -> str:
    """
    Get the decision of the applicant
    """
    return db.collection(DECISIONS_COLLECTION).document(uid).get().to_dict()["type"]

def get_decisions() -> dict:
    """
    Get all decisions from firestore
    """
    decisions = {}
    decisions_collection = db.collection(DECISIONS_COLLECTION).stream()
    for decision in decisions_collection:
        decisions[decision.id] = decision.to_dict()["type"]
    
    return decisions

def get_confirmation(uid: str) -> str:
    """
    Get the decision of the applicant
    """
    return db.collection(CONFIRMATIONS_COLLECTION).document(uid).get().to_dict()["confirmed"]

def get_confirmations() -> dict:
    """
    Get all decisions from firestore
    """
    confirmations = {}
    confirmations_collection = db.collection(CONFIRMATIONS_COLLECTION).stream()
    for confirmation in confirmations_collection:
        confirmations[confirmation.id] = confirmation.to_dict()["confirmed"]
    
    return confirmations

def get_accepted_applications() -> dict:
    """
    Get all accepted applications from firestore
    """
    accepted_applications = {}
    applications = get_applications()
    decisions = get_decisions()
    for uid, decision in decisions.items():
        if decision == "accepted":
            accepted_applications[uid] = applications[uid]

    return accepted_applications

def get_confirmed_applications() -> dict:
    """
    Get all confirmed participants from firestore
    """
    confirmed_participants = {}
    applications = get_applications()
    confirmations = get_confirmations()
    for uid, confirmation in confirmations.items():
        if confirmation == "Yes, I can attend all 3 days of HackHarvard.":
            confirmed_participants[uid] = applications[uid]

    return confirmed_participants

def get_all_applicants_emails(only_accepted: bool = False) -> list:
    """
    Get emails from applicants who have a decision made about them
    """
    print("Getting emails, this may take a while...")
    emails = []
    for uid, decision in get_decisions().items():
        # Set only_accepted to True if you only want emails of accepted applicants
        if only_accepted:
            if decision == "accepted":
                emails.append(get_applicant_email(uid))
        else:
            emails.append(get_applicant_email(uid))

    return emails

# -----------GET FUNCTIONS----------- #

def get_collection_func(collection: str):
    """
    Get the appropriate function to get the collection
    """
    if collection == "all":
        return get_applications
    elif collection == "accepted":
        return get_accepted_applications
    elif collection == "confirmed":
        return get_confirmed_applications
    else:
        raise ValueError("Invalid collection name")

# --------------EXPORT--------------- #

def export_to_csv(data, file_path, columns) -> None:
    """
    Export data to a csv file given some column headers and data
    """
    try:
        if isinstance(data, dict):
            df = pd.DataFrame.from_dict(data, orient='index')
        
        df = pd.DataFrame(data)

        df.to_csv(file_path, columns=columns, index=False)
        print("Data exported to", file_path)
    except Exception as e:
        print("Error exporting data to csv:", e)

def export_to_json(data, file_path) -> None:
    """
    Export data to a json file
    """
    try:
        with open(file_path, 'w') as f:
            json.dump(data, f)
        print("Data exported to", file_path)
    except Exception as e:
        print("Error exporting data to json:", e)
