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

def get_user_activities(user_id, since_date):
    """Fetch user activities from their profile"""
    activities = []
    page = 1
    per_page = 100
    
    while True:
        url = f"{GITLAB_URL}/api/v4/users/{user_id}/events"
        params = {
            'after': since_date.strftime('%Y-%m-%d'),
            'per_page': per_page,
            'page': page
        }
        response = make_api_request(url, headers, params=params)
        if not response:
            break
        activities.extend(response)
        if len(response) < per_page:
            break
        page += 1
    
    return activities

def get_user_merge_requests(user_id, since_date):
    """Get merge requests created by a specific user - DEBUG VERSION"""
    states = ['opened', 'merged', 'closed']
    all_mrs = []
    
    print(f"    🔍 Searching MRs for user ID {user_id} since {since_date}")
    
    for state in states:
        url = f"{GITLAB_URL}/api/v4/merge_requests"
        params = {
            'state': state,
            'author_id': user_id,
            'created_after': since_date.isoformat(),
            'per_page': 100
        }
        
        print(f"    📡 API Call: {url}")
        print(f"    📋 Params: {params}")
        
        mrs = make_api_request(url, headers, params=params)
        
        if mrs:
            print(f"    ✅ Found {len(mrs)} {state} MRs")
            all_mrs.extend(mrs)
        else:
            print(f"    ❌ No {state} MRs found")
    
    print(f"    🏁 Total MRs for user {user_id}: {len(all_mrs)}")
    return all_mrs

def get_project_name_by_id(project_id):
    """Get project name by project ID"""
    url = f"{GITLAB_URL}/api/v4/projects/{project_id}"
    response = make_api_request(url, headers)
    if response:
        return response.get('name', f'Project-{project_id}')
    return f'Project-{project_id}'

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
name_to_id = {m["name"]: m["id"] for m in members}

# ✅ Initialize user_stats with ALL group members
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

def process_user_activities(member):
    """Process activities for a single user - ENHANCED DEBUG VERSION"""
    user_name = member["name"]
    user_id = member["id"]
    
    print(f"🔍 Processing user: {user_name} (ID: {user_id})")
    
    stats = {
        "commits": 0,
        "merge_requests": 0,
        "issues": 0,
        "project_names": set(),
        "last_activity": None,
    }
    
    try:
        # Debug: Check user MRs first
        print(f"  📝 Fetching MRs for {user_name}...")
        user_mrs = get_user_merge_requests(user_id, since_date)
        print(f"  📊 Found {len(user_mrs) if user_mrs else 0} MRs for {user_name}")
        
        if user_mrs:
            stats["merge_requests"] = len(user_mrs)
            print(f"  ✅ {user_name}: {len(user_mrs)} MRs")
            
            # Debug project names from MRs
            for i, mr in enumerate(user_mrs):
                print(f"    📋 MR {i+1}:")
                print(f"       Title: {mr.get('title', 'No title')[:50]}...")
                print(f"       Created: {mr.get('created_at', 'No date')}")
                print(f"       State: {mr.get('state', 'No state')}")
                
                # Check different ways project info might be stored
                project_name = None
                
                # Method 1: Direct project object
                if 'project' in mr and mr['project']:
                    project_name = mr['project'].get('name')
                    print(f"       Project (method 1): {project_name}")
                
                # Method 2: project_id field
                elif 'project_id' in mr:
                    project_id = mr['project_id']
                    project_name = get_project_name_by_id(project_id)
                    print(f"       Project (method 2): {project_name} (ID: {project_id})")
                
                # Method 3: web_url parsing
                elif 'web_url' in mr:
                    web_url = mr['web_url']
                    # Extract project name from URL like: https://code.swecha.org/group/project/-/merge_requests/1
                    try:
                        url_parts = web_url.split('/')
                        if len(url_parts) >= 5:
                            project_name = url_parts[4]  # Assuming format: host/group/project/...
                            print(f"       Project (method 3): {project_name} (from URL)")
                    except:
                        pass
                
                if project_name:
                    stats["project_names"].add(project_name)
                    print(f"       ✅ Added project: {project_name}")
                else:
                    print(f"       ❌ Could not determine project name")
                    print(f"       MR keys: {list(mr.keys())}")
        else:
            print(f"  ❌ No MRs found for {user_name}")
        
        # Get user activities from profile
        print(f"  🔄 Fetching activities for {user_name}...")
        activities = get_user_activities(user_id, since_date)
        print(f"  📊 Found {len(activities) if activities else 0} activities for {user_name}")
        
        if activities:
            commit_count = 0
            for activity in activities:
                activity_date = None
                if activity.get('created_at'):
                    activity_date = parse_datetime(activity['created_at'])
                    if not stats["last_activity"] or activity_date > stats["last_activity"]:
                        stats["last_activity"] = activity_date
                
                # Count different types of activities
                action_name = activity.get('action_name', '')
                target_type = activity.get('target_type', '')
                
                if action_name == 'pushed to' or target_type == 'PushEvent':
                    commit_count += 1
                    
                    # Get project name from activity
                    project_name = None
                    if activity.get('project'):
                        project_name = activity['project'].get('name')
                    elif activity.get('project_id'):
                        project_name = get_project_name_by_id(activity['project_id'])
                    
                    if project_name:
                        stats["project_names"].add(project_name)
                        print(f"    ✅ Added project from activity: {project_name}")
            
            stats["commits"] = commit_count
            print(f"  ✅ {user_name}: {commit_count} commits from activities")
        
        # Update last activity with MR dates
        for mr in user_mrs or []:
            mr_date = None
            if mr.get('created_at'):
                mr_date = parse_datetime(mr['created_at'])
                if not stats["last_activity"] or mr_date > stats["last_activity"]:
                    stats["last_activity"] = mr_date
        
        print(f"  🏁 Final stats for {user_name}: {stats['commits']} commits, {stats['merge_requests']} MRs")
        print(f"  📁 Projects: {list(stats['project_names'])}")
        
    except Exception as e:
        print(f"  ❌ Error processing user activities for {user_name}: {e}")
        import traceback
        traceback.print_exc()
    
    return user_name, stats

