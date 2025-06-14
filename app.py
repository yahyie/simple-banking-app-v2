import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import secrets
import pymysql
from flask_wtf.csrf import CSRFProtect
from flask_limiter.errors import RateLimitExceeded
from flask_session import Session

# Import extensions
from extensions import db, login_manager, bcrypt, limiter

# Load environment variables
load_dotenv()

# Initialize CSRF protection
csrf = CSRFProtect()

# MySQL connection
pymysql.install_as_MySQLdb()

# Create Flask application
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or secrets.token_hex(16)

    # Flask-Session configuration for server-side sessions
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SESSION_PERMANENT'] = True  # Enable permanent sessions
    app.config['PERMANENT_SESSION_LIFETIME'] = 900  # 15 minutes (in seconds)
    app.config['SESSION_USE_SIGNER'] = True
    app.config['SESSION_FILE_DIR'] = os.path.join(os.path.dirname(__file__), 'flask_session')
    Session(app)

    # CSRF Protection
    csrf.init_app(app)
    app.config['WTF_CSRF_ENABLED'] = True
    app.config['WTF_CSRF_TIME_LIMIT'] = 3600  # 1 hour CSRF token validity
    app.config['WTF_CSRF_METHODS'] = ['POST', 'PUT', 'PATCH', 'DELETE']
    app.config['WTF_CSRF_SSL_STRICT'] = True  # Only accept CSRF tokens over HTTPS
    
    @app.errorhandler(400)
    def csrf_error(e):
        if getattr(e, 'description', None) == 'The CSRF token is missing.':
            return render_template('rate_limit_error.html', message="CSRF token missing or invalid. Please refresh the page and try again."), 400
        return e

    # Database configuration

    # Construct the MySQL URL from individual environment variables if DATABASE_URL is not provided
    # Use defaults to avoid None values
    mysql_user = os.environ.get('MYSQL_USER', '')
    mysql_password = os.environ.get('MYSQL_PASSWORD', '')
    mysql_host = os.environ.get('MYSQL_HOST', '')  # Default to localhost if not set
    mysql_port = os.environ.get('MYSQL_PORT', '3306')
    mysql_database = os.environ.get('MYSQL_DATABASE', '')
    
    # Make sure all values are strings
    mysql_port = str(mysql_port)
    
    # Check if required parameters are set
    if not mysql_host or not mysql_user or not mysql_database:
        print(f"WARNING: Missing database configuration. Host: {mysql_host}, User: {mysql_user}, Database: {mysql_database}")
    
    db_uri = f"mysql+pymysql://{mysql_user}:{mysql_password}@{mysql_host}:{mysql_port}/{mysql_database}"
    print(f"Database URI: {db_uri}")
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    limiter.init_app(app)
    
    # Register custom error handler for rate limiting
    @app.errorhandler(RateLimitExceeded)
    def handle_rate_limit_exceeded(e):
        # Log the event for auditing
        app.logger.warning(f"Rate limit exceeded: {request.remote_addr} {request.method} {request.path} - {str(e)}")
        # Check if it's an API request (expecting JSON)
        if request.path.startswith('/api/') or request.headers.get('Accept') == 'application/json':
            return jsonify({"error": "Rate limit exceeded", "message": str(e)}), 429
        # Otherwise, return the HTML template
        return render_template('rate_limit_error.html', message="You have exceeded the allowed number of requests. Please try again later."), 429

    return app

# Create Flask app
app = create_app()

# Import models - must be after db initialization
from models import User, Transaction

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Import routes after app creation
from routes import *

# Database initialization function
def init_db():
    """Initialize the database with required tables and default admin user."""
    with app.app_context():
        db.create_all()
        # Check if there are admin users, if not create one
        admin = User.query.filter_by(is_admin=True).first()
        if not admin:
            admin_user = User(
                username="admin",
                email="admin@bankapp.com",
                account_number="0000000001",
                status="active",
                is_admin=True,
                balance=0.0
            )
            admin_user.set_password("admin123")
            db.session.add(admin_user)
            db.session.commit()
            print("Created admin user with username 'admin' and password 'admin123'")

if __name__ == '__main__':
    # Print environment variables for debugging
    print(f"Environment variables:")
    print(f"MYSQL_HOST: {os.environ.get('MYSQL_HOST')}")
    print(f"MYSQL_USER: {os.environ.get('MYSQL_USER')}")
    print(f"MYSQL_DATABASE: {os.environ.get('MYSQL_DATABASE')}")
    
    with app.app_context():
        db.create_all()
    app.run(debug=True)
