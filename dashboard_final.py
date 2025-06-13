import streamlit as st
from datetime import datetime, timedelta
from collections import defaultdict
import pandas as pd
import altair as alt
from dateutil.parser import parse as parse_datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

from apis.projects_api import get_projects
from apis.commits_api import get_commits_for_project
from apis.merge_api import get_merge_requests
from apis.issues_api import fetch_all_project_issues
from apis.users_api import get_group_members, get_user_details
from utils.auth import get_gitlab_headers
from Issueboard.issueboard_automation import parse_gitlab_date
from utils.fetch import make_api_request
from apis.groups_api import get_all_users_from_group
from apis.readme_exists_api import check_readme_exists_api

groupID_1 = "69994"
GITLAB_URL = "https://code.swecha.org"

def get_all_accessible_projects():
    projects = []
    page = 1
    per_page = 100
    while True:
        url = f"{GITLAB_URL}/api/v4/projects?membership=true&simple=true&per_page={per_page}&page={page}"
        response = make_api_request(url, headers)
        if not response:
            break
        projects.extend(response)
        if len(response) < per_page:
            break
        page += 1
    return projects

st.set_page_config(layout="wide")
st.title("📊 BITS Pilani Internship | GitLab Contributions Dashboard")

days = st.slider("🗖️ Days to look back", 1, 60, 7)
since_date = datetime.now() - timedelta(days=days)
headers = get_gitlab_headers()

@st.cache_data(show_spinner=False)
def load_projects():
    return get_all_accessible_projects()

projects = load_projects()

if not projects:
    st.error("❌ No projects found or API error.")
    st.stop()

# ✅ Load group 69994 members and build valid name set
members = get_all_users_from_group(groupID_1)
valid_names = {m["name"] for m in members}

# ✅ Initialize user_stats with ALL group members (this is the key change)
user_stats = {}
for member in members:
    user_stats[member["name"]] = {
        "commits": 0,
        "merge_requests": 0,
        "issues": 0,
        "project_names": set(),
        "last_activity": None,
    }

progress = st.progress(0)

def process_project(project):
    stats = defaultdict(lambda: {
        "commits": 0,
        "merge_requests": 0,
        "issues": 0,
        "project_names": set(),
        "last_activity": None,
    })
    project_id = project["id"]
    project_name = project["name"]

    try:
        commits = get_commits_for_project(project_id, since_date)
        for c in commits or []:
            author = c.get("author_name", "Unknown")
            if author not in valid_names:
                continue
            date_str = c.get("created_at")
            if date_str:
                dt = parse_datetime(date_str)
                current = stats[author]["last_activity"]
                if not current or dt > current:
                    stats[author]["last_activity"] = dt
            stats[author]["commits"] += 1
            stats[author]["project_names"].add(project_name)

        mrs = get_merge_requests(project_id)
        for mr in mrs or []:
            updated_at = parse_gitlab_date(mr.get("updated_at"))
            author = mr.get("author", {}).get("name", "Unknown")
            if author not in valid_names:
                continue
            if updated_at and updated_at >= since_date:
                current = stats[author]["last_activity"]
                if not current or updated_at > current:
                    stats[author]["last_activity"] = updated_at
                stats[author]["merge_requests"] += 1
                stats[author]["project_names"].add(project_name)

        issues = fetch_all_project_issues(headers, project_id, since_date.isoformat())
        for issue in issues or []:
            author = issue.get("author", {}).get("name", "Unknown")
            if author not in valid_names:
                continue
            date_str = issue.get("created_at")
            if date_str:
                dt = parse_datetime(date_str)
                current = stats[author]["last_activity"]
                if not current or dt > current:
                    stats[author]["last_activity"] = dt
            stats[author]["issues"] += 1
            stats[author]["project_names"].add(project_name)

    except Exception as e:
        print(f"Error processing project {project_name}: {e}")

    return stats

with ThreadPoolExecutor(max_workers=8) as executor:
    futures = {executor.submit(process_project, proj): proj for proj in projects}
    total = len(projects)
    for i, future in enumerate(as_completed(futures)):
        result = future.result()
        for user, stats in result.items():
            if user not in valid_names:
                continue
            # ✅ Now we're guaranteed that user exists in user_stats
            user_data = user_stats[user]
            user_data["commits"] += stats["commits"]
            user_data["merge_requests"] += stats["merge_requests"]
            user_data["issues"] += stats["issues"]
            user_data["project_names"].update(stats["project_names"])
            if not user_data["last_activity"] or (stats["last_activity"] and stats["last_activity"] > user_data["last_activity"]):
                user_data["last_activity"] = stats["last_activity"]
        progress.progress((i + 1) / total)

