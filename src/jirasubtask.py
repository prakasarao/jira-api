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
SUBTASKID = os.environ.get("Subtaskid")

def create_jira_subtask(summary, parent_story, description, story_points, priority, acceptance_criteria):
    """
    Create a Jira subtask with dynamic priority.
    - summary: The summary of the subtask.
    - parent_story: The parent story key (e.g., SCRUM-34).
    - description: A detailed description of the subtask.
    - story_points: Number of story points for the subtask.
    - priority: The priority of the subtask (e.g., 'High', 'Medium', 'Low').
    - acceptance_criteria: Acceptance criteria for the subtask.
    
    Returns the issue key of the created subtask if successful, else None.
    """
    try:
        # Check if all required environment variables are loaded
        if not all([EMAIL, API_TOKEN, PROJECT_KEY, JIRA_BASE_URL, SUBTASKID]):
            raise EnvironmentError("Missing one or more required environment variables.")

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
                "description": {
                    "type": "doc",
                    "version": 1,
                    "content": [{"type": "paragraph", "content": [{"text": description, "type": "text"}]}]
                },
                "issuetype": {"id": SUBTASKID},
                "parent": {"key": parent_story},
                "customfield_10030": story_points,
                "priority": {"name": priority},  # Priority field dynamically set
                "customfield_10270": {
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

        # Sending POST request to Jira API
        response = requests.post(url, headers=headers, auth=auth, data=json.dumps(payload))
        response.raise_for_status()  # This will raise an exception for any 4xx or 5xx status code

        if response.status_code == 201:
            issue_key = response.json().get("key")
            print(f"Subtask created successfully: {JIRA_BASE_URL}/browse/{issue_key}")
            logging.info(f"Subtask created successfully: {JIRA_BASE_URL}/browse/{issue_key}")
            return issue_key
        else:
            raise Exception(f"Failed to create subtask. Status code: {response.status_code}, Response: {response.text}")

    except requests.exceptions.RequestException as e:
        logging.error(f"Request error occurred while creating the subtask: {e}")
        print(f"Request error occurred: {e}")
        return None

    except EnvironmentError as e:
        logging.error(f"Environment error: {e}")
        print(f"Environment error: {e}")
        return None

    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        print(f"Unexpected error: {e}")
        return None

# Example usage:
create_jira_subtask(
    summary="Subtask for SCRUM-34",
    parent_story="SCRUM-67",
    description="This is a subtask under the story SCRUM-34.",
    story_points=8,
    priority="Medium",  # Priority can be passed here
    acceptance_criteria="Added Acceptance Criteria"
)
