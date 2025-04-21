from flask import Flask, request, jsonify, redirect
from flask_cors import CORS
from email.message import EmailMessage
from datetime import datetime
import base64
import gspread
import json
import os
import re
import requests
import smtplib
import traceback

# Google Auth & APIs
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google.oauth2.service_account import Credentials as ServiceAccountCredentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
# ✨ Setup
app = Flask(__name__)
CORS(app)

GMAIL_USER = "it@elpueblomex.com"
GMAIL_PASSWORD = "tywz qiut zlzq yndx"

# 🔐 Google Sheets setup
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SERVICE_ACCOUNT_FILE = "sheets-creds.json"
credentials = ServiceAccountCredentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES
)

gc = gspread.authorize(credentials)
SHEET_ID = "1s1bqJcfEY2d4bCXHqfowPnHsZ2-hvm1EldrNeydZumQ"


# 📆 Utility: format date
def format_date(date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").strftime("%B %d, %Y")
    except:
        return date_str


# 🌐 CORS utilities
def _get_allowed_origin():
    allowed_origins = ["http://localhost:8080", "https://restart-elpueblo.web.app"]
    origin = request.headers.get("Origin")
    return origin if origin in allowed_origins else "null"


def _build_cors_preflight_response():
    res = jsonify({"message": "Preflight OK"})
    res.headers.add("Access-Control-Allow-Origin", _get_allowed_origin())
    res.headers.add("Access-Control-Allow-Headers", "Content-Type")
    res.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
    return res


def _cors_response(data, status=200):
    res = jsonify(data)
    res.status_code = status
    res.headers.add("Access-Control-Allow-Origin", _get_allowed_origin())
    res.headers.add("Access-Control-Allow-Headers", "Content-Type")
    res.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
    return res


# ✉️ Contact Form Email
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


# 🧑‍💼 Job Application Email with signature images
def send_job_application_email(data):
    name = data.get("fullName", "")
    email = data.get("email", "")

    msg = EmailMessage()
    msg["Subject"] = f"New Job Application from {name}"
    msg["From"] = GMAIL_USER
    msg["To"] = "rob@elpueblomex.com, rob@barbank.com"
    msg.set_content(f"New job application from {name}. View in HTML client.")

    html_body = f"""
    <html><body style="font-family: Arial, sans-serif; font-size: 15px;">
      <h2>📨 New Job Application</h2>
      <p><strong>Timestamp:</strong> {datetime.now().isoformat()}</p>
      <p><strong>Full Name:</strong> {name}<br>
      <strong>Email:</strong> {email}<br>
      <strong>Phone:</strong> {data.get("phone")}<br>
      <strong>DOB:</strong> {format_date(data.get("dob"))}<br>
      <strong>Address:</strong> {data.get("addressLine1")}, {data.get("addressLine2")}<br>
      <strong>City/State/Zip:</strong> {data.get("city")}, {data.get("state")} {data.get("postalCode")}<br>
      <strong>Other Names:</strong> {data.get("otherNames")}<br>
      <strong>Employed Before:</strong> {data.get("employedBefore")} ({data.get("employmentDates")})<br>
      <strong>Application Date:</strong> {format_date(data.get("applicationDate"))}<br>
      <strong>Referral:</strong> {data.get("referralSource")}<br>
      <strong>Position:</strong> {data.get("position")} at {data.get("location")}<br>
      <strong>Start Date:</strong> {format_date(data.get("availableDate"))}<br>
      <strong>Availability:</strong> {data.get("availability")}<br>
      <strong>Employment History:</strong> {data.get("employmentHistory")}<br>
      <strong>References:</strong> {data.get("references")}<br>
      <strong>Felony:</strong> {data.get("felony")} – {data.get("felonyExplanation")}<br>
      <strong>Perform Job Functions:</strong> {data.get("jobFunctions")}<br>
      <strong>Reliable Transportation:</strong> {data.get("transportation")}<br>
      <strong>Attendance:</strong> {data.get("attendance")}<br>
      <strong>Authorization to work in the US:</strong> {data.get("authorization")}<br>

      <p><strong>Initials & Signature:</strong></p>
      <p>1.<br><img src="cid:initial1" width="150" height="85" style="border:1px solid #ccc;"></p>
      <p>2.<br><img src="cid:initial2" width="150" height="85" style="border:1px solid #ccc;"></p>
      <p>3.<br><img src="cid:initial3" width="150" height="85" style="border:1px solid #ccc;"></p>
      <p><strong>Applicant Signature:</strong><br>
      <img src="cid:signature" width="400" height="150" style="border:1px solid #ccc;"></p>
      <p><strong>Print Name:</strong> {data.get("printName")}<br>
      <strong>Signature Date:</strong> {format_date(data.get("signatureDate"))}</p>
    </body></html>
    """
    msg.add_alternative(html_body, subtype="html")

    def attach_image(cid, data_url):
        if not data_url or not data_url.startswith("data:image"):
            return
        match = re.search(r"^data:image/\w+;base64,(.+)", data_url)

        if match:
            b64_data = match.group(1)
            img_data = base64.b64decode(b64_data)
            msg.get_payload()[1].add_related(
                img_data, maintype="image", subtype="png", cid=f"<{cid}>"
            )

    attach_image("initial1", data.get("initial1"))
    attach_image("initial2", data.get("initial2"))
    attach_image("initial3", data.get("initial3"))
    attach_image("signature", data.get("signature"))

    confirmation = EmailMessage()
    confirmation["Subject"] = "We received your job application!"
    confirmation["From"] = GMAIL_USER
    confirmation["To"] = email
    confirmation.set_content(
        f"Hi {name},\n\nThanks for applying! We’ll review it shortly.\n\n— El Pueblo Team"
    )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(GMAIL_USER, GMAIL_PASSWORD)
        smtp.send_message(msg)
        smtp.send_message(confirmation)


# 🔄 OAuth Flow for Google Business Profile
OAUTH_SCOPES = ["https://www.googleapis.com/auth/business.manage"]
CLIENT_SECRETS_FILE = "client_secret.json"
REDIRECT_URI = "http://127.0.0.1:5000/oauth2callback"


@app.route("/authorize")
def authorize():
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=OAUTH_SCOPES, redirect_uri=REDIRECT_URI
    )
    auth_url, _ = flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true",
        prompt="consent",
    )
    return redirect(auth_url)