progress.empty()

# Display Summary Table
if not user_stats:
    st.warning("No users found in the group.")
else:
    # ✅ Show total number of members in the group
    st.subheader(f"🧑‍💼 All {len(user_stats)} members from group 69994")

    df = pd.DataFrame([
        {
            "User": user,
            "Commits": stats["commits"],
            "MRs": stats["merge_requests"],
            "Issues": stats["issues"],
            "Projects": ", ".join(stats["project_names"]) if stats["project_names"] else "None",
            "Last Activity": stats["last_activity"].strftime("%Y-%m-%d %H:%M:%S") if stats["last_activity"] else "No activity"
        }
        for user, stats in user_stats.items()
    ])

    df["User"] = df["User"].astype(str)

    # README status check
    name_to_username = {m["name"]: m["username"] for m in members}
    name_to_username.update({
        "amar": "awmar",
        "Prem-Kowshik": "premk",
        "Phanindra Varma": "phanindra_varma",
        "sailadachetansurya": "ChetanSurya",
    })

    def fetch_readme_status(users, name_to_username):
        statuses = {}
        with ThreadPoolExecutor(max_workers=8) as executor:
            futures = {}
            for user in users:
                username = name_to_username.get(user)
                if username:
                    futures[executor.submit(check_readme_exists_api, username)] = user
                else:
                    statuses[user] = "❌ (username not found)"
            for future in as_completed(futures):
                user = futures[future]
                try:
                    result = future.result()
                    statuses[user] = "✅" if result else "❌"
                except Exception:
                    statuses[user] = "error"
        return statuses

    usernames = df["User"].tolist()
    readme_status_map = fetch_readme_status(usernames, name_to_username)
    df["README"] = df["User"].map(readme_status_map)

    # ✅ Sort by activity first (active users first), then by name for inactive users
    df_sorted = df.sort_values(
        ["Last Activity", "User"], 
        ascending=[False, True],
        na_position='last'
    )
    
    st.dataframe(df_sorted, use_container_width=True)

    # ✅ Show statistics
    active_users = len([u for u in user_stats.values() if u["commits"] > 0 or u["merge_requests"] > 0 or u["issues"] > 0])
    inactive_users = len(user_stats) - active_users
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("👥 Total Members", len(user_stats))
    with col2:
        st.metric("✅ Active Members", active_users)
    with col3:
        st.metric("😴 Inactive Members", inactive_users)

    st.subheader("🔎 Per-User Details")
    for user, stats in sorted(user_stats.items()):
        total_activity = stats['commits'] + stats['merge_requests'] + stats['issues']
        activity_label = f"{total_activity} total activities" if total_activity > 0 else "No activity"
        
        with st.expander(f"👤 {user} | {stats['commits']} commits, {stats['merge_requests']} MRs, {stats['issues']} issues ({activity_label})"):
            if stats['project_names']:
                st.markdown(f"**Projects:** {', '.join(stats['project_names'])}")
            else:
                st.markdown("**Projects:** No project activity in the selected time period")

# Active Users (Optional)
def fetch_online_users(minutes=10):
    st.info(f"⏳ Checking users active in last {minutes} minutes...")
    members = get_group_members(groupID_1)
    online_users = []
    now = datetime.utcnow()
    delta = timedelta(minutes=minutes)

    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = {executor.submit(get_user_details, member["id"]): member for member in members}
        for future in as_completed(futures):
            user_detail = future.result()
            if not user_detail:
                continue

            last_sign_in_at = user_detail.get("last_sign_in_at")
            last_active_dt = None

            if last_sign_in_at:
                try:
                    last_active_dt = datetime.fromisoformat(last_sign_in_at.rstrip("Z"))
                except Exception:
                    pass

            if last_active_dt and (now - last_active_dt) <= delta:
                online_users.append({
                    "name": user_detail.get("name"),
                    "username": user_detail.get("username"),
                    "last_sign_in_at": last_sign_in_at
                })

    return online_users

st.subheader("🟢 Users Active Recently (approximate online)")
try:
    online_users = fetch_online_users(minutes=10)
    if not online_users:
        st.write("No users active in the last 10 minutes.")
    else:
        online_df = pd.DataFrame(online_users)
        st.dataframe(online_df, use_container_width=True)
except Exception as e:
    st.error(f"Failed to fetch online users: {e}")