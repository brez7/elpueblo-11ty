from flask import Flask, request, jsonify
import smtplib
from email.message import EmailMessage
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import base64
import re


def format_date(date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").strftime("%B %d, %Y")
    except:
        return date_str  # fallback if the format is off


app = Flask(__name__)

# Gmail setup
GMAIL_USER = "it@elpueblomex.com"
GMAIL_PASSWORD = "tywz qiut zlzq yndx"

# Google Sheets setup
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SERVICE_ACCOUNT_FILE = "sheets-creds.json"
credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
gc = gspread.authorize(credentials)
SHEET_ID = "1s1bqJcfEY2d4bCXHqfowPnHsZ2-hvm1EldrNeydZumQ"
worksheet = gc.open_by_key(SHEET_ID).worksheet("Sheet1")


# Utility: CORS headers
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


# ✉️ Job Application Email
import base64
import re
from email.message import EmailMessage


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

      <strong>Initials & Signature:</strong><br>
        <p>
        I hereby certify that I have not knowingly withheld any information that might adversely affect my chances for employment and that the answers given by me are correct to the best of my knowledge. I further certify that I, the undersigned applicant, have personally completed this application. I understand that any permission or misstatements of material fact on this application or on any document used to secure employment shall be grounds for rejection of this application or for immediate discharge if I am employed, regardless of the time elapsed before discovery.
        <br><img src="cid:initial1" width="150" height="85" style="border:1px solid #ccc; margin-top:8px;">
        </p>

        <p>
        I hereby authorize El Pueblo Mexican Food to thoroughly investigate my references, work record and other matters related to my suitability for employment and further.
        <br><img src="cid:initial2" width="150" height="85" style="border:1px solid #ccc; margin-top:8px;">
        </p>

        <p>
        I understand and agree that if I am employed, my employment is at will and is for no definite or determinable period and may be terminated at any anytime, with or without prior notice, or with or without cause, at the option of either myself or the company.
        <br><img src="cid:initial3" width="150" height="85" style="border:1px solid #ccc; margin-top:8px;">
        </p>

        <p>
        <strong>Applicant Signature:</strong><br>
        <img src="cid:signature" width="400" height="150" style="border:1px solid #ccc; margin-top:8px;">
        </p>
              <strong>Print Name:</strong> {data.get("printName")}<br>
<strong>Signature Date:</strong> {format_date(data.get("signatureDate"))}<br>
      
    </body></html>
    """

    msg.add_alternative(html_body, subtype="html")

    # Helper to safely attach base64-encoded images
    def attach_image(cid, data_url):
        if (
            not data_url
            or not isinstance(data_url, str)
            or not data_url.startswith("data:image")
        ):
            print(f"⚠️ Skipping image {cid}: invalid or missing data URL")
            return
        try:
            match = re.search(r"^data:image\/\w+;base64,(.+)", data_url)
            if not match:
                print(f"⚠️ Skipping image {cid}: malformed base64 data")
                return
            b64_data = match.group(1)
            img_data = base64.b64decode(b64_data)
            msg.get_payload()[1].add_related(
                img_data, maintype="image", subtype="png", cid=f"<{cid}>"
            )
        except Exception as e:
            print(f"❌ Error attaching image {cid}: {e}")

    # Attach all signature fields
    attach_image("initial1", data.get("initial1"))
    attach_image("initial2", data.get("initial2"))
    attach_image("initial3", data.get("initial3"))
    attach_image("signature", data.get("signature"))

    # Confirmation email to applicant
    confirmation = EmailMessage()
    confirmation["Subject"] = "We received your job application!"
    confirmation["From"] = GMAIL_USER
    confirmation["To"] = email
    confirmation.set_content(
        f"Hi {name},\n\nThanks for applying! We’ve received your job application and will review it shortly.\n\n— El Pueblo Team"
    )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(GMAIL_USER, GMAIL_PASSWORD)
        smtp.send_message(msg)
        smtp.send_message(confirmation)


# 📨 /submit
@app.route("/submit", methods=["POST", "OPTIONS"])
def submit():
    if request.method == "OPTIONS":
        return _build_cors_preflight_response()
    data = request.get_json()
    send_email(data.get("name"), data.get("email"), data.get("message"))
    try:
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
    app.run(debug=True, port=8080)