@app.route("/oauth2callback")
def oauth2callback():
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=OAUTH_SCOPES, redirect_uri=REDIRECT_URI
    )

    flow.fetch_token(authorization_response=request.url)
    creds = flow.credentials

    # ✅ Properly save the token using the built-in serializer
    with open("token.json", "w") as token_file:
        token_file.write(creds.to_json())

    return "✅ Auth successful. You can close this tab."


def load_credentials():
    with open("token.json", "r") as f:
        token_data = json.load(f)

    creds = Credentials.from_authorized_user_info(token_data, SCOPES)

    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        # Save updated token
        with open("token.json", "w") as f:
            f.write(creds.to_json())

    return creds


# 📨 /submit
@app.route("/submit", methods=["POST", "OPTIONS"])
def submit():
    if request.method == "OPTIONS":
        return _build_cors_preflight_response()
    data = request.get_json()
    send_email(data.get("name"), data.get("email"), data.get("message"))
    try:
        worksheet = gc.open_by_key(SHEET_ID).worksheet("Sheet1")
        worksheet.append_row(
            [
                datetime.now().isoformat(),
                data.get("name"),
                data.get("email"),
                data.get("message"),
            ]
        )
    except Exception as e:
        print("❌ Google Sheets logging failed:", e)
    return _cors_response(
        {"status": "success", "message": "Thanks! Your message was sent."}
    )


# 📨 /
@app.route("/", methods=["POST", "OPTIONS"])
def root_post():
    if request.method == "OPTIONS":
        return _build_cors_preflight_response()
    data = request.get_json()
    send_email(data.get("name"), data.get("email"), data.get("message"))
    return _cors_response(
        {"status": "success", "message": "Thanks! Your message was sent."}
    )


