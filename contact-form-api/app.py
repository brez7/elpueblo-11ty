from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
from email.message import EmailMessage
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

app = Flask(__name__)
CORS(app, origins="*", methods=["GET", "POST", "OPTIONS"])

# Gmail credentials (app password)
GMAIL_USER = "it@elpueblomex.com"
GMAIL_PASSWORD = "tywz qiut zlzq yndx"

# Google Sheets setup
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SERVICE_ACCOUNT_FILE = "sheets-creds.json"  # Your service account JSON

credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
gc = gspread.authorize(credentials)

SHEET_ID = "1s1bqJcfEY2d4bCXHqfowPnHsZ2-hvm1EldrNeydZumQ"
SHEET_NAME = "Sheet1"
worksheet = gc.open_by_key(SHEET_ID).worksheet(SHEET_NAME)


def send_email(name, email, message):
    msg = EmailMessage()
    msg["Subject"] = f"New Contact Form Submission from {name}"
    msg["From"] = GMAIL_USER
    msg["To"] = ", ".join(["rob@elpueblomex.com", "rob@barbank.com"])
    msg.set_content(f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(GMAIL_USER, GMAIL_PASSWORD)
        smtp.send_message(msg)


@app.route("/submit", methods=["POST", "OPTIONS"])
def submit():
    if request.method == "OPTIONS":
        return "", 204

    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    message = data.get("message")

    # Send the email
    send_email(name, email, message)

    # Log to Google Sheets
    try:
        worksheet.append_row([datetime.now().isoformat(), name, email, message])
    except Exception as e:
        print("❌ Google Sheets logging failed:", e)

    return jsonify({"status": "success", "message": "Thanks! Your message was sent."})


@app.route("/", methods=["POST", "OPTIONS"])
def root_post():
    if request.method == "OPTIONS":
        return "", 204

    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    message = data.get("message")

    # Send the email only (can also log here if needed)
    send_email(name, email, message)

    return jsonify({"status": "success", "message": "Thanks! Your message was sent."})


if __name__ == "__main__":
    app.run(debug=True, port=8080)
