from flask import Flask
from flask_mailman import EmailMessage, Mail

app = Flask(__name__)

# SMTP settings
app.config['MAIL_SERVER'] = 'wp13793223.mailout.server-he.de'
app.config['MAIL_BACKEND'] = 'smtp'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'wp13793223-master'
app.config['MAIL_PASSWORD'] = 'FkZUTRN9CHv#wnN'
app.config['MAIL_DEFAULT_SENDER'] = 'info@refining-smart-data.com' 

mail = Mail(app)

with app.app_context():
    msg = EmailMessage(
        subject='Hello from Flask',
        body='This is a test email sent from the Flask application using Google Workspace SMTP Relay.',
        to=['reiner.ruebel@corvendor.com'],
        from_email='ml.support@stoxs.io'
        )
    msg.send()
