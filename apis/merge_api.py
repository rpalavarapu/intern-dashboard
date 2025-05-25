def get_merge_requests(headers, project_id):
    all_mrs = []
    page = 1
    per_page = 100
    while True:
        url = f"{GITLAB_URL}/api/v4/projects/{project_id}/merge_requests"
        try:
            response = requests.get(
                url,
                headers=headers,
                params={"state": "opened", "page": page, "per_page": per_page}
            )
            response.raise_for_status()
            mrs = response.json()
            if not mrs:
                break
            all_mrs.extend(mrs)
            page += 1
        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching merge requests (page {page}): {e}, Response: {e.response.text if e.response else 'No response'}")
            raise
    return all_mrs

def get_merge_request_changes(headers, project_id, mr_iid):
    url = f"{GITLAB_URL}/api/v4/projects/{project_id}/merge_requests/{mr_iid}/changes"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def accept_merge_request(headers, project_id, mr_iid):
    url = f"{GITLAB_URL}/api/v4/projects/{project_id}/merge_requests/{mr_iid}/merge"
    response = requests.put(url, headers=headers)
    response.raise_for_status()
    return response.json()

def comment_on_merge_request(headers, project_id, mr_iid, message):
    url = f"{GITLAB_URL}/api/v4/projects/{project_id}/merge_requests/{mr_iid}/notes"
    data = {"body": message}
    response = requests.post(url, headers=headers, data=data)
    response.raise_for_status()
    print(f"💬 Comment added to MR #{mr_iid}")







