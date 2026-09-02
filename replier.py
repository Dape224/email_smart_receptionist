import os, smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
from dotenv import load_dotenv

load_dotenv()
EMAIL = os.getenv("EMAIL")
APP_PASSWORD = os.getenv("EMAIL_APP_PASSWORD", "").replace(" ", "")

def send_reply(to_email: str, subject: str, body: str, original_message_id: str = None):
    """Send a reply that threads into the sender's original conversation."""
    msg = MIMEText(body)
    msg["From"] = formataddr(("Oladapo", EMAIL))
    msg["To"] = to_email
    msg["Subject"] = subject if subject.lower().startswith("re:") else f"Re: {subject}"

    if original_message_id:
        msg["In-Reply-To"] = original_message_id
        msg["References"] = original_message_id

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(EMAIL, APP_PASSWORD)
        server.sendmail(EMAIL, [to_email], msg.as_string())
    print(f"📨 Reply sent to {to_email}")