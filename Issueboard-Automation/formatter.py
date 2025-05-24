def generate_summary(categorized):
    summary = """<html>
<head>
    <style>
        body { font-family: Arial, sans-serif; }
        h1 { color: #333; }
        table { border-collapse: collapse; width: 100%; margin-bottom: 20px; }
        th, td { border: 1px solid #ccc; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; }
        tr:nth-child(even) { background-color: #f9f9f9; }
        a { color: #0066cc; text-decoration: none; }
        .yesterday { background-color: #e6f7ff; }
        .today { background-color: #fffbe6; }
        .blockers { background-color: #ffe5e5; }
    </style>
</head>
<body>
<h1>📅 Daily Standup Summary</h1>"""

    for name, tasks in categorized.items():
        summary += f"<h2>👤 {name}</h2>\n"

        if not any(tasks.values()):
            summary += "<p>No tasks found for this user.</p>"
            continue

        summary += "<table><tr><th>Category</th><th>Task Title</th><th>Project</th><th>Status</th></tr>"

        if tasks['yesterday']:
            for task in tasks['yesterday']:
                summary += f"<tr class='yesterday'><td>✅ Yesterday</td><td><a href='{task['web_url']}'>{task['title']}</a></td><td>{task['project']}</td><td>Closed</td></tr>"

        if tasks['today']:
            for task in tasks['today']:
                summary += f"<tr class='today'><td>🚀 Today</td><td><a href='{task['web_url']}'>{task['title']}</a></td><td>{task['project']}</td><td>Open</td></tr>"

        if tasks.get('blockers'):
            for task in tasks['blockers']:
                summary += f"<tr class='blockers'><td>⚠️ Blocker</td><td><a href='{task['web_url']}'>{task['title']}</a></td><td>{task['project']}</td><td>Open</td></tr>"

        summary += "</table>"

    summary += """
</body>
</html>"""
    return summary