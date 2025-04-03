import smtplib
from email.message import EmailMessage

GMAIL_USER = "it@elpueblomex.com"
GMAIL_PASSWORD = "tywz qiut zlzq yndx"

msg = EmailMessage()
msg["Subject"] = "Test from Flask"
msg["From"] = GMAIL_USER
msg["To"] = GMAIL_USER
msg.set_content("This is a test email from your Flask backend.")

with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
    smtp.login(GMAIL_USER, GMAIL_PASSWORD)
    smtp.send_message(msg)

print("Email sent!")
