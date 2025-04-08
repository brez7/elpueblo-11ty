from flask import Flask, request, jsonify
import smtplib
from email.message import EmailMessage
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

app = Flask(__name__)

print("✅ Routes loaded at build time:")
print(app.url_map)

# Gmail credentials
GMAIL_USER = "it@elpueblomex.com"
GMAIL_PASSWORD = "tywz qiut zlzq yndx"

# Google Sheets setup
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SERVICE_ACCOUNT_FILE = "sheets-creds.json"

credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
gc = gspread.authorize(credentials)

SHEET_ID = "1s1bqJcfEY2d4bCXHqfowPnHsZ2-hvm1EldrNeydZumQ"
SHEET_NAME = "Sheet1"
worksheet = gc.open_by_key(SHEET_ID).worksheet(SHEET_NAME)


def send_email(name, email, message):
    msg = EmailMessage()
    msg["Subject"] = f"New Contact Form Submission from {name}"
    msg["From"] = GMAIL_USER
    msg["To"] = "rob@elpueblomex.com, rob@barbank.com"
    msg.set_content(f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}")

    confirmation = EmailMessage()
    confirmation["Subject"] = "We received your message!"
    confirmation["From"] = GMAIL_USER
    confirmation["To"] = email
    confirmation.set_content(
        f"Hi {name},\n\nThanks for reaching out to El Pueblo Mexican Food. We’ve received your message and will be in touch soon!\n\nYour message:\n{message}\n\n— El Pueblo Team"
    )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(GMAIL_USER, GMAIL_PASSWORD)
        smtp.send_message(msg)
        smtp.send_message(confirmation)


def _build_cors_preflight_response():
    response = jsonify({"message": "Preflight OK"})
    response.headers.add(
        "Access-Control-Allow-Origin", "https://restart-elpueblo.web.app"
    )
    response.headers.add("Access-Control-Allow-Headers", "Content-Type")
    response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
    return response


def _cors_response(data, status=200):
    response = jsonify(data)
    response.status_code = status
    response.headers.add(
        "Access-Control-Allow-Origin", "https://restart-elpueblo.web.app"
    )
    return response


@app.route("/submit", methods=["POST", "OPTIONS"])
def submit():
    if request.method == "OPTIONS":
        return _build_cors_preflight_response()

    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    message = data.get("message")

    send_email(name, email, message)

    try:
        worksheet.append_row([datetime.now().isoformat(), name, email, message])
    except Exception as e:
        print("❌ Google Sheets logging failed:", e)

    return _cors_response(
        {"status": "success", "message": "Thanks! Your message was sent."}
    )


@app.route("/", methods=["POST", "OPTIONS"])
def root_post():
    if request.method == "OPTIONS":
        return _build_cors_preflight_response()

    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    message = data.get("message")

    send_email(name, email, message)

    return _cors_response(
        {"status": "success", "message": "Thanks! Your message was sent."}
    )


@app.route("/reserve", methods=["POST", "OPTIONS"])
def reserve():
    if request.method == "OPTIONS":
        return _build_cors_preflight_response()

    try:
        data = request.get_json()
        required_fields = [
            "firstName",
            "lastName",
            "phone",
            "email",
            "location",
            "date",
            "time",
            "partySize",
            "eventType",
            "organization",
        ]
        missing = [field for field in required_fields if not data.get(field)]
        if missing:
            return _cors_response(
                {"error": f"Missing fields: {', '.join(missing)}"}, status=400
            )

        # Email body formatting
        msg_body = f"""
        New Party Reservation Request:

        Name: {data['firstName']} {data['lastName']}
        Phone: {data['phone']}
        Email: {data['email']}
        Location: {data['location']}
        Date: {data['date']}
        Time: {data['time']}
        Party Size: {data['partySize']}
        Type of Event: {data['eventType']}
        Organization: {data['organization']}
        Comments: {data.get('comments', 'N/A')}
        """

        # Send notification email
        msg = EmailMessage()
        msg.set_content(msg_body)
        msg["Subject"] = "New Party Reservation Request"
        msg["From"] = GMAIL_USER
        msg["To"] = ["rob@elpueblomex.com", "rob@barbank.com"]

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(GMAIL_USER, GMAIL_PASSWORD)
            smtp.send_message(msg)

        # ✅ Log to Sheet2
        try:
            sheet2 = gc.open_by_key(SHEET_ID).worksheet("Sheet2")
            sheet2.append_row(
                [
                    datetime.now().isoformat(),
                    data["firstName"],
                    data["lastName"],
                    data["phone"],
                    data["email"],
                    data["location"],
                    data["date"],
                    data["time"],
                    data["partySize"],
                    data["eventType"],
                    data["organization"],
                    data.get("comments", ""),
                ]
            )
            print(
                f"✅ Sheet2 logging successful for: {data['firstName']} {data['lastName']}"
            )
        except Exception as e:
            print("❌ Failed to log to Sheet2:", e)

        # Success response
        return _cors_response(
            {
                "message": "Reservation request submitted successfully! Our store manager will contact you to verify the details."
            }
        )

    except Exception as e:
        print("❌ Error processing reservation:", e)
        return _cors_response(
            {"error": "An error occurred while processing your reservation."},
            status=500,
        )


if __name__ == "__main__":
    app.run(debug=True, port=8080)
