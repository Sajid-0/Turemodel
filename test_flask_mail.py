#!/usr/bin/env python3
"""
Test Flask-Mail configuration with the working Hostinger credentials
"""
import os
from flask import Flask
from flask_mail import Mail, Message

# Set up the working credentials
os.environ['EMAIL_PROVIDER'] = 'hostinger'
os.environ['EMAIL_USER'] = 'info@truemodel.pro'
os.environ['EMAIL_PASS'] = '7iTVH5$Em'  # Using password from successful mailtest.py

app = Flask(__name__)
app.secret_key = 'test_key'

# Configure Flask-Mail with working Hostinger settings
app.config['MAIL_SERVER'] = 'smtp.hostinger.com'
app.config['MAIL_PORT'] = 465  # SSL port
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'info@truemodel.pro'
app.config['MAIL_PASSWORD'] = '7iTVH5$Em'  # Using password from successful mailtest.py
app.config['MAIL_DEFAULT_SENDER'] = 'info@truemodel.pro'

print("🔧 Flask-Mail Configuration:")
print(f"Server: {app.config['MAIL_SERVER']}:{app.config['MAIL_PORT']}")
print(f"SSL: {app.config['MAIL_USE_SSL']}")
print(f"TLS: {app.config['MAIL_USE_TLS']}")
print(f"Username: {app.config['MAIL_USERNAME']}")
print(f"Password: {'*' * len(app.config['MAIL_PASSWORD'])}")

# Initialize Mail
mail = Mail(app)

def test_send_email():
    """Test sending an email using Flask-Mail"""
    try:
        with app.app_context():
            msg = Message(
                subject="Flask-Mail Test",
                recipients=["info@truemodel.pro"],
                body="This is a test email sent using Flask-Mail with working Hostinger configuration."
            )
            mail.send(msg)
            print("✅ Flask-Mail test email sent successfully!")
            return True
    except Exception as e:
        print(f"❌ Flask-Mail test failed: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("🧪 FLASK-MAIL HOSTINGER TEST")
    print("=" * 60)
    
    test_send_email()
    
    print("=" * 60)
    print("🎉 TEST COMPLETE!")
    print("=" * 60)
