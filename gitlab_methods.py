import csv
import requests
from urllib.parse import quote

GITLAB_URL = "https://code.swecha.org"


def create_group(headers, group_payload):
    group_response = requests.post(
        f"{GITLAB_URL}/api/v4/groups", headers=headers, data=group_payload
    )

    if group_response.status_code != 201:
        print("❌ Failed to create group:", group_response.json())
        exit()
    group_id = group_response.json()["id"]
    print(f"✅ Created group '{group_payload['name']}' with ID: {group_id}")
    return group_id


def remove_projects(headers, projectsList):
    for project in projectsList:
        project_id = project["id"]
        project_response = requests.delete(
            f"{GITLAB_URL}/api/v4/projects/{project_id}", headers=headers
        )
        if project_response.status_code == 202:
            print(f"✅ '{project['name']}' deleted.")
        else:
            print("❌ Failed to delete:", project_response.json())


def remove_group(headers, groupNames):
    for groupName in groupNames:
        group_id = groupName["id"]
        group_response = requests.delete(
            f"{GITLAB_URL}/api/v4/groups/{group_id}", headers=headers
        )
        if group_response.status_code == 202:
            print(f"✅ '{groupName}' deleted.")
        else:
            print("❌ Failed to delete:", group_response.json())


def add_members_to_group(filename, headers, group_id, access_level=30):
    with open(filename, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            username = row["username"].strip()
            user_id = get_user_id(headers, username)
            if user_id is None:
                continue

            add_response = requests.post(
                f"{GITLAB_URL}/api/v4/groups/{group_id}/members",
                headers=headers,
                data={"user_id": user_id, "access_level": access_level},
            )
            if add_response.status_code == 201:
                print(f"✅ Added '{username}' to the group.")
            elif add_response.status_code == 409:
                print(f"🎓 '{username}' already exists in the group.")
            else:
                print(
                    f"❌ Failed to add '{username}':",
                    add_response.json(),
                    add_response.status_code,
                )


def check_file_in_repo(headers, project_path, file_path):
    encoded_project = quote(project_path, safe="")
    encoded_file = quote(file_path, safe="")
    url = f"https://code.swecha.org/api/v4/projects/{encoded_project}/repository/files/{encoded_file}/raw"

    response = requests.get(url, headers=headers, params={"ref": "main"})

    if response.status_code == 200:
        return True
    else:
        return False


def get_all_users_from_group(headers, group_id):
    members = []
    page = 1
    per_page = 100  # GitLab allows up to 100 per page

    while True:
        url = f"https://code.swecha.org/api/v4/groups/{group_id}/members/all"
        params = {"page": page, "per_page": per_page}
        response = requests.get(url, headers=headers, params=params)

        if response.status_code != 200:
            print(f"Error {response.status_code}: {response.text}")
            break

        data = response.json()
        if not data:
            break  # No more data

        members.extend(data)
        page += 1
    return members


def update_access_level(group_id, users, headers, level):
    for user in users:
        user_id = get_user_id(headers, user)
        response = requests.put(
            f"{GITLAB_URL}/api/v4/projects/{group_id}/members/",
            headers=headers,
            data={"user_id": user_id, "access_level": level},
        )
        if response.status_code == 200:
            print("✅ Updated access level.")
        else:
            print("❌ Failed to update.", response.json())


def update_project_access_level(project_id, users, headers, level):
    for user in users:
        user_id = get_user_id(headers, user)
        response = requests.post(
            f"{GITLAB_URL}/api/v4/projects/{project_id}/members",
            headers=headers,
            data={
                "user_id": user_id,
                "access_level": level,  # e.g., 10, 20, 30, 40
            },
        )
        if response.status_code == 200:
            print("✅ Updated access level.")
        else:
            print("❌ Failed to update.", response.json())


def get_group_id(headers, group_payload):
    group_response = requests.get(
        f"{GITLAB_URL}/api/v4/groups", headers=headers, data=group_payload
    )
    if group_response.status_code != 201:
        print("❌ Failed to create group:", group_response.json())
        exit()
    group_id = group_response.json()["id"]
    return group_id


def get_user_id(headers, username):
    user_response = requests.get(
        f"{GITLAB_URL}/api/v4/users", headers=headers, params={"username": username}
    )
    if not user_response.ok or not user_response.json():
        print(f"❌ User '{username}' not found.")
        return None

    user_id = user_response.json()[0]["id"]
    return user_id


def get_all_groups(headers, group_id):
    response = requests.get(
        f"{GITLAB_URL}/api/v4/groups/{group_id}/projects", headers=headers
    )
    if response.status_code == 200:
        print("✅ All groups retrieved.")
    else:
        print("❌ Failed to retrieve.", response.status_code)
    return response.json()
