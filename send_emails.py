import gspread
from oauth2client.service_account import ServiceAccountCredentials
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get email and password from environment variables
SENDER_EMAIL = os.getenv('SENDER_EMAIL')
SENDER_PASSWORD = os.getenv('SENDER_PASSWORD')

# Google Sheets setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(creds)

# List all spreadsheets to check access
spreadsheet_list = client.openall()
print("Available spreadsheets:")
for sheet in spreadsheet_list:
    print(sheet.title)

# Open your Google Sheet
sheet = client.open(os.getenv('GOOGLE_SHEET')).sheet1

# Fetch all data from the sheet
data = sheet.get_all_records()

# Email setup
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
RESUME_PATH = os.getenv('RESUME_PATH')

def send_email(to_email, role, company, code):
    subject = f"Interested in {role} role at {company} - Job Bank Invite Code: {code}"
    body = f"""
    Dear Hiring Manager,

    I hope you're doing well. I'm Himanshu Kumar.  I am writing in response to your invitation to apply for the {role} role at {company} as posted on Job Bank (Job Bank invite code: {code}).

    After closely reviewing the role's specifics, I am genuinely excited about bringing my strengths in Software development, website architecture, software development strategy, and database design to your team.

    Please find my Resume attached for your detailed review.

    [Demo] Direct link to my sample work: https://himanshu.dev/projects/remplr

    Should you need any additional information or wish to discuss my experience further, please don't hesitate to contact me via this email. I look forward to hearing from you.

    Best,
    Himanshu Kumar
    """

    # Create the email
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = to_email
    msg['Subject'] = subject

    # Attach the body with the msg instance
    msg.attach(MIMEText(body, 'plain'))

    # Attach the resume
    with open(RESUME_PATH, 'rb') as attachment:
        part = MIMEApplication(attachment.read(), Name='Resume-Himanshu Kumar.pdf')
        part['Content-Disposition'] = 'attachment; filename="Resume-Himanshu Kumar.pdf"'
        msg.attach(part)

    # Connect to the server
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(SENDER_EMAIL, SENDER_PASSWORD)

    # Send the email
    server.sendmail(SENDER_EMAIL, to_email, msg.as_string())

    # Disconnect from the server
    server.quit()

# Iterate over each record and send emails
for record in data:
    send_email(record['Email'], record['ROLE'], record['COMPANY'], record['CODE'])

print("Emails sent successfully!")
