# apis/projects_api.py
from urllib.parse import quote
from utils.fetch import make_api_request
import os

def check_file_in_project(project_path, file_path):
    encoded_project = quote(project_path, safe="")
    encoded_file = quote(file_path, safe="")
    url = f"https://code.swecha.org/api/v4/projects/ {encoded_project}/repository/files/{encoded_file}/raw"
    headers = {"PRIVATE-TOKEN": os.getenv("GITLAB_TOKEN")}
    response = make_api_request(url, headers, params={"ref": "main"})
    return response is not None

def run_check_file():
    print("\n📁 Check File in Project Repository")
    project_path = input("📥 Enter Project Path (e.g., group/project): ").strip()
    file_path = input("📄 Enter File Path (e.g., README.md): ").strip()
    
    exists = check_file_in_project(project_path, file_path)
    if exists:
        print(f"✅ File '{file_path}' exists in '{project_path}'.")
    else:
        print(f"❌ File '{file_path}' NOT FOUND in '{project_path}'.")