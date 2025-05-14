# 🧾 Jira Story Creator

This script allows you to **create Jira stories automatically** using Jira's REST API. It reads configuration from environment variables and logs activity to a file for audit and debugging purposes.

---

## 📌 Features

- Creates a **Jira Story** ticket using the provided details.
- Logs requests and errors to a file (`logs/` directory).
- Uses `.env` for secure environment configuration.
- Supports custom fields like **Story Points** and **Acceptance Criteria**.

---

## 🛠️ Setup

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd <your-repo-folder>

# Create a .env file in the root directory with the following content:

EMAIL=your-email@example.com
JIRA_INTEGRATION_KEY=your-api-token
PROJECT_KEY=PROJECT123
JIRA_BASE_URL=https://your-domain.atlassian.net

Install the required dependencies

pip install -r requirements.txt

