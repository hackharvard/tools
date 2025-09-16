from helpers import get_confirmed_applications, export_to_csv, get_accepted_applications
import os
"""
Associates a uid with a tshirt size
"""

DEFAULT_FILE_PATH = "csv/tshirts.csv"

if not os.path.exists('csv'):
    print('creating new subdir: csv...')
    os.mkdir('csv')	

def generate_tshirt_sizes():
    """
    Generate resume links for all accepted applicants
    """
    confirmations =get_accepted_applications()
    tshirts = {}
    for uid, application_data in confirmations.items():
        personal = application_data["personal"]

        tshirts[uid] = {
            "name": f"{personal['firstName']} {personal['lastName']}",
            "size": application_data["hackathon"]["shirtSize"],
        }

    return tshirts

def export_tshirts(file_path=DEFAULT_FILE_PATH):
    tshirts = generate_tshirt_sizes()
    # Define the column names for the csv
    columns = ["name", "size"]

    # Convert dict to a list of dictionaries
    csv_data = [
        {"name": data["name"], "size": data["size"]}
        for data in tshirts.values()
    ]

    export_to_csv(csv_data, file_path, columns)

if __name__ == "__main__":
    export_tshirts()
