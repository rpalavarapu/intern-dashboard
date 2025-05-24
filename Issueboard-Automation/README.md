
# 📦 Automate Standups with GitLab Issue Boards

This Python-based automation script fetches tasks from GitLab for a given team/project, categorizes them by status (yesterday’s completed tasks, today’s open tasks, and blockers), and sends a clean HTML-formatted email summary.

---

## 🧩 Overview

| Feature | Description |
|--------|-------------|
| ✅ GitLab Integration | Fetches all issues from a specified GitLab project |
| 🗂️ Task Categorization | Sorts tasks into "Yesterday", "Today", and "Blockers" |
| 📨 Email Summary | Sends a formatted daily report via email |

---

## 📁 Project Structure

```
automate-the-standups-with-issue-boards/
├── config.yaml             # Configuration for GitLab and Email
├── main.py                 # Main script that runs the pipeline
├── gitlab_fetcher.py       # Fetches GitLab issues
├── categorizer.py          # Categorizes tasks
├── formatter.py            # Formats the summary as HTML
├── notifier.py             # Sends the summary via email
├── requirements.txt        # Required Python packages
└── README.md               # This file
```

---

## 🔧 Setup Instructions

### 1. Create a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

> Make sure `requirements.txt` includes:
```
python-gitlab
pyyaml
email.mime
```

### 3. Configure `config.yaml`

Update the following fields:

```yaml
gitlab:
  url: "https://code.swecha.org"
  private_token: "your-gitlab-private-token"
  project_ids: [17357]  # Replace with your actual project ID(s)

email:
  smtp_server: "smtp.gmail.com"
  smtp_port: 587
  sender_email: "your-email@gmail.com"
  sender_password: "your-app-password"  # Use a Gmail App Password if using 2FA
  recipient_email: "recipient@example.com"
```

> ⚠️ If you're using Gmail with 2FA, use a [Gmail App Password](https://myaccount.google.com/apppasswords).

---

## 🚀 How It Works

### 1. **Fetch Issues from GitLab**

The script connects to GitLab using the provided URL and private token. It retrieves all issues assigned to users in the configured project(s) and stores task details like title, status, labels, and web URL.

---

### 2. **Categorize Tasks**

Tasks are sorted into three categories:

- ✅ **Yesterday**: Closed tasks
- 🚀 **Today**: Open tasks
- ⚠️ **Blockers**: Tasks labeled as "blocked"

---

### 3. **Format as HTML Table**

A clean HTML table is generated for each team member, including:

| Category | Task Title | Project | Status |
|----------|------------|---------|--------|
| ✅ Yesterday | [Task Name](url) | Project X | Closed |
| 🚀 Today | [Task Name](url) | Project Y | Open |
| ⚠️ Blocker | [Task Name](url) | Project Z | Open |

---

### 4. **Send Email**

The HTML-formatted summary is sent via email using the SMTP server configuration in `config.yaml`.

---

## 📬 Example Email Output

![Example Email Screenshot](https://via.placeholder.com/600x300.png?text=Daily+Standup+Summary)

---

## 🛠️ Run the Script

To run the automation manually:

```bash
python main.py
```

You should receive an email with the daily standup summary.

---

## 🧪 Testing the Email Manually

If you want to test whether the email is working, try this small script:

```python
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_test_email():
    msg = MIMEMultipart('alternative')
    msg['Subject'] = 'Test Email'
    msg['From'] = 'your-email@gmail.com'
    msg['To'] = 'recipient@example.com'

    html = """<html><body><h1>Hello!</h1><p>This is a test email.</p></body></html>"""
    msg.attach(MIMEText(html, 'html'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('your-email@gmail.com', 'your-app-password')
    server.sendmail('your-email@gmail.com', ['recipient@example.com'], msg.as_string())
    server.quit()

send_test_email()
```

---

## 📝 Notes

- Make sure your GitLab token has access to the projects you're querying.
- Always store sensitive information like API tokens and passwords securely (e.g., in environment variables or encrypted files).
- You can schedule this script to run daily using a cron job or Task Scheduler.

---

## 🚀 Next Steps

- Add support for multiple teams/projects
- Export report to PDF or Markdown
- Add Slack integration for real-time updates

---