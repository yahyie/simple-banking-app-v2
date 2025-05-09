from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize SQLAlchemy
db = SQLAlchemy()

# Initialize Login Manager
login_manager = LoginManager()
login_manager.login_view = 'login'

# Initialize Bcrypt
bcrypt = Bcrypt()

# Initialize rate limiter
storage_uri = os.environ.get('REDIS_URL', 'memory://')

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri=storage_uri,
    strategy="fixed-window",  # can be 'fixed-window', 'fixed-window-elastic-expiry', 'moving-window'
) 