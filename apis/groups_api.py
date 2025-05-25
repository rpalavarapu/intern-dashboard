import requests

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
