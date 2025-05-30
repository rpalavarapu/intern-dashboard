# apis/users_api.py
from utils.fetch import make_api_request
from utils.auth import get_gitlab_headers

GITLAB_URL = "https://code.swecha.org"

def get_user_id(username):
    url = f"{GITLAB_URL}/api/v4/users"
    params = {"username": username}
    response = make_api_request(url, get_gitlab_headers(), params=params)
    if response and isinstance(response, list) and len(response) > 0:
        return response[0]["id"]
    print(f"❌ User '{username}' not found.")
    return None

def run_users():
    print("\n👤 Get User Info")
    username = input("📥 Enter GitLab username: ").strip()
    user_id = get_user_id(username)
    if user_id:
        print(f"✅ User ID for '{username}': {user_id}")