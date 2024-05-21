
# SmartMailer

SmartMailer is an automated email sending tool designed to streamline the process of applying to job positions. It reads recipient details from a Google Sheet, customizes each email with specific details such as the job role, company name, and job invite code, and sends the emails individually. The emails are personalized with a tailored subject line and body content, and each email includes an attachment of the sender's resume.



https://github.com/himanshuk-dev/SmartMailer/assets/87880250/c25703ea-4a54-4526-826d-621957de14b9



## Features

- Read recipient details from a Google Sheet
- Customize email subject and body with job-specific details
- Attach resume to each email
- Send emails individually

## Prerequisites

- Python 3.x
- Google Cloud project with Google Sheets API enabled
- Credentials JSON file for Google Sheets API
- Gmail account for sending emails
- Required Python libraries (`gspread`, `oauth2client`, `smtplib`)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/SmartMailer.git
   cd SmartMailer
   ```

2. Install the required Python libraries:
   ```bash
   pip install gspread oauth2client
   ```

3. Ensure you have your Google Sheets API credentials JSON file (e.g., `credentials.json`) and your resume file (e.g., `resume.pdf`) in the project directory.

## Setup

1. Create a Google Sheet with the following columns:
   - Email
   - ROLE
   - COMPANY
   - CODE

2. Share the Google Sheet with your service account email from the Google Cloud project.

3. Update the `send_emails.py` script with your details:
   - Replace `"Your Google Sheet Name"` with the name of your Google Sheet.
   - Update `SENDER_EMAIL` and `SENDER_PASSWORD` with your Gmail credentials.
   - Ensure `credentials.json` and `resume.pdf` are in the same directory as the script.

## Usage

Run the script to send the emails:
```bash
python send_emails.py
```

## License

This project is licensed under the MIT License.
