# apis/groups_api.py
from utils.fetch import make_api_request
from utils.auth import get_gitlab_headers
from urllib.parse import quote
import csv
from apis.users_api import get_user_id




GITLAB_URL = "https://code.swecha.org"

def get_all_users_from_group(group_id):
    url_base = f"{GITLAB_URL}/api/v4/groups/{group_id}/members/all"
    return make_api_request(url_base, get_gitlab_headers())

def add_members_to_group(group_id, filename, access_level=30):
    with open(filename, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            username = row["username"].strip()
            user_id = get_user_id(username)
            if not user_id:
                continue
            url = f"{GITLAB_URL}/api/v4/groups/{group_id}/members"
            data = {"user_id": user_id, "access_level": access_level}
            response = make_api_request(url, get_gitlab_headers(), data=data)
            if response:
                print(f"✅ Added '{username}' to the group.")

def update_access_level(group_id, filename, level):
    with open(filename, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            username = row["username"].strip()
            user_id = get_user_id(username)
            if not user_id:
                continue
            url = f"{GITLAB_URL}/api/v4/groups/{group_id}/members/{user_id}"
            data = {"access_level": level}
            response = make_api_request(url, get_gitlab_headers(), data=data)
            if response:
                print(f"🔄 Updated access level for '{username}'")

def run_groups():
    print("\n👥 Manage GitLab Groups")
    group_id= input("📥 Enter Group ID: ").strip()
    print("1. List Members")
    print("2. Add Members from CSV")
    print("3. Update Access Level")
    choice = input("Enter choice: ").strip()

    if choice == "1":
        members = get_all_users_from_group(group_id)
        if members:
            print(f"\n👥 Members in group {group_id}:")
            for member in members:
                print(f"- {member['name']} ({member['username']})")
        else:
            print("❌ No members found.")

    elif choice == "2":
        filename = input("📄 Enter CSV filename: ").strip()
        add_members_to_group(group_id, filename)
    
    elif choice == "3":
        filename = input("📄 Enter CSV filename: ").strip()
        level = int(input("🔒 Enter access level (e.g., 30 for Developer): "))
        update_access_level(group_id, filename, level)

    else:
        print("❌ Invalid choice.")