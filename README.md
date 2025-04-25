# Jira Ticket and Subtask Automation Documentation

## Overview
This script allows you to automate the creation of Jira Stories and Subtasks using the Jira REST API. It uses environment variables for configuration and makes authenticated HTTP requests to create the issues.

## Requirements
- Python 3.x
- `requests` library
- `.env` file with the following variables:
  - `EMAIL`: Your Jira user email
  - `JIRA_INTEGRATION_KEY`: Your Jira API token
  - `PROJECT_KEY`: Your Jira project key
  - `JIRA_BASE_URL`: Your Jira instance base URL (e.g., https://yourdomain.atlassian.net)
  - `Subtaskid`: The ID of the Subtask issue type in your Jira instance

## Setup
1. Install required dependencies:
   ```bash
   pip install requests python-dotenv
   ```

2. Create a `.env` file in the root of your project with the following contents:
   ```env
   EMAIL=your_email@example.com
   JIRA_INTEGRATION_KEY=your_api_token
   PROJECT_KEY=YOURPROJECT
   JIRA_BASE_URL=https://yourdomain.atlassian.net
   Subtaskid=your_subtask_issue_type_id
   ```

3. Make sure your Jira instance has a Story and Subtask issue type configured.

## Script Functions

### `create_jira_story(summary, epic_key, description)`
Creates a Jira Story linked to an Epic.
- `summary`: Title of the Story.
- `epic_key`: Key of the parent Epic (e.g., "SCRUM-1").
- `description`: Description of the Story.

#### Example
```python
create_jira_story("Test Jira Ticket", "SCRUM-7", "This is a test description for the Jira ticket.")
```

### `create_jira_subtask(summary, parent_story, description, story_points)`
Creates a Jira Subtask under a Story.
- `summary`: Title of the Subtask.
- `parent_story`: Key of the parent Story (e.g., "SCRUM-34").
- `description`: Description of the Subtask.
- `story_points`: Estimation points for the Subtask.

#### Example
```python
create_jira_subtask("Subtask for SCRUM-34", "SCRUM-34", "This is a subtask under the story SCRUM-34.", 8)
```

## Notes
- Make sure the `customfield_10014` and `customfield_10030` used in the script match the field IDs in your Jira instance.
- The script prints the URL of the created Jira issue or an error message if the creation fails.

## Conclusion
This script simplifies the creation of Jira Stories and Subtasks via API. It's useful for project managers, scrum masters, or developers who want to automate ticket creation in Agile workflows.
