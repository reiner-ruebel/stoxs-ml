import os

from flask import Flask
from flask_mailman import EmailMessage, Mail

app = Flask(__name__)

# SMTP settings
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'my.smtp.server')
app.config['MAIL_BACKEND'] = 'smtp'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME', 'username')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD', '********')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER', 'username@company.com')

mail = Mail(app)

with app.app_context():
    msg = EmailMessage(
        subject='Hello from Flask',
        body='This is a test email sent from the Flask application using Google Workspace SMTP Relay.',
        to=['reiner.ruebel@corvendor.com'],
        from_email='ml.support@stoxs.io'
        )
    msg.send()
