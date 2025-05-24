import yaml
from gitlab_fetcher import fetch_issues
from categorizer import categorize_tasks
from formatter import generate_summary
from notifier import send_email

# Load config
with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

# Fetch and process
try:
    all_tasks = fetch_issues(config)
    categorized = categorize_tasks(all_tasks)
    summary = generate_summary(categorized)

    # Deliver
    send_email(summary, config)

except Exception as e:
    print("🚨 Error during execution:", str(e))