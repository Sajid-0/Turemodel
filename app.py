from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mail import Mail, Message
import os
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'truemodel_secret_key'

# Configure Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER', 'joy.apee@gmail.com')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS', 'your_email_password')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('EMAIL_USER', 'joy.apee@gmail.com')
mail = Mail(app)

# Database setup

def get_db_connection():
    # Check if using production database URL (environment variable)
    database_url = os.environ.get('DATABASE_URL', 'truemodel.db')
    if database_url.startswith('postgres://'):
        # For platforms that use PostgreSQL
        import psycopg2
        conn = psycopg2.connect(database_url)
        conn.cursor().execute('CREATE TABLE IF NOT EXISTS contact_messages (...)')
        return conn
    else:
        # Local SQLite development
        conn = sqlite3.connect(database_url)
        conn.row_factory = sqlite3.Row
        return conn



def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS contact_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            subject TEXT NOT NULL,
            message TEXT NOT NULL,
            requirements TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# Initialize the database
init_db()

# Define virtual models data
virtual_models = {
    'ava': {
        'name': 'AVA',
        'description': 'Our elegant and versatile virtual model for various fashion and lifestyle contexts.',
        'images': [
            'https://i.postimg.cc/t4tFBqqx/image-0-16.png',
            'https://i.postimg.cc/NfX6r8Zb/image-0-18.png',
            'https://i.postimg.cc/DwKqQJTh/image-0-4.png',
            'https://i.postimg.cc/pdWz7wr1/image-0-7.png'
        ]
    },
    'busty': {
        'name': 'Busty',
        'description': 'A confident and striking virtual model ideal for bold fashion statements and campaigns.',
        'images': [
            'https://i.postimg.cc/XqKQdTvK/image-13.png',
            'https://i.postimg.cc/PJnSLtdr/image-16.png',
            'https://i.postimg.cc/bNTmJcWp/image-17.png',
            'https://i.postimg.cc/fWYHG0v3/image-4.png',
            'https://i.postimg.cc/vHMPbHP0/image-6.png'
        ]
    },
    'mary': {
        'name': 'Mary',
        'description': 'A natural and approachable virtual model perfect for casual and relatable brand imagery.',
        'images': [
            'https://i.postimg.cc/zDwjtYJK/prompt-16-image-0-seed-1326810014.png',
            'https://i.postimg.cc/Ghcj6g2N/prompt-26-image-0-seed-36969806.png',
            'https://i.postimg.cc/02cCvGKN/prompt-34-image-0-seed-675966102.png',
            'https://i.postimg.cc/zBKjY9Tm/prompt-3-image-0-seed-1304252368.png',
            'https://i.postimg.cc/D0hcvBcS/prompt-3-image-0-seed-1822999138.png',
            'https://i.postimg.cc/BvdgyqLc/prompt-3-image-0-seed-344006658.png',
            'https://i.postimg.cc/PJMQPY62/prompt-7-image-0-seed-1722280745.png'
        ]
    },
    'anissa': {
        'name': 'Anissa',
        'description': 'An expressive and dynamic virtual model suited for contemporary and edgy brand aesthetics.',
        'images': [
            'https://i.postimg.cc/Bnmbb5d7/image-10.png',
            'https://i.postimg.cc/mDHgmvhK/image-23-1.png',
            'https://i.postimg.cc/DzmZXJhv/image-50.png',
            'https://i.postimg.cc/DzDzdvfq/image-70.png'
        ]
    }
}

# Define real vs generated photos for comparison
real_vs_generated = {
    'real': [
        'https://i.postimg.cc/3Nhzsj4B/1.jpg',
        'https://i.postimg.cc/NG831nSP/a14cf70b-56ca-4d71-9ddf-21e2965e375d.jpg',
        'https://i.postimg.cc/jdsGvXrq/cd24c53f-ee7c-47b4-b33c-981a9d11fe0e.jpg',
        'https://i.postimg.cc/L5VG2qjM/e3080a13-007c-48e6-9f5f-abe0c8b5d7d8.jpg',
        'https://i.postimg.cc/282gtZzQ/ecbfa719-0b52-4892-a8a7-b79a58e64bed.jpg'
    ],
    'generated': [
        'https://i.postimg.cc/rmk4xzRb/prompt-11-image-0-seed-234017599.png',
        'https://i.postimg.cc/Gh7vVc68/prompt-5-image-0-seed-740846037.png',
        'https://i.postimg.cc/g218cgzG/prompt-8-image-0-seed-237859241.png',
        'https://i.postimg.cc/pLmKtwt0/prompt-8-image-0-seed-579869548.png'
    ]
}

# Define other niches
other_niches = [
    'https://i.postimg.cc/WpyKVPBK/image-0-1.png',
    'https://i.postimg.cc/L6ZW6bRs/image-0-61.png',
    'https://i.postimg.cc/Vs38RMkd/image-14.png',
    'https://i.postimg.cc/GmR10CYR/image-16-1.png',
    'https://i.postimg.cc/TPPFGY3z/image-17-1.png',
    'https://i.postimg.cc/d0SX0P7L/image-23.png',
    'https://i.postimg.cc/4xkSKQNQ/image-3.png',
    'https://i.postimg.cc/KjCsDn7F/image-3-1.png',
    'https://i.postimg.cc/mDznzXMV/image-41.png',
    'https://i.postimg.cc/pTw6DfJv/image-46.png',
    'https://i.postimg.cc/s23HmfWB/image-6-1.png',
    'https://i.postimg.cc/c6qXndZL/image-6-2.png',
    'https://i.postimg.cc/7Y0yQ65X/image-9.png'
]

