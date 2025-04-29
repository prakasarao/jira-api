import os
import json
import requests
import logging
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Configure logging
log_file = os.path.join(log_dir, f"app_{datetime.now().strftime('%Y_%m_%d')}.log")
logging.basicConfig(
    filename=log_file,
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


EMAIL = os.environ.get("EMAIL")
API_TOKEN = os.environ.get("JIRA_INTEGRATION_KEY")
PROJECT_KEY = os.environ.get("PROJECT_KEY")
JIRA_BASE_URL = os.environ.get("JIRA_BASE_URL")

def create_jira_story(title, business_value, description, story_points, priority, acceptance_criteria):
    """
    Creates a Jira story with the given details using Jira's REST API.
    """
    try:
        url = f"{JIRA_BASE_URL}/rest/api/3/issue"
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        auth = (EMAIL, API_TOKEN)

        payload = {
            "fields": {
                "project": {"key": PROJECT_KEY},
                "summary": title,
                "description": {
                    "type": "doc",
                    "version": 1,
                    "content": [
                        {
                            "type": "paragraph",
                            "content": [
                                {"type": "text", "text": description}
                            ]
                        },
                        {
                            "type": "paragraph",
                            "content": [
                                {
                                    "type": "text",
                                    "text": "Business Value: ",
                                    "marks": [{"type": "strong"}]
                                },
                                {
                                    "type": "text",
                                    "text": business_value
                                }
                            ]
                        }
                    ]
                },
                "issuetype": {"name": "Story"},
                # "parent": {"key": epic_key},
                "customfield_10030": int(story_points),  # Story Points
                "priority": {"name": priority},
                "customfield_10270": {  # Acceptance Criteria
                    "type": "doc",
                    "version": 1,
                    "content": [
                        {
                            "type": "paragraph",
                            "content": [
                                {"type": "text", "text": acceptance_criteria}
                            ]
                        }
                    ]
                }
            }
        }

        response = requests.post(url, headers=headers, auth=auth, data=json.dumps(payload))
        
        if response.status_code == 201:
            issue_key = response.json().get("key")
            jira_url = f"{JIRA_BASE_URL}/browse/{issue_key}"
            print(f"Jira ticket created successfully: {jira_url}")
            logging.info(f"Jira ticket created successfully: {jira_url}")
            return issue_key
        else:
            print(f"Failed to create Jira ticket: {response.status_code} - {response.text}")
            logging.error(f"Failed to create Jira ticket: {response.status_code} - {response.text}")
            return None

    except Exception as e:
        logging.exception("Exception occurred while creating Jira ticket")
        print(f"An error occurred while creating Jira ticket: {e}")
        return None

# Example usage
if __name__ == "__main__":
    create_jira_story(
        title="Test Jira Ticket",
        business_value="Allows customers to find hotels based on their preferences",
        description="This is a test description for the Jira ticket.",
        story_points=8,
        priority="Medium",
        acceptance_criteria="Added Acceptance Criteria"
    )
