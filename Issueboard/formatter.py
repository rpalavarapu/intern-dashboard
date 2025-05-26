# formatter.py
from datetime import datetime

def generate_summary(categorized):
    """Generate HTML summary for standup"""
    current_date = datetime.now().strftime("%B %d, %Y")
    
    summary = f"""<html>
<head>
    <style>
        body {{ 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            line-height: 1.6;
            margin: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1 {{ 
            color: #2c3e50; 
            text-align: center;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }}
        h2 {{ 
            color: #34495e; 
            border-left: 4px solid #3498db;
            padding-left: 15px;
            margin-top: 30px;
        }}
        table {{ 
            border-collapse: collapse; 
            width: 100%; 
            margin-bottom: 20px;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }}
        th, td {{ 
            border: 1px solid #ddd; 
            padding: 12px; 
            text-align: left; 
        }}
        th {{ 
            background-color: #3498db; 
            color: white;
            font-weight: bold;
        }}
        tr:nth-child(even) {{ background-color: #f8f9fa; }}
        tr:hover {{ background-color: #e3f2fd; }}
        a {{ 
            color: #2980b9; 
            text-decoration: none;
            font-weight: 500;
        }}
        a:hover {{ text-decoration: underline; }}
        .yesterday {{ background-color: #d5f4e6; }}
        .today {{ background-color: #fff3cd; }}
        .blockers {{ background-color: #f8d7da; }}
        .no-tasks {{ 
            text-align: center; 
            color: #6c757d; 
            font-style: italic;
            padding: 20px;
            background-color: #f8f9fa;
            border-radius: 5px;
        }}
        .labels {{
            display: inline-block;
            background-color: #6c757d;
            color: white;
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 0.8em;
            margin: 2px;
        }}
        .status {{
            font-weight: bold;
            text-transform: capitalize;
        }}
        .notes {{
            font-size: 0.9em;
            color: #6c757d;
            max-width: 300px;
        }}
        .ai-summary {{
            background-color: #e8f4fd;
            border-left: 3px solid #007bff;
            padding: 16px 20px;
            margin: 8px 0;
            border-radius: 4px;
            font-size: 0.9em;
            line-height: 1.4;
            white-space: pre-wrap;
        }}
        .ai-summary strong {{
            color: #007bff;
        }}
    </style>
</head>
<body>
<div class="container">
<h1>📅 Daily Standup Summary - {current_date}</h1>"""

    for name, tasks in categorized.items():
        summary += f"<h2>👤 {name}</h2>\n"
        
        # Check if user has any tasks
        total_tasks = len(tasks.get('yesterday', [])) + len(tasks.get('today', [])) + len(tasks.get('blockers', []))
        
        if total_tasks == 0:
            summary += "<div class='no-tasks'>No tasks found for this user.</div>"
            continue
        
        summary += "<table><tr><th>Category</th><th>Task Title</th><th>Project</th><th>Status</th><th>Labels</th><th>Recent Notes</th></tr>"
        
        # Yesterday's completed tasks
        if tasks['yesterday']:
            for task in tasks['yesterday']:
                labels_html = ''.join([f"<span class='labels'>{label}</span>" for label in task.get('labels', [])])
                
                # Recent notes
                notes_html = ""
                if task.get('notes'):
                    latest_note = task['notes'][-1] if task['notes'] else None
                    if latest_note:
                        notes_html = f"<div class='notes'><strong>{latest_note['author']}:</strong> {latest_note['body']}</div>"
                
                summary += f"""<tr class='yesterday'>
                    <td>✅ Yesterday</td>
                    <td><a href='{task['web_url']}'>{task['title']}</a></td>
                    <td>{task['project']}</td>
                    <td><span class='status'>{task['status']}</span></td>
                    <td>{labels_html}</td>
                    <td>{notes_html}</td>
                </tr>"""
                
                # Add AI summary in a separate row
                ai_summary = task.get('ai_summary', '')
                if ai_summary:
                    summary += f"""<tr class='yesterday' style='background-color: transparent;'>
                        <td colspan='6' class='ai-summary'>
                            <strong>📋 Summary:</strong> {ai_summary}
                        </td>
                    </tr>"""
        
        # Today's active tasks
        if tasks['today']:
            for task in tasks['today']:
                labels_html = ''.join([f"<span class='labels'>{label}</span>" for label in task.get('labels', [])])
                
                # Recent notes
                notes_html = ""
                if task.get('notes'):
                    latest_note = task['notes'][-1] if task['notes'] else None
                    if latest_note:
                        notes_html = f"<div class='notes'><strong>{latest_note['author']}:</strong> {latest_note['body']}</div>"
                
                summary += f"""<tr class='today'>
                    <td>🚀 Today</td>
                    <td><a href='{task['web_url']}'>{task['title']}</a></td>
                    <td>{task['project']}</td>
                    <td><span class='status'>{task['status']}</span></td>
                    <td>{labels_html}</td>
                    <td>{notes_html}</td>
                </tr>"""
                
                # Add AI summary in a separate row
                ai_summary = task.get('ai_summary', '')
                if ai_summary:
                    summary += f"""<tr class='today' style='background-color: transparent;'>
                        <td colspan='6' class='ai-summary'>
                            <strong>📋 Summary:</strong> {ai_summary}
                        </td>
                    </tr>"""
        
        # Blockers
        if tasks.get('blockers'):
            for task in tasks['blockers']:
                labels_html = ''.join([f"<span class='labels'>{label}</span>" for label in task.get('labels', [])])
                
                # Recent notes
                notes_html = ""
                if task.get('notes'):
                    latest_note = task['notes'][-1] if task['notes'] else None
                    if latest_note:
                        notes_html = f"<div class='notes'><strong>{latest_note['author']}:</strong> {latest_note['body']}</div>"
                
                summary += f"""<tr class='blockers'>
                    <td>⚠️ Blocker</td>
                    <td><a href='{task['web_url']}'>{task['title']}</a></td>
                    <td>{task['project']}</td>
                    <td><span class='status'>{task['status']}</span></td>
                    <td>{labels_html}</td>
                    <td>{notes_html}</td>
                </tr>"""
                
                # Add AI summary in a separate row
                ai_summary = task.get('ai_summary', '')
                if ai_summary:
                    summary += f"""<tr class='blockers' style='background-color: transparent;'>
                        <td colspan='6' class='ai-summary'>
                            <strong>📋 Summary:</strong> {ai_summary}
                        </td>
                    </tr>"""
        
        summary += "</table>"
    
    summary += """
</div>
</body>
</html>"""
    return summary