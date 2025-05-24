import gitlab

def fetch_issues(config):
    gl = gitlab.Gitlab(url=config['gitlab']['url'], private_token=config['gitlab']['private_token'])
    all_tasks = {}

    for member in config['gitlab']['team_members']:
        user_id = member['id']
        try:
            # Fetch issues assigned to the user
            issues = gl.issues.list(assignee_id=user_id, all=True)

            all_tasks[member['name']] = []

            for issue in issues:
                # Get project name (since issue.project_id is just an int)
                try:
                    project = gl.projects.get(issue.project_id)
                    project_name = project.name
                except Exception:
                    project_name = f"Project {issue.project_id}"

                # Get notes/comments on the issue
                project_obj = gl.projects.get(issue.project_id)
                issue_obj = project_obj.issues.get(issue.iid)
                notes = issue_obj.notes.list(all=True)

                recent_notes = []
                for note in notes[-3:]:  # Last 3 comments
                    recent_notes.append({
                        'author': note.author['name'],
                        'body': note.body,
                        'created_at': note.created_at
                    })

                task = {
                    'title': issue.title,
                    'status': issue.state,
                    'labels': issue.labels,
                    'project': project_name,
                    'web_url': issue.web_url,
                    'notes': recent_notes
                }
                all_tasks[member['name']].append(task)
        except Exception as e:
            print(f"Error fetching issues for {member['name']}: {e}")
    return all_tasks