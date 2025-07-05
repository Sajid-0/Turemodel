from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory, abort
from flask_mail import Mail, Message
import os
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'truemodel_secret_key'

# Configure Flask-Mail - Multiple options
# Option 1: Gmail (more reliable, requires app password)
# Option 2: Hostinger (domain email, but may have authentication issues)

EMAIL_PROVIDER = os.environ.get('EMAIL_PROVIDER', 'gmail')  # 'gmail' or 'hostinger'

if EMAIL_PROVIDER == 'gmail':
    # Gmail configuration (requires app password)
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False
    app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER', 'truemodel.ai.contact@gmail.com')
    app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')  # Gmail app password
    app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('EMAIL_USER', 'truemodel.ai.contact@gmail.com')
    print("📧 Using Gmail SMTP configuration")
else:
    # Hostinger configuration - WORKING SETTINGS FROM TEST
    app.config['MAIL_SERVER'] = 'smtp.hostinger.com'
    app.config['MAIL_PORT'] = 465  # Use SSL port 465 (working from test)
    app.config['MAIL_USE_TLS'] = False  # Disable TLS when using SSL
    app.config['MAIL_USE_SSL'] = True   # Enable SSL for port 465
    app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER', 'info@truemodel.pro')  # Correct domain
    app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')  # Hostinger email password
    app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('EMAIL_USER', 'info@truemodel.pro')  # Correct domain
    print("📧 Using Hostinger SMTP configuration (SSL port 465)")

# Only initialize mail if password is configured
if app.config['MAIL_PASSWORD']:
    mail = Mail(app)
    print("✅ Flask-Mail configured successfully")
else:
    mail = None
    print("❌ EMAIL_PASS environment variable not set. Email functionality disabled.")

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
            '/images/Ava/image_0 (16).webp',
            '/images/Ava/image_0 (18).webp',
            '/images/Ava/image_0 (4).webp',
            '/images/Ava/image_0.webp',
            '/images/Ava/image_0 (13).webp'
        ]
    },
    'busty': {
        'name': 'Busty',
        'description': 'A confident and striking virtual model ideal for bold fashion statements and campaigns.',
        'images': [
            '/images/Busty/image_13.webp',
            '/images/Busty/image_16.webp',
            '/images/Busty/image_17.webp',
            '/images/Busty/image_4.webp',
            '/images/Busty/image_6.webp'
        ]
    },
    'mary': {
        'name': 'Mary',
        'description': 'A natural and approachable virtual model perfect for casual and relatable brand imagery.',
        'images': [
            '/images/Mary/prompt_16_image_0_seed_1326810014.webp',
            '/images/Mary/prompt_26_image_0_seed_36969806.webp',
            '/images/Mary/prompt_34_image_0_seed_675966102.webp',
            '/images/Mary/prompt_3_image_0_seed_1304252368.webp',
            '/images/Mary/prompt_3_image_0_seed_1822999138.webp',
            '/images/Mary/prompt_3_image_0_seed_344006658.webp',
            '/images/Mary/prompt_6_image_0_seed_694012188.webp',
            '/images/Mary/prompt_7_image_0_seed_1722280745.webp'
        ]
    },
    'anissa': {
        'name': 'Anissa',
        'description': 'An expressive and dynamic virtual model suited for contemporary and edgy brand aesthetics.',
        'images': [
            '/images/Annisa/image_10.webp',
            '/images/Annisa/image_23 (1).webp',
            '/images/Annisa/image_50.webp',
            '/images/Annisa/image_70.webp'
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
        '/images/Lollipop/prompt_11_image_0_seed_234017599.webp',
        '/images/Lollipop/prompt_5_image_0_seed_740846037.webp',
        '/images/Lollipop/prompt_7_image_0_seed_382826355.webp',
        '/images/Lollipop/prompt_8_image_0_seed_237859241.webp',
        '/images/Lollipop/prompt_8_image_0_seed_579869548.webp'
    ]
}

# Define other niches
other_niches = [
    '/images/OtherNiches/image_0 (1).webp',
    '/images/OtherNiches/image_0 (61).webp',
    '/images/OtherNiches/image_14.webp',
    '/images/OtherNiches/image_16 (1).webp',
    '/images/OtherNiches/image_17 (1).webp',
    '/images/OtherNiches/image_23.webp',
    '/images/OtherNiches/image_3.webp',
    '/images/OtherNiches/image_3 (1).webp',
    '/images/OtherNiches/image_41.webp',
    '/images/OtherNiches/image_46.webp',
    '/images/OtherNiches/image_6 (1).webp',
    '/images/OtherNiches/image_6 (2).webp',
    '/images/OtherNiches/image_9.webp'
]

# Define pricing plans
pricing_plans = {
    'basic': {
        'name': 'Basic',
        'price': '$105 USD',
        'images': '15 high-quality images',
        'revisions': '2 revisions per image',
        'delivery': '1-3 days'
    },
    'standard': {
        'name': 'Standard',
        'price': '$199 USD',
        'images': '30 high-quality images',
        'revisions': '3 revisions per image',
        'delivery': '3-5 days'
    },
    'premium': {
        'name': 'Premium',
        'price': '$385 USD',
        'images': '60 high-quality images',
        'revisions': '3 revisions per image',
        'delivery': '5-7 days'
    }
}

# Define custom pricing plans
custom_pricing = [
    {'range': '200-499 Images', 'price': 'starting at $6.00 per image', 'delivery': '7-12 business days', 'revisions': '3 revisions per image'},
    {'range': '500-999 Images', 'price': 'starting at $5.60 per image', 'delivery': '10-15 business days', 'revisions': '3 revisions per image'},
    {'range': '1000+ Images', 'price': 'starting at $5.40 per image', 'delivery': '15-25 business days', 'revisions': '3 revisions per image'}
]

# Define social media links
social_links = {
    'whatsapp': 'https://wa.me/your_number_here',
    'linkedin': 'https://linkedin.com/in/your_profile',
    'gmail': 'mailto:info@truemodel.pro',  # Updated to correct domain
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
                           photos=other_niches,
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
            
            # Send email only if mail is configured
            if mail:
                try:
                    recipient = "info@truemodel.pro"  # Updated to correct domain
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
            else:
                flash('Your message was saved successfully. Email notifications are currently disabled.', 'info')
                
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
def other_niches_alt():
    return redirect(url_for('other_niches_page'))

# Route to serve images
@app.route('/images/<path:filename>')
def serve_image(filename):
    try:
        # Check if file exists
        image_path = os.path.join('Images', filename)
        if not os.path.exists(image_path):
            abort(404)
        
        response = send_from_directory('Images', filename)
        # Add cache headers for better performance
        response.cache_control.max_age = 86400  # Cache for 1 day
        response.cache_control.public = True
        return response
    except Exception as e:
        print(f"Error serving image {filename}: {e}")
        abort(404)

# Route to serve hero image
@app.route('/hero-image')
def hero_image():
    try:
        hero_path = os.path.join('Images', 'hero.webp')
        if not os.path.exists(hero_path):
            abort(404)
        
        response = send_from_directory('Images', 'hero.webp')
        response.cache_control.max_age = 86400  # Cache for 1 day
        response.cache_control.public = True
        return response
    except Exception as e:
        print(f"Error serving hero image: {e}")
        abort(404)

if __name__ == '__main__':
    app.run(debug=False)