def process_project_for_issues(project):
    """Process issues for a project (keeping existing logic)"""
    stats = defaultdict(lambda: {
        "issues": 0,
        "project_names": set(),
        "last_activity": None,
    })
    
    project_id = project["id"]
    project_name = project["name"]

    try:
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
        print(f"Error processing issues for project {project_name}: {e}")

    return stats

# Process user activities for commits and merge requests
st.info("🔄 Processing user activities...")
with ThreadPoolExecutor(max_workers=4) as executor:  # Reduced workers to avoid rate limiting
    futures = {executor.submit(process_user_activities, member): member for member in members}
    total_users = len(members)
    
    for i, future in enumerate(as_completed(futures)):
        user_name, stats = future.result()
        if user_name in user_stats:
            user_stats[user_name]["commits"] = stats["commits"]
            user_stats[user_name]["merge_requests"] = stats["merge_requests"]
            user_stats[user_name]["project_names"].update(stats["project_names"])
            if stats["last_activity"]:
                current = user_stats[user_name]["last_activity"]
                if not current or stats["last_activity"] > current:
                    user_stats[user_name]["last_activity"] = stats["last_activity"]
        progress.progress((i + 1) / total_users * 0.7)  # 70% for user activities

# Process projects for issues (keeping existing logic)
st.info("🔄 Processing project issues...")
with ThreadPoolExecutor(max_workers=4) as executor:  # Reduced workers
    futures = {executor.submit(process_project_for_issues, proj): proj for proj in projects}
    total_projects = len(projects)
    
    for i, future in enumerate(as_completed(futures)):
        result = future.result()
        for user, stats in result.items():
            if user in user_stats:
                user_stats[user]["issues"] += stats["issues"]
                user_stats[user]["project_names"].update(stats["project_names"])
                if stats["last_activity"]:
                    current = user_stats[user]["last_activity"]
                    if not current or stats["last_activity"] > current:
                        user_stats[user]["last_activity"] = stats["last_activity"]
        progress.progress(0.7 + (i + 1) / total_projects * 0.3)  # 30% for issues

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
            "Projects": ", ".join(stats["project_names"]) if stats["project_names"] else "No activity",
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
        with ThreadPoolExecutor(max_workers=4) as executor:  # Reduced workers
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
                    statuses[user] = "❓"
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

    with ThreadPoolExecutor(max_workers=4) as executor:  # Reduced workers
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