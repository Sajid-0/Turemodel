#!/usr/bin/env python3
"""
Email configuration test script for Hostinger SMTP
This script tests different SMTP configurations to find the working one
"""

import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def test_smtp_config(server, port, use_tls, use_ssl, username, password):
    """Test a specific SMTP configuration"""
    print(f"\n🔧 Testing: {server}:{port} (TLS: {use_tls}, SSL: {use_ssl})")
    
    try:
        # Create SMTP connection
        if use_ssl:
            smtp = smtplib.SMTP_SSL(server, port)
            print("  ✅ SSL connection established")
        else:
            smtp = smtplib.SMTP(server, port)
            print("  ✅ SMTP connection established")
            
            if use_tls:
                smtp.starttls()
                print("  ✅ TLS enabled")
        
        # Try to login
        smtp.login(username, password)
        print("  ✅ Authentication successful!")
        
        # Create test message
        msg = MIMEMultipart()
        msg['From'] = username
        msg['To'] = username  # Send to self for testing
        msg['Subject'] = "Test Email from TrueModel.ai"
        
        body = "This is a test email to verify SMTP configuration."
        msg.attach(MIMEText(body, 'plain'))
        
        # Send test email
        text = msg.as_string()
        smtp.sendmail(username, username, text)
        print("  ✅ Test email sent successfully!")
        
        smtp.quit()
        return True
        
    except Exception as e:
        print(f"  ❌ Error: {str(e)}")
        return False

def main():
    # Get credentials from environment
    username = os.environ.get('EMAIL_USER', 'info@truemodel.ai')
    password = os.environ.get('EMAIL_PASS')
    
    if not password:
        print("❌ EMAIL_PASS environment variable not set!")
        print("Please set it with: export EMAIL_PASS='your_password'")
        return
    
    print(f"🔍 Testing email configurations for: {username}")
    print(f"🔑 Password length: {len(password)} characters")
    
    # Test different SMTP configurations
    configs = [
        # Hostinger standard configs
        {'server': 'smtp.hostinger.com', 'port': 587, 'tls': True, 'ssl': False},
        {'server': 'smtp.hostinger.com', 'port': 465, 'tls': False, 'ssl': True},
        {'server': 'smtp.hostinger.com', 'port': 25, 'tls': True, 'ssl': False},
        
        # Alternative Hostinger servers
        {'server': 'mail.truemodel.ai', 'port': 587, 'tls': True, 'ssl': False},
        {'server': 'mail.truemodel.ai', 'port': 465, 'tls': False, 'ssl': True},
        
        # Generic mail servers (if domain is configured)
        {'server': 'smtp.truemodel.ai', 'port': 587, 'tls': True, 'ssl': False},
        {'server': 'smtp.truemodel.ai', 'port': 465, 'tls': False, 'ssl': True},
    ]
    
    successful_configs = []
    
    for i, config in enumerate(configs, 1):
        print(f"\n📧 Configuration {i}/{len(configs)}:")
        success = test_smtp_config(
            config['server'], 
            config['port'], 
            config['tls'], 
            config['ssl'], 
            username, 
            password
        )
        if success:
            successful_configs.append(config)
    
    print(f"\n{'='*50}")
    if successful_configs:
        print(f"✅ Found {len(successful_configs)} working configuration(s):")
        for i, config in enumerate(successful_configs, 1):
            print(f"  {i}. {config['server']}:{config['port']} (TLS: {config['tls']}, SSL: {config['ssl']})")
        
        # Show Flask-Mail configuration for the first working config
        best_config = successful_configs[0]
        print(f"\n🔧 Recommended Flask-Mail configuration:")
        print(f"app.config['MAIL_SERVER'] = '{best_config['server']}'")
        print(f"app.config['MAIL_PORT'] = {best_config['port']}")
        print(f"app.config['MAIL_USE_TLS'] = {best_config['tls']}")
        print(f"app.config['MAIL_USE_SSL'] = {best_config['ssl']}")
        
    else:
        print("❌ No working configurations found!")
        print("\n🔍 Troubleshooting suggestions:")
        print("1. Verify your email password is correct")
        print("2. Check if SMTP is enabled in your Hostinger control panel")
        print("3. Ensure your domain's MX records are properly configured")
        print("4. Try using your Hostinger account password instead of email password")
        print("5. Check if two-factor authentication is interfering")

if __name__ == "__main__":
    main()
