import smtplib
import imaplib
import poplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import ssl
import socket
from datetime import datetime

# Your credentials - UPDATED WITH ACTUAL EMAIL
EMAIL = "info@truemodel.pro"
PASSWORD = "7iTVH5$Em"

# Hostinger mail server settings
SMTP_SERVER = "smtp.hostinger.com"
SMTP_PORT = 465
IMAP_SERVER = "imap.hostinger.com"
IMAP_PORT = 993
POP3_SERVER = "pop.hostinger.com"
POP3_PORT = 995

def test_server_connectivity():
    """Test if mail servers are reachable"""
    print("🔍 Testing server connectivity...")
    
    servers = [
        (SMTP_SERVER, SMTP_PORT, "SMTP"),
        (IMAP_SERVER, IMAP_PORT, "IMAP"),
        (POP3_SERVER, POP3_PORT, "POP3")
    ]
    
    for server, port, protocol in servers:
        try:
            sock = socket.create_connection((server, port), timeout=10)
            sock.close()
            print(f"✅ {protocol} server {server}:{port} is reachable")
        except Exception as e:
            print(f"❌ {protocol} server {server}:{port} is not reachable: {e}")

def test_smtp_connection():
    """Test SMTP connection for sending emails"""
    try:
        print("\n📤 Testing SMTP connection...")
        
        # Create SSL context
        context = ssl.create_default_context()
        
        # Connect to server
        server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context)
        server.set_debuglevel(0)  # Set to 1 for detailed debug info
        
        # Login
        server.login(EMAIL, PASSWORD)
        print("✅ SMTP connection and authentication successful!")
        
        # Test EHLO
        server.ehlo()
        print("✅ SMTP EHLO command successful!")
        
        server.quit()
        return True
    except smtplib.SMTPAuthenticationError as e:
        print(f"❌ SMTP Authentication failed: {e}")
        print("   Check your email and password!")
        return False
    except smtplib.SMTPException as e:
        print(f"❌ SMTP error: {e}")
        return False
    except Exception as e:
        print(f"❌ SMTP connection failed: {e}")
        return False

def test_imap_connection():
    """Test IMAP connection for reading emails"""
    try:
        print("\n📥 Testing IMAP connection...")
        
        # Connect to IMAP server
        imap = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
        
        # Login
        imap.login(EMAIL, PASSWORD)
        print("✅ IMAP connection and authentication successful!")
        
        # List mailboxes
        mailboxes = imap.list()
        print(f"✅ Found {len(mailboxes[1])} mailboxes")
        
        # Select inbox
        imap.select('INBOX')
        print("✅ INBOX selected successfully!")
        
        # Get email count
        status, messages = imap.search(None, 'ALL')
        if status == 'OK':
            email_count = len(messages[0].split())
            print(f"✅ Found {email_count} emails in INBOX")
        
        imap.close()
        imap.logout()
        return True
    except imaplib.IMAP4.error as e:
        print(f"❌ IMAP authentication failed: {e}")
        return False
    except Exception as e:
        print(f"❌ IMAP connection failed: {e}")
        return False

def test_pop3_connection():
    """Test POP3 connection for reading emails"""
    try:
        print("\n📨 Testing POP3 connection...")
        
        # Connect to POP3 server
        pop3 = poplib.POP3_SSL(POP3_SERVER, POP3_PORT)
        
        # Login
        pop3.user(EMAIL)
        pop3.pass_(PASSWORD)
        print("✅ POP3 connection and authentication successful!")
        
        # Get email count
        num_messages = len(pop3.list()[1])
        print(f"✅ Found {num_messages} emails via POP3")
        
        pop3.quit()
        return True
    except poplib.error_proto as e:
        print(f"❌ POP3 authentication failed: {e}")
        return False
    except Exception as e:
        print(f"❌ POP3 connection failed: {e}")
        return False

def send_test_email(recipient_email=None):
    """Send a test email"""
    try:
        print("\n📧 Sending test email...")
        
        # Use sender's email as recipient if not specified
        if not recipient_email:
            recipient_email = EMAIL
        
        # Create message
        msg = MIMEMultipart()
        msg['From'] = EMAIL
        msg['To'] = recipient_email
        msg['Subject'] = f"Test Email - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        # Email body
        body = f"""
        Hello!
        
        This is a test email sent from your Flask mail application.
        
        Test Details:
        - Sent from: {EMAIL}
        - SMTP Server: {SMTP_SERVER}:{SMTP_PORT}
        - Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        - Status: All mail server connections working properly!
        
        Best regards,
        Your Flask Mail App
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Send email
        context = ssl.create_default_context()
        server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context)
        server.login(EMAIL, PASSWORD)
        server.send_message(msg)
        server.quit()
        
        print(f"✅ Test email sent successfully to {recipient_email}!")
        print("   Check your inbox to confirm delivery.")
        return True
    except Exception as e:
        print(f"❌ Failed to send test email: {e}")
        return False

def send_simple_text_email():
    """Send a simple text email using basic SMTP"""
    try:
        print("\n📧 Sending simple text email...")
        
        # Email content
        subject = "Simple Test Email"
        body = "This is a simple test email sent using Python!"
        
        # Create message
        message = f"Subject: {subject}\n\n{body}"
        
        # Send email
        context = ssl.create_default_context()
        server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context)
        server.login(EMAIL, PASSWORD)
        server.sendmail(EMAIL, EMAIL, message)
        server.quit()
        
        print("✅ Simple text email sent successfully!")
        return True
    except Exception as e:
        print(f"❌ Failed to send simple email: {e}")
        return False

def main():
    """Main test function"""
    print("=" * 60)
    print("🔧 HOSTINGER MAIL SERVER CONNECTIVITY TEST")
    print("=" * 60)
    print(f"📧 Email: {EMAIL}")
    print(f"🔐 Password: {'*' * len(PASSWORD)}")
    print(f"📅 Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Test server connectivity
    test_server_connectivity()
    
    # Test connections
    smtp_ok = test_smtp_connection()
    imap_ok = test_imap_connection()
    pop3_ok = test_pop3_connection()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    print(f"SMTP (Send Mail): {'✅ WORKING' if smtp_ok else '❌ FAILED'}")
    print(f"IMAP (Read Mail): {'✅ WORKING' if imap_ok else '❌ FAILED'}")
    print(f"POP3 (Read Mail): {'✅ WORKING' if pop3_ok else '❌ FAILED'}")
    
    # Send test emails if SMTP works
    if smtp_ok:
        print("\n" + "=" * 60)
        print("📧 EMAIL SENDING TESTS")
        print("=" * 60)
        
        # Ask user if they want to send test emails
        send_test = input("\n🤔 Do you want to send test emails? (y/n): ").lower()
        if send_test == 'y':
            # Send different types of test emails
            send_simple_text_email()
            send_test_email()
            
            # Option to send to another email
            other_email = input("\n📧 Send test to another email address? (Enter email or press Enter to skip): ").strip()
            if other_email and '@' in other_email:
                send_test_email(other_email)
    
    print("\n" + "=" * 60)
    print("🎉 TESTING COMPLETE!")
    print("=" * 60)

if __name__ == "__main__":
    main()