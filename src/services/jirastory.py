from flask import Flask, request, jsonify
import os
import json
import requests
import logging
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

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
                            "content": [{"type": "text", "text": description}]
                        },
                        {
                            "type": "paragraph",
                            "content": [
                                {"type": "text", "text": "Business Value: ", "marks": [{"type": "strong"}]},
                                {"type": "text", "text": business_value}
                            ]
                        }
                    ]
                },
                "issuetype": {"name": "Story"},
                # "parent": {"key": epic_key},
                "customfield_10030": int(story_points),  # Story Points
                "priority": {"name": priority},
                "customfield_10270": {
                    "type": "doc",
                    "version": 1,
                    "content": [
                        {
                            "type": "paragraph",
                            "content": [{"type": "text", "text": acceptance_criteria}]
                        }
                    ]
                }
            }
        }

        response = requests.post(url, headers=headers, auth=auth, data=json.dumps(payload))

        if response.status_code == 201:
            issue_key = response.json().get("key")
            jira_url = f"{JIRA_BASE_URL}/browse/{issue_key}"
            logging.info(f"Jira ticket created: {jira_url}")
            return {"success": True, "issue_key": issue_key, "url": jira_url}
        else:
            logging.error(f"Failed to create Jira ticket: {response.status_code} - {response.text}")
            return {"success": False, "error": response.text, "status": response.status_code}

    except Exception as e:
        logging.exception("Exception occurred while creating Jira ticket")
        return {"success": False, "error": str(e)}

