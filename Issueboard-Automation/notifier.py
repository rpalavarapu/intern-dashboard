import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(summary, config):
    email_config = config['email']

    # Create message container
    msg = MIMEMultipart('alternative')
    msg['Subject'] = '📅 Daily Standup Summary'
    msg['From'] = email_config['sender_email']
    msg['To'] = email_config['recipient_email']

    # Attach HTML content
    html_part = MIMEText(summary, 'html')
    msg.attach(html_part)

    try:
        server = smtplib.SMTP(email_config['smtp_server'], email_config['smtp_port'])
        server.starttls()
        server.login(email_config['sender_email'], email_config['sender_password'])
        server.sendmail(
            email_config['sender_email'],
            [email_config['recipient_email']],
            msg.as_string()
        )
        server.quit()
        print("✅ Email sent successfully.")
        return True
    except Exception as e:
        print("❌ Failed to send email:", str(e))
        return False