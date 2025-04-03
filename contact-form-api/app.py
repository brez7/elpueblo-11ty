from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
from email.message import EmailMessage

app = Flask(__name__)
CORS(app, origins="*", methods=["GET", "POST", "OPTIONS"])

# Your Gmail credentials
GMAIL_USER = "it@elpueblomex.com"
GMAIL_PASSWORD = "tywz qiut zlzq yndx"  # Use the app password you just created


def send_email(name, email, message):
    msg = EmailMessage()
    msg["Subject"] = f"New Contact Form Submission from {name}"
    msg["From"] = GMAIL_USER
    msg["To"] = GMAIL_USER  # Or use another address if you want

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

    send_email(name, email, message)

    return jsonify({"status": "success", "message": "Thanks! Your message was sent."})


@app.route("/", methods=["POST", "OPTIONS"])
def root_post():
    if request.method == "OPTIONS":
        return "", 204

    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    message = data.get("message")

    send_email(name, email, message)

    return jsonify({"status": "success", "message": "Thanks! Your message was sent."})