# 🥳 /reserve
@app.route("/reserve", methods=["POST", "OPTIONS"])
def reserve():
    if request.method == "OPTIONS":
        return _build_cors_preflight_response()
    try:
        data = request.get_json()
        required = [
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
        missing = [f for f in required if not data.get(f)]
        if missing:
            return _cors_response(
                {"error": f"Missing fields: {', '.join(missing)}"}, status=400
            )

        msg_body = f"""
        New Reservation from {data['firstName']} {data['lastName']}
        Phone: {data['phone']}
        Email: {data['email']}
        Location: {data['location']}
        Date/Time: {data['date']} @ {data['time']}
        Party Size: {data['partySize']}
        Event Type: {data['eventType']}
        Org: {data['organization']}
        Comments: {data.get('comments', 'N/A')}
        """
        msg = EmailMessage()
        msg.set_content(msg_body)
        msg["Subject"] = "New Party Reservation"
        msg["From"] = GMAIL_USER
        msg["To"] = ["rob@elpueblomex.com", "rob@barbank.com"]
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(GMAIL_USER, GMAIL_PASSWORD)
            smtp.send_message(msg)

        sheet = gc.open_by_key(SHEET_ID).worksheet("Sheet2")
        sheet.append_row(
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

        return _cors_response({"message": "Reservation submitted!"})
    except Exception as e:
        print("❌ Reservation error:", e)
        return _cors_response({"error": "Reservation failed."}, status=500)


from flask import jsonify
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
import json, requests


@app.route("/reviews", methods=["GET"])
def reviews():
    try:
        with open("token.json", "r") as f:
            token_data = json.load(f)

        creds = Credentials.from_authorized_user_info(token_data, OAUTH_SCOPES)

        if creds.expired and creds.refresh_token:
            creds.refresh(Request())
            with open("token.json", "w") as f:
                f.write(creds.to_json())

        access_token = creds.token

        # ✅ Hardcoded values for now (you can dynamically list later if needed)
        account_id = "107556498414456817580"
        location_id = "1189929405054644351"
        url = f"https://mybusiness.googleapis.com/v4/accounts/{account_id}/locations/{location_id}/reviews"

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json",
        }

        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            print("❌ Google API Error:", response.status_code, response.text)
            return jsonify({"error": "Could not fetch reviews"}), 500

        data = response.json()
        return jsonify(
            {
                "location": "El Pueblo Mexican Food & Bar - Carmel Valley",
                "reviews": data.get("reviews", []),
            }
        )

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": "Server error while loading reviews"}), 500


# 🧑‍💼 /jobs
@app.route("/jobs", methods=["POST", "OPTIONS"])
def jobs():
    if request.method == "OPTIONS":
        return _build_cors_preflight_response()
    try:
        data = request.get_json()
        required = [
            "fullName",
            "phone",
            "dob",
            "email",
            "addressLine1",
            "city",
            "state",
            "postalCode",
            "employedBefore",
            "appliedBefore",
            "referralSource",
            "position",
            "location",
            "availableDate",
            "availability",
            "employmentHistory",
            "contactEmployer",
            "references",
            "felony",
            "jobFunctions",
            "transportation",
            "attendance",
            "authorization",
            "printName",
            "signatureDate",
        ]
        missing = [f for f in required if not data.get(f)]
        if missing:
            return _cors_response(
                {"error": f"Missing fields: {', '.join(missing)}"}, status=400
            )

        sheet3 = gc.open_by_key(SHEET_ID).worksheet("Sheet3")
        sheet3.append_row(
            [
                datetime.now().isoformat(),
                data.get("fullName"),
                data.get("phone"),
                data.get("dob"),
                data.get("email"),
                data.get("addressLine1"),
                data.get("addressLine2"),
                data.get("city"),
                data.get("state"),
                data.get("postalCode"),
                data.get("otherNames"),
                data.get("employedBefore"),
                data.get("employmentDates"),
                data.get("appliedBefore"),
                data.get("applicationDate"),
                data.get("referralSource"),
                data.get("position"),
                data.get("location"),
                data.get("availableDate"),
                data.get("availability"),
                data.get("employmentHistory"),
                data.get("contactEmployer"),
                data.get("references"),
                data.get("felony"),
                data.get("felonyExplanation"),
                data.get("jobFunctions"),
                data.get("transportation"),
                data.get("attendance"),
                data.get("authorization"),
                data.get("printName"),
                data.get("signatureDate"),
            ]
        )
        send_job_application_email(data)
        return _cors_response({"message": "✅ Job application submitted successfully!"})
    except Exception as e:
        print("❌ Job form error:", e)
        return _cors_response({"error": "Job submission failed."}, status=500)


if __name__ == "__main__":
    print("✅ Registered routes:")
    for rule in app.url_map.iter_rules():
        print(f"→ {rule.rule}")
    app.run(debug=True, port=5000)
