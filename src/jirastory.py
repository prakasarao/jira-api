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



def create_jira_story(summary, epic_key, description, story_points, priority, acceptance_criteria):
    url = f"{JIRA_BASE_URL}/rest/api/3/issue"
    
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    
    auth = (EMAIL, API_TOKEN)
    
    payload = {
        "fields": {
            "project": {"key": PROJECT_KEY},
            "summary": summary,
            "description": {"type": "doc", "version": 1, "content": [{"type": "paragraph", "content": [{"text": description, "type": "text"}]}]},
            "issuetype": {"name": "Story"},
            "parent": {"key": epic_key},
            "customfield_10030": int(story_points),
            "priority": {"name": priority},
            "customfield_10270" : {
                "type": "doc",
                "version": 1,
                "content": [
                    {
                        "type": "paragraph",
                        "content": [{"text": acceptance_criteria, "type": "text"}]
                    }
                ]
            }
        }
    }

    
    response = requests.post(url, headers=headers, auth=auth, data=json.dumps(payload))

    if response.status_code == 201:
        issue_key = response.json().get("key")
        print(f"Jira ticket created successfully: {JIRA_BASE_URL}/browse/{issue_key}")
        logging.info(f"Jira ticket created successfully: {JIRA_BASE_URL}/browse/{issue_key}")
        return issue_key
    else:
        print(f"Failed to create Jira ticket: {response.text}")
        logging.error(f"Failed to create Jira ticket: {response.text}")
        return None

create_jira_story("Test Jira Ticket", "SCRUM-7", "This is a test description for the Jira ticket.", 8, "Medium", "Added Acceptance Criteria")