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