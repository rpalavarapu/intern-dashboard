# apis/commits_api.py
from utils.fetch import fetch_paginated_data
from utils.auth import get_gitlab_headers, get_group_id
from datetime import datetime, timedelta

GITLAB_BASE_URL = "https://code.swecha.org/api/v4"

def get_projects(group_id_or_path):
    url_base = f"{GITLAB_BASE_URL}/groups/{group_id_or_path}/projects"
    return fetch_paginated_data(url_base, get_gitlab_headers())

def get_commits_for_project(project_id, since_date):
    url_base = f"{GITLAB_BASE_URL}/projects/{project_id}/repository/commits"
    extra_params = {'since': since_date.isoformat()}
    return fetch_paginated_data(url_base, get_gitlab_headers(), extra_params)

def summarize_commit(message):
    message = message.lower()
    if "fix" in message or "bug" in message:
        return "🛠️ Fix applied"
    elif "add" in message or "create" in message:
        return "➕ Feature added"
    elif "update" in message or "upgrade" in message:
        return "🔄 Updated content"
    elif "remove" in message or "delete" in message:
        return "❌ Removed content"
    elif "refactor" in message:
        return "♻️ Refactored code"
    else:
        return message.capitalize()

def run_commits():
    print("\n📂 Fetching Commits...")
    group = input("📥 Enter Group ID or Path: ").strip()
    days_input = input("📆 Days back to check commits (default 1): ").strip()
    days = int(days_input) if days_input else 1
    since_date = datetime.now() - timedelta(days=days)

    projects = get_projects(group)
    if not projects:
        print("❌ No projects found.")
        return

    print(f"\n🔍 GitLab Commit Summary (Last {days} day(s)):")
    for project in projects:
        project_name = project['name']
        project_id = project['id']
        commits = get_commits_for_project(project_id, since_date)
        print(f"\n📁 {project_name}")
        if not commits:
            print(f"   ⚠️ No recent commits in the last {days} day(s).")
            continue
        author_commits = {}
        for commit in commits:
            author = commit['author_name']
            author_commits.setdefault(author, []).append(commit)
        for author, commit_list in author_commits.items():
            print(f"  👤 {author}: {len(commit_list)} commit(s)")
            for commit in commit_list:
                msg = commit['title']
                date = commit['created_at']
                summary = summarize_commit(msg)
                print(f"     - [{date[:10]}] {summary}")