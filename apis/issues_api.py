import requests

GITLAB_URL = "https://code.swecha.org/api/v4"


def get_gitlab_headers(token):
    return {"PRIVATE-TOKEN": token}


def fetch_project_info(headers, group_id):
    url = f"{GITLAB_URL}/projects/{group_id}"
    response = requests.get(url, headers=headers)
    return response.json()


def fetch_issues(headers, group_id, user_id, since):
    url = f"{GITLAB_URL}/projects/{group_id}/issues"
    params = {
        "assignee_id": user_id,
        "updated_after": since,
        "state": "all",
        "per_page": 100,
    }
    response = requests.get(url, headers=headers, params=params)
    return response.json()


def fetch_issues_by_username(headers, group_id, username, since):
    url = f"{GITLAB_URL}/projects/{group_id}/issues"
    params = {
        "assignee_username": username,
        "updated_after": since,
        "state": "all",
        "per_page": 100,
    }
    response = requests.get(url, headers=headers, params=params)
    return response.json()


def fetch_authored_issues(headers, group_id, user_id, since):
    url = f"{GITLAB_URL}/projects/{group_id}/issues"
    params = {
        "author_id": user_id,
        "updated_after": since,
        "state": "all",
        "per_page": 100,
    }
    response = requests.get(url, headers=headers, params=params)
    return response.json()


def fetch_all_project_issues(headers, group_id, since):
    all_issues = []
    page = 1
    per_page = 100

    while True:
        params = {
            "updated_after": since,
            "state": "all",
            "per_page": per_page,
            "page": page,
        }
        url = f"{GITLAB_URL}/projects/{group_id}/issues"
        response = requests.get(url, headers=headers, params=params)

        if response.status_code != 200:
            print(f"Error {response.status_code}: {response.text}")
            break

        data = response.json()
        if not data:
            break

        all_issues.extend(data)
        page += 1

    return all_issues


def fetch_notes(headers, group_id, issue_iid):
    url = f"{GITLAB_URL}/projects/{group_id}/issues/{issue_iid}/notes"
    response = requests.get(url, headers=headers)
    return response.json()

