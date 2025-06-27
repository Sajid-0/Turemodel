# TrueModel Website

A professional website for TrueModel, a service that provides hyper-realistic AI-generated images customized to meet the specific needs of various industries.

## Features

- Responsive, modern design
- Virtual model galleries
- Real vs AI-generated photo comparisons
- Industry-specific examples
- Pricing information
- Contact form
- How to order guides

## Technology Stack

- Backend: Python with Flask
- Frontend: HTML, CSS, JavaScript, Bootstrap 5
- Dependencies managed with pip

## Installation

1. Clone the repository:
```bash
git clone https://github.com/your-username/truemodel.git
cd truemodel
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

## Usage

To run the application locally:

```bash
python app.py
```

The application will be available at http://127.0.0.1:5000/

## Project Structure

```
truemodel/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── static/                # Static files (CSS, JS, images)
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── script.js
│   └── images/
├── templates/             # HTML templates
│   ├── base.html          # Base template with common elements
│   ├── index.html         # Home page
│   ├── virtual_models.html
│   ├── model_detail.html
│   ├── real_photos.html
│   ├── other_niches.html
│   ├── pricing.html
│   ├── how_to_order.html
│   └── contact.html
└── README.md              # Project documentation
```

## Deployment

To deploy this application to a production server:

1. Set up a WSGI server like Gunicorn:
```bash
gunicorn app:app
```

2. Use a reverse proxy like Nginx to serve the application.

3. Make sure to set `debug=False` in the Flask application for production.

## License

All rights reserved. This project and its content are proprietary.

## Contact

For any inquiries, please contact:
- Email: info@truemodel.ai
