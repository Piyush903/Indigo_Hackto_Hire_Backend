import smtplib
from email.mime.text import MIMEText
from twilio.rest import Client
import os

# Ensure these environment variables are set correctly
SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', 587))  # TLS
SMTP_USERNAME = os.getenv('SMTP_USERNAME')
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD')
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')

def send_email(recipient, subject, body):
    # Use MIMEText to create an HTML email
    msg = MIMEText(body, 'html')
    msg['Subject'] = subject
    msg['From'] = SMTP_USERNAME
    msg['To'] = recipient

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.sendmail(SMTP_USERNAME, recipient, msg.as_string())
        print('Email sent successfully!')
    except smtplib.SMTPAuthenticationError as e:
        print(f'Authentication error: {e}')
    except smtplib.SMTPException as e:
        print(f'SMTP error: {e}')

def send_sms(recipient, body):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    try:
        message = client.messages.create(
            body=body,
            from_=TWILIO_PHONE_NUMBER,
            to=recipient
        )
        print('SMS sent successfully!')
        return message.sid
    except Exception as e:
        print(f'SMS sending error: {e}')
