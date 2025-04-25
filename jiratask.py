import os
import json
import requests
import logging
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

# === Constants ===
LOG_DIR = "logs"
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"

# === Ensure log directory exists ===
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# === Configure logging ===
log_file = os.path.join(LOG_DIR, f"app_{datetime.now().strftime('%Y_%m_%d')}.log")
logging.basicConfig(filename=log_file, level=logging.DEBUG, format=LOG_FORMAT)

# === Load environment variables ===
EMAIL = os.getenv("EMAIL")
API_TOKEN = os.getenv("JIRA_INTEGRATION_KEY")
PROJECT_KEY = os.getenv("PROJECT_KEY")
JIRA_BASE_URL = os.getenv("JIRA_BASE_URL")
SUBTASKID = os.getenv("Subtaskid")


def create_jira_task(summary: str, epic_key: str, description: str, story_points: int) -> str | None:
    """
    Create a Jira task under the given epic with specified details.
    Returns the created issue key or None if creation fails.
    """
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
                "content": [
                    {
                        "type": "paragraph",
                        "content": [{"text": description, "type": "text"}]
                    }
                ]
            },
            "issuetype": {"name": "Task"},
            "parent": {"key": epic_key},
            "customfield_10030": int(story_points)
        }
    }

    try:
        response = requests.post(url, headers=headers, auth=auth, data=json.dumps(payload))
        response.raise_for_status()  # Raises exception for non-2xx codes

        issue_key = response.json().get("key")
        logging.info(f"Jira ticket created successfully: {JIRA_BASE_URL}/browse/{issue_key}")
        print(f"Jira ticket created successfully: {JIRA_BASE_URL}/browse/{issue_key}")
        return issue_key

    except requests.exceptions.RequestException as e:
        logging.exception("Error occurred while creating Jira task")
        print(f"Failed to create Jira ticket: {e}")
        return None


def main():
    try:
        if not all([EMAIL, API_TOKEN, PROJECT_KEY, JIRA_BASE_URL]):
            raise EnvironmentError("Missing required environment variables")

        create_jira_task(
            summary="Test Creating a Jira Ticket for Task",
            epic_key="SCRUM-7",
            description="This is a test description for the Jira Task ticket.",
            story_points=2
        )

    except Exception as e:
        logging.exception("Unexpected error in main execution")
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