# Define pricing plans
pricing_plans = {
    'basic': {
        'name': 'Basic',
        'price': '$75 USD',
        'images': '15 high-quality images',
        'revisions': '2 revisions per image',
        'delivery': '1-3 days'
    },
    'standard': {
        'name': 'Standard',
        'price': '$145 USD',
        'images': '30 high-quality images',
        'revisions': '3 revisions per image',
        'delivery': '3-5 days'
    },
    'premium': {
        'name': 'Premium',
        'price': '$275 USD',
        'images': '60 high-quality images',
        'revisions': '3 revisions per image',
        'delivery': '5-7 days'
    }
}

# Define custom pricing plans
custom_pricing = [
    {'range': '200-499 Images', 'price': 'starting at $4.30 per image', 'delivery': '7-12 business days', 'revisions': '3 revisions per image'},
    {'range': '500-999 Images', 'price': 'starting at $4.00 per image', 'delivery': '10-15 business days', 'revisions': '3 revisions per image'},
    {'range': '1000+ Images', 'price': 'starting at $3.85 per image', 'delivery': '15-25 business days', 'revisions': '3 revisions per image'}
]

# Define social media links
social_links = {
    'whatsapp': 'https://wa.me/your_number_here',
    'linkedin': 'https://linkedin.com/in/your_profile',
    'gmail': 'mailto:joy.apee@gmail.com',
    'instagram': 'https://www.instagram.com/truemodelofficial/'
}

@app.route('/')
def home():
    # Pass all the data to the template
    return render_template('index.html', 
                           virtual_models=virtual_models,
                           real_vs_generated=real_vs_generated,
                           other_niches=other_niches,
                           pricing_plans=pricing_plans,
                           custom_pricing=custom_pricing,
                           social_links=social_links)

@app.route('/model/<model_id>')
def model_detail(model_id):
    if model_id in virtual_models:
        return render_template('model_detail.html', 
                               model_id=model_id, 
                               model=virtual_models[model_id],
                               social_links=social_links)
    else:
        flash('Model not found', 'error')
        return redirect(url_for('home'))

@app.route('/real-comparison')
def real_comparison():
    return render_template('real_comparison.html', 
                           real_vs_generated=real_vs_generated,
                           social_links=social_links)

@app.route('/real-photos')
def real_photos_page():
    return render_template('real_comparison.html', 
                           real_vs_generated=real_vs_generated,
                           social_links=social_links)

@app.route('/other-niches')
def other_niches_page():
    return render_template('other_niches.html', 
                           other_niches=other_niches,
                           social_links=social_links)

@app.route('/pricing')
def pricing():
    return render_template('pricing.html', 
                           pricing_plans=pricing_plans,
                           custom_pricing=custom_pricing,
                           social_links=social_links)

@app.route('/how-to-order')
def how_to_order():
    return render_template('how_to_order.html', social_links=social_links)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Get form data
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')
        requirements = request.form.get('requirements', '')
        
        # Save to database
        try:
            conn = get_db_connection()
            conn.execute(
                'INSERT INTO contact_messages (name, email, subject, message, requirements) VALUES (?, ?, ?, ?, ?)',
                (name, email, subject, message, requirements)
            )
            conn.commit()
            conn.close()
            
            # Send email
            try:
                recipient = "joy.apee@gmail.com"
                msg = Message(
                    subject=f"TrueModel Contact Form: {subject}",
                    recipients=[recipient],
                    body=f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}\n\nProject Requirements:\n{requirements}"
                )
                mail.send(msg)
                
                # Send confirmation email to user
                user_msg = Message(
                    subject="Thank you for contacting TrueModel",
                    recipients=[email],
                    body=f"Dear {name},\n\nThank you for reaching out to us. We have received your message and will get back to you shortly.\n\nBest regards,\nThe TrueModel Team"
                )
                mail.send(user_msg)
                
                flash('Thank you! Your message has been sent successfully.', 'success')
            except Exception as e:
                # If email fails, still save to database but inform admin
                print(f"Email sending failed: {e}")
                flash('Your message was saved but email notification failed. We will still process your request.', 'warning')
                
        except Exception as e:
            print(f"Database error: {e}")
            flash('There was an error processing your request. Please try again.', 'danger')
            
        return redirect(url_for('contact', success=True))
    
    return render_template('contact.html', social_links=social_links)

# Add this new route for the virtual models page
@app.route('/virtual-models')
def virtual_models_page():
    return render_template('virtual_models.html', 
                           virtual_models=virtual_models,
                           social_links=social_links)

@app.route('/virtual-model/<model_id>')
def virtual_model_detail(model_id):
    if model_id in virtual_models:
        return render_template('model_detail.html', 
                              model_id=model_id, 
                              model=virtual_models[model_id],
                              social_links=social_links)
    else:
        flash('Model not found', 'error')
        return redirect(url_for('home'))

# Add an alias route for 'other_niches'
@app.route('/other-niches-alt')
def other_niches():
    return redirect(url_for('other_niches_page'))

if __name__ == '__main__':
    app.run(debug=True)
