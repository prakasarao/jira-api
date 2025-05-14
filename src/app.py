from flask import Flask, request, jsonify
import os
import json
import requests
import logging
from dotenv import load_dotenv
from datetime import datetime

from services.jirastory import create_jira_story

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

app = Flask(__name__)

@app.route("/create_jirastory", methods=["POST"])
def api_create_jira_story():
    data = request.json
    required_fields = ["title", "business_value", "description", "story_points", "priority", "acceptance_criteria"]

    if not all(field in data for field in required_fields):
        return jsonify({"success": False, "error": "Missing one or more required fields"}), 400

    result = create_jira_story(
        title=data["title"],
        business_value=data["business_value"],
        description=data["description"],
        story_points=data["story_points"],
        priority=data["priority"],
        acceptance_criteria=data["acceptance_criteria"]
    )

    status_code = 200 if result.get("success") else 500
    return jsonify(result), status_code

if __name__ == "__main__":
    app.run(debug=True)
