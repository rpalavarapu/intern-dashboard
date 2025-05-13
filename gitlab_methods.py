import csv
import requests

GITLAB_URL = "https://code.swecha.org"

def get_group_id(headers, group_payload):
    group_response = requests.get(f"{GITLAB_URL}/api/v4/groups", headers=headers, data=group_payload)
    if group_response.status_code != 201:
        print("❌ Failed to create group:", group_response.json())
        exit()
    group_id = group_response.json()["id"]
    return group_id

def create_group(headers, group_payload):
    group_response = requests.post(f"{GITLAB_URL}/api/v4/groups", headers=headers, data=group_payload)

    if group_response.status_code != 201:
        print("❌ Failed to create group:", group_response.json())
        exit()
    group_id = group_response.json()["id"]
    print(f"✅ Created group '{group_payload["name"]}' with ID: {group_id}")
    return group_id

def get_user_id(headers, username):
    user_response = requests.get(f"{GITLAB_URL}/api/v4/users", headers=headers, params={"username": username})
    if not user_response.ok or not user_response.json():
        print(f"❌ User '{username}' not found.")
        return None

    user_id = user_response.json()[0]["id"]
    return user_id

def add_members_to_group(filename, headers, group_id, access_level=30):
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            username = row["username"].strip()
            
            user_id = get_user_id(headers, username)
            if user_id is None:
                continue

            add_response = requests.post(
                f"{GITLAB_URL}/api/v4/groups/{group_id}/members",
                headers=headers,
                data={"user_id": user_id, "access_level": access_level}
            )

            if add_response.status_code == 201:
                print(f"✅ Added '{username}' to the group.")
            elif add_response.status_code == 409:
                print(f"🎓 '{username}' already exists in the group.")
            else:
                print(f"❌ Failed to add '{username}':", add_response.json(), add_response.status_code)
