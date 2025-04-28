import requests
import os
from dotenv import load_dotenv

load_dotenv()

JIRA_BASE_URL = "https://edvenswatech.atlassian.net"
EMAIL = os.environ.get("email")
API_TOKEN = os.environ.get("jira_integration_key")

url = f"{JIRA_BASE_URL}/rest/api/3/field"
headers = {"Accept": "application/json"}
auth = (EMAIL, API_TOKEN)

# response = requests.get(url, headers=headers, auth=auth)

# if response.status_code == 200:
#     fields = response.json()
#     for field in fields:
#         if "priority" in field["name"].lower():
#             print(f"{field['name']}: {field['id']}")
# else:
#     print(f"Failed to fetch fields: {response.text}")

def get_acceptance_criteria_field():
    url = f"{JIRA_BASE_URL}/rest/api/3/field"
    response = requests.get(url, auth=(EMAIL, API_TOKEN))

    if response.status_code == 200:
        fields = response.json()
        for field in fields:
            if field.get("name", "").lower() == "acceptance criteria":
                print(f"Field Name: {field['name']}")
                print(f"Field ID: {field['id']}")
                return field['id']
        print("Acceptance Criteria field not found.")
    else:
        print("Failed to fetch fields:", response.status_code, response.text)

get_acceptance_criteria_field()

def get_story_points_field():
    url = f"{JIRA_BASE_URL}/rest/api/3/field"
    response = requests.get(url, auth=(EMAIL, API_TOKEN))

    if response.status_code == 200:
        fields = response.json()
        for field in fields:
            # Look for the "Story Points" field by name (case-insensitive)
            if field.get("name", "").lower() == "story points":
                print(f"Field Name: {field['name']}")
                print(f"Field ID: {field['id']}")
                return field['id']
        print("Story Points field not found.")
    else:
        print("Failed to fetch fields:", response.status_code, response.text)

# Call the function
get_story_points_field()