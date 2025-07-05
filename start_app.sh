#!/bin/bash

# TrueMelif [ "$EMAIL_PROVIDER" = "hostinger" ]; then
    echo "📧 Configuring Hostinger SMTP..."
    export EMAIL_PROVIDER="hostinger"
    export EMAIL_USER="info@truemodel.pro"  # Updated to correct working domain
    export EMAIL_PASS="7iTVH5\$Em"  # Correct working password (without X)
    
elseask App Startup Script
echo "🚀 Starting TrueModel Flask Application..."

# Email configuration - choose your provider
# Options: 'gmail' or 'hostinger'
EMAIL_PROVIDER=${EMAIL_PROVIDER:-"hostinger"}

if [ "$EMAIL_PROVIDER" = "gmail" ]; then
    echo "📧 Configuring Gmail SMTP..."
    export EMAIL_PROVIDER="gmail"
    export EMAIL_USER="truemodel.ai.contact@gmail.com"
    export EMAIL_PASS="${GMAIL_APP_PASSWORD}"  # Set this environment variable with your Gmail app password
    
    if [ -z "$EMAIL_PASS" ]; then
        echo "⚠️  Warning: GMAIL_APP_PASSWORD not set. Email functionality will be disabled."
        echo "   Please set your Gmail app password: export GMAIL_APP_PASSWORD='your_app_password'"
    fi
    
elif [ "$EMAIL_PROVIDER" = "hostinger" ]; then
    echo "� Configuring Hostinger SMTP..."
    export EMAIL_PROVIDER="hostinger"
    export EMAIL_USER="info@truemodel.pro"  # Updated to correct working domain
    export EMAIL_PASS="7iTVH5$EmX"  # Working password from successful test
    
else
    echo "❌ Invalid EMAIL_PROVIDER. Use 'gmail' or 'hostinger'"
    exit 1
fi

echo "✅ Email provider: $EMAIL_PROVIDER"
echo "✅ Email user: $EMAIL_USER"

# Activate virtual environment if it exists
if [ -f "/home/storage/AI/Research/Turemodel/webenv/bin/activate" ]; then
    echo "🐍 Activating virtual environment..."
    source /home/storage/AI/Research/Turemodel/webenv/bin/activate
fi

# Start the Flask application
echo "🚀 Starting Flask application..."
python3 app.py
