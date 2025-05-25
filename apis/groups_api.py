import requests
import csv

from apis.users_api import get_user_id

GITLAB_URL = "https://code.swecha.org"


def get_group_id(headers, params):
    group_response = requests.get(
        f"{GITLAB_URL}/api/v4/groups", headers=headers, params=params
    )
    if group_response.status_code >= 401:
        print("Failed to get group id:", group_response.json())
        exit()
    group_id = group_response.json()[0]["id"]
    return group_id


def get_all_users_from_group(headers, group_id):
    members = []
    page = 1
    per_page = 100  # GitLab allows up to 100 per page

    while True:
        params = {"page": page, "per_page": per_page}
        response = requests.get(
            f"https://code.swecha.org/api/v4/groups/{group_id}/members/all",
            headers=headers,
            params=params,
        )

        if response.status_code != 200:
            print(f"Error {response.status_code}: {response.text}")
            break

        data = response.json()
        if not data:
            break  # No more data

        members.extend(data)
        page += 1
    return members


def add_members_to_group(headers, group_id, filename, access_level=30):
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
                print(f"Added '{username}' to the group.")
            elif add_response.status_code == 409:
                print(f"'{username}' already exists in the group.")
            else:
                print(
                    f"Failed to add '{username}':",
                    add_response.json(),
                    add_response.status_code,
                )


def update_access_level(headers, group_id, filename, level):
    with open(filename, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            username = row["username"].strip()
            user_id = get_user_id(headers, username)
            response = requests.put(
                f"{GITLAB_URL}/api/v4/projects/{group_id}/members/",
                headers=headers,
                data={"user_id": user_id, "access_level": level},
            )
            if response.status_code == 200:
                print("Updated access level.")
            else:
                print("Failed to update.", response.json())
