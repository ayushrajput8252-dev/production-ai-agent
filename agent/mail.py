import smtplib
import json
from pathlib import Path
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

load_dotenv()

EMAIL_USER = (os.getenv("EMAIL_USER") or "").strip()
EMAIL_PASS = (os.getenv("EMAIL_PASS") or "").strip()
MAIL_MODE = (os.getenv("MAIL_MODE") or "smtp").strip().lower()
OUTBOX_PATH = Path(__file__).resolve().parent / "mail_outbox.jsonl"


def _queue_local_mail(to_email, subject, body, reason):
    record = {
        "to": to_email,
        "subject": subject,
        "body": body,
        "reason": reason,
    }
    with open(OUTBOX_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=True) + "\n")


def send_mail(to_email, subject, body):
    if MAIL_MODE == "local":
        _queue_local_mail(to_email, subject, body, "MAIL_MODE=local")
        return True, "queued locally"

    if not EMAIL_USER or not EMAIL_PASS:
        _queue_local_mail(to_email, subject, body, "missing credentials")
        return True, "queued locally (missing credentials)"

    msg = MIMEMultipart()
    msg["From"] = EMAIL_USER
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587, timeout=20)
        server.starttls()
        # Gmail app passwords are sometimes copied with spaces; normalize safely.
        normalized_pass = EMAIL_PASS.replace(" ", "")
        server.login(EMAIL_USER, normalized_pass)
        server.send_message(msg)
        server.quit()
        print(f"Mail sent to {to_email}")
        return True, ""
    except Exception as exc:
        _queue_local_mail(to_email, subject, body, f"smtp_failed: {exc}")
        return True, "queued locally (smtp failed)"