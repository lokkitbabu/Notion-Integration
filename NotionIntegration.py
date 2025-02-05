import requests
import json

# Notion API Configuration
NOTION_API_URL = "https://api.notion.com/v1"
NOTION_API_KEY = "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"
NOTION_DATABASE_ID = "2921d3b640a5475c9a006d213de6a576"

notion_headers = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

def verify_database(notion_database_id):
    url = f"https://api.notion.com/v1/databases/{notion_database_id}"
    response = requests.get(url, headers=notion_headers)
    print(response.status_code, response.json())

    if response.status_code == 200:
        print("Database verified successfully!")
    else:
        print("Error verifying database:", response.status_code, response.json())


# Push assignments from JSON to Notion
def push_to_notion(json_file):
    with open(json_file, "r") as f:
        data = json.load(f)

    for assignment in data:
        course_name = assignment.get("course_name", "Unknown Course")
        assignment_name = assignment.get("assignment_name", "Unnamed Assignment")
        due_date = assignment.get("due_at", None)

        notion_data = {
            "parent": {"database_id": NOTION_DATABASE_ID},
            "properties": {
                "Assignment Name": {"title": [{"text": {"content": assignment_name}}]},
                "Deadline": {"date": {"start": due_date} if due_date else None},
                "Done": {"checkbox": False},  # Default to not done
            }
        }

        response = requests.post(f"{NOTION_API_URL}/pages", headers=notion_headers, json=notion_data)
        if response.status_code == 200:
            print(f"Successfully added assignment '{assignment_name}' to Notion.")
        else:
            print(f"Error sending assignment '{assignment_name}' to Notion:", response.status_code, response.text)

# Main function
if __name__ == "__main__":
    verify_database(NOTION_DATABASE_ID)
    push_to_notion("all_assignments.json")
