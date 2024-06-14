from eoms import app
from flask import jsonify
from eoms.form.contact_form import ContactForm
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

# Module to send emails using SMTP

# Load email configuration from environment variables
EMAIL_HOST = os.getenv('MAIL_SERVER')
EMAIL_PORT = os.getenv('MAIL_PORT')
EMAIL_HOST_USER = os.getenv('MAIL_USERNAME')
EMAIL_HOST_PASSWORD = os.getenv('MAIL_PASSWORD')
EMAIL_USE_TLS = True

def send_email(from_email, to_email, subject, body):
    # Compose the email
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    try:
        server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
        server.starttls()
        server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)
        server.quit()
        return {'success': True}
    except Exception as e:
        return {'success': False, 'message': f'{e}'}

