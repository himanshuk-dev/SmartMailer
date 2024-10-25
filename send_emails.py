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
print("Data retrieved:", data)


# Email setup
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
RESUME_PATH = os.getenv('RESUME_PATH')
COVER_LETTER_PATH = os.getenv('COVER_LETTER_PATH')
SAMPLE_WORK = os.getenv('SAMPLE_WORK')

def send_email(to_email, role, company, code):
    print(f"Sending email to: {to_email} for role: {role} at company: {company}")

    
#     # NOTE: Use without Invite Code
#     subject = f"Interested in {role} role at {company}"
#     body = f"""
# Dear Hiring Manager,

# I hope you're doing well. I'm Himanshu Kumar. I am writing to express my interest in the {role} role at {company} as posted on Job Bank.

# After closely reviewing the role's specifics, I am genuinely excited about bringing my strengths in Software development, website architecture, software development strategy, and database design to your team.

# Please find my Resume, Cover letter and sample work attached for your detailed review.

# [Demo] Direct link to my work sample: https://himanshu.dev/projects/remplr

# Should you need any additional information or wish to discuss my experience further, please don't hesitate to contact me via this email. I look forward to hearing from you.

# Best,
# Himanshu Kumar
# """
    
    # NOTE: Use when Invite Code
    subject = f"Interested in {role} role at {company} - Job Bank Invite Code: {code}"
    body = f"""
Dear Hiring Manager,

I hope you're doing well. I'm Himanshu Kumar. I am writing in response to your invitation to apply for the {role} role at {company} as posted on Job Bank (Job Bank invite code: {code}).

After closely reviewing the role's specifics, I am genuinely excited about bringing my strengths in Software development, website architecture, software development strategy, and database design to your team.

Please find my Resume, Cover letter and sample work attached for your detailed review.

[Demo] Direct link to my work sample: https://himanshu.dev/projects/remplr

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
    
    # Attach the generic cover letter
    with open(COVER_LETTER_PATH, 'rb') as attachment:
        part = MIMEApplication(attachment.read(), Name='Cover Letter-Himanshu Kumar.pdf')
        part['Content-Disposition'] = 'attachment; filename="Cover Letter-Himanshu Kumar.pdf"'
        msg.attach(part)
    
    # Attach the sample work
    with open(SAMPLE_WORK, 'rb') as attachment:
        part = MIMEApplication(attachment.read(), Name='Work Sample-Himanshu Kumar.pdf')
        part['Content-Disposition'] = 'attachment; filename="Work Sample-Himanshu Kumar.pdf"'
        msg.attach(part)

    # Connect to the server
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, to_email, msg.as_string())
        print("Email sent to", to_email)
    except Exception as e:
        print("Error sending email:", e)
    finally:
        server.quit()


# Iterate over each record and send emails
for record in data:
    print("Processing record:", record)
    send_email(record['Email'], record['ROLE'], record['COMPANY'], record['CODE'])


print("Emails sent successfully!")
