import requests

def get_gitlab_headers(token):
    return {"PRIVATE-TOKEN": token}

def fetch_project_info(api_url, project_id, headers):
    url = f"{api_url}/projects/{project_id}"
    return requests.get(url, headers=headers).json()

def fetch_project_members(api_url, project_id, headers):
    members = []
    page = 1
    while True:
        url = f"{api_url}/projects/{project_id}/members/all?per_page=100&page={page}"
        res = requests.get(url, headers=headers)
        if res.status_code != 200:
            break
        data = res.json()
        if not data:
            break
        members.extend(data)
        if len(data) < 100:
            break
        page += 1
    return members

def fetch_issues(api_url, project_id, user_id, since, headers):
    url = f"{api_url}/projects/{project_id}/issues"
    params = {
        "assignee_id": user_id,
        "updated_after": since,
        "state": "all",
        "per_page": 100
    }
    return requests.get(url, headers=headers, params=params).json()

def fetch_issues_by_username(api_url, project_id, username, since, headers):
    url = f"{api_url}/projects/{project_id}/issues"
    params = {
        "assignee_username": username,
        "updated_after": since,
        "state": "all",
        "per_page": 100
    }
    return requests.get(url, headers=headers, params=params).json()

def fetch_authored_issues(api_url, project_id, user_id, since, headers):
    url = f"{api_url}/projects/{project_id}/issues"
    params = {
        "author_id": user_id,
        "updated_after": since,
        "state": "all",
        "per_page": 100
    }
    return requests.get(url, headers=headers, params=params).json()

def fetch_all_project_issues(api_url, project_id, since, headers):
    all_issues = []
    page = 1
    while True:
        url = f"{api_url}/projects/{project_id}/issues"
        params = {
            "updated_after": since,
            "state": "all",
            "per_page": 100,
            "page": page
        }
        res = requests.get(url, headers=headers, params=params)
        if res.status_code != 200:
            break
        data = res.json()
        if not data:
            break
        all_issues.extend(data)
        if len(data) < 100:
            break
        page += 1
    return all_issues

def fetch_notes(api_url, project_id, issue_iid, headers):
    url = f"{api_url}/projects/{project_id}/issues/{issue_iid}/notes"
    return requests.get(url, headers=headers).json()

