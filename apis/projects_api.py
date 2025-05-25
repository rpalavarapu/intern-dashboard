from urllib.parse import quote
import requests

def check_file_in_project(headers, project_path, file_path):
    encoded_project = quote(project_path, safe="")
    encoded_file = quote(file_path, safe="")
    url = f"https://code.swecha.org/api/v4/projects/{encoded_project}/repository/files/{encoded_file}/raw"

    response = requests.get(url, headers=headers, params={"ref": "main"})

    if response.status_code == 200:
        return True
    else:
        return False