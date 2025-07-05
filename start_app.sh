#!/bin/bash

# Set environment variables for email configuration
export EMAIL_USER="joy.apee@gmail.com"
export EMAIL_PASS="1710374103"

echo "🔧 Setting up email configuration..."
echo "📧 Email User: $EMAIL_USER"
echo "🔑 Email Password: [CONFIGURED]"

# Activate virtual environment if it exists
if [ -f "/home/storage/AI/Research/Turemodel/webenv/bin/activate" ]; then
    echo "🐍 Activating virtual environment..."
    source /home/storage/AI/Research/Turemodel/webenv/bin/activate
fi

# Start the Flask application
echo "🚀 Starting Flask application..."
python app.py
