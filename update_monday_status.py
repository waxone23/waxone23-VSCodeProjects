import requests
import json

# --- CONFIGURATION ---
API_KEY = "YOUR_MONDAY_API_KEY"
API_URL = "https://api.monday.com/v2"
HEADERS = {"Authorization": API_KEY, "Content-Type": "application/json"}


def update_monday_status(item_id, status_text):
    """
    Updates a 'Status' column on Monday.com to a specific value.
    """
    # GraphQL query (The language Monday.com speaks)
    query = """
    mutation ($itemId: Int!, $columnId: String!, $statusValue: String!) {
      change_simple_column_value (item_id: $itemId, board_id: YOUR_BOARD_ID, column_id: $columnId, value: $statusValue) {
        id
      }
    }
    """

    variables = {
        "itemId": int(item_id),
        "columnId": "status",  # Usually 'status' or 'label'
        "statusValue": status_text,
    }

    data = {"query": query, "variables": variables}

    response = requests.post(url=API_URL, json=data, headers=HEADERS)

    if response.status_code == 200:
        print(f"✅ Monday.com Updated: Item {item_id} is now '{status_text}'")
    else:
        print(f"❌ Failed to update Monday.com: {response.text}")


# --- Integration Example ---
# This would be triggered by your Render Watcher script
# update_monday_status("123456789", "Ready for Review")
