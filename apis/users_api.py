import requests

GITLAB_URL = "https://code.swecha.org"

def get_user_id(headers, username):
    user_response = requests.get(
        f"{GITLAB_URL}/api/v4/users", headers=headers, params={"username": username}
    )
    if not user_response.ok or not user_response.json():
        print(f"User: '{username}' not found.")
        return None

    user_id = user_response.json()[0]["id"]
    return user_id