from extensions import db, bcrypt
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
import random
import string

def generate_account_number():
    """Generate a random 10-digit account number"""
    return ''.join(random.choices(string.digits, k=10))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(120), unique=True, index=True)
    firstname = db.Column(db.String(64), nullable=True)
    lastname = db.Column(db.String(64), nullable=True)
    # Detailed address fields
    address_line = db.Column(db.String(256), nullable=True)  # Street address, building, etc.
    region_code = db.Column(db.String(20), nullable=True)
    region_name = db.Column(db.String(100), nullable=True)
    province_code = db.Column(db.String(20), nullable=True)
    province_name = db.Column(db.String(100), nullable=True)
    city_code = db.Column(db.String(20), nullable=True)
    city_name = db.Column(db.String(100), nullable=True)
    barangay_code = db.Column(db.String(20), nullable=True)
    barangay_name = db.Column(db.String(100), nullable=True)
    postal_code = db.Column(db.String(10), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    password_hash = db.Column(db.String(128))
    account_number = db.Column(db.String(10), unique=True, default=generate_account_number)
    balance = db.Column(db.Float, default=1000.0)  # Match schema.sql default of 1000.0
    status = db.Column(db.String(20), default='pending')  # 'active', 'deactivated', or 'pending'
    is_admin = db.Column(db.Boolean, default=False)  # Admin status
    is_manager = db.Column(db.Boolean, default=False)  # Manager status (can manage admins)
    date_registered = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    transactions_sent = db.relationship('Transaction', foreign_keys='Transaction.sender_id', backref='sender', lazy='dynamic')
    transactions_received = db.relationship('Transaction', foreign_keys='Transaction.receiver_id', backref='receiver', lazy='dynamic')
    
    @property
    def full_address(self):
        """Return the full formatted address"""
        address_parts = []
        if self.address_line:
            address_parts.append(self.address_line)
        if self.barangay_name:
            address_parts.append(f"Barangay {self.barangay_name}")
        if self.city_name:
            address_parts.append(self.city_name)
        if self.province_name:
            address_parts.append(self.province_name)
        if self.region_name:
            address_parts.append(self.region_name)
        if self.postal_code:
            address_parts.append(self.postal_code)
        
        if address_parts:
            return ", ".join(address_parts)
        return "No address provided"
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def set_password(self, password):
        # Use bcrypt for secure password hashing with salt
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    
    def check_password(self, password):
        # Use bcrypt to verify password
        return bcrypt.check_password_hash(self.password_hash, password)
    
    @property
    def is_active(self):
        """Property to maintain compatibility with code using is_active"""
        return self.status == 'active'
    
    def transfer_money(self, recipient, amount):
        # Allow transfers if: 
        # 1. User has sufficient balance
        # 2. Amount is positive
        # 3. User is either active OR an admin OR a manager
        if self.balance >= amount and amount > 0 and (self.status == 'active' or self.is_admin or self.is_manager):
            self.balance -= amount
            recipient.balance += amount
            transaction = Transaction(
                sender_id=self.id,
                receiver_id=recipient.id,
                amount=amount,
                transaction_type='transfer',
                timestamp=datetime.datetime.utcnow()
            )
            db.session.add(transaction)
            return True
        return False
    
    def deposit(self, amount, admin_user):
        """Process an over-the-counter deposit by an admin"""
        if amount <= 0:
            return False
            
        # Add amount to user's balance
        self.balance += amount
        
        # Create a transaction record (from admin to user)
        transaction = Transaction(
            sender_id=admin_user.id,
            receiver_id=self.id,
            amount=amount,
            transaction_type='deposit',
            timestamp=datetime.datetime.utcnow()
        )
        db.session.add(transaction)
        return True
    
    def get_recent_transactions(self, limit=10):
        sent = self.transactions_sent.filter(Transaction.transaction_type != 'user_edit').order_by(Transaction.timestamp.desc()).limit(limit).all()
        received = self.transactions_received.filter(Transaction.transaction_type != 'user_edit').order_by(Transaction.timestamp.desc()).limit(limit).all()
        all_transactions = sorted(sent + received, key=lambda x: x.timestamp, reverse=True)
        return all_transactions[:limit]
    
    def activate_account(self):
        """Activate a user account"""
        self.status = 'active'
        db.session.commit()
    
    def deactivate_account(self):
        """Deactivate a user account"""
        self.status = 'deactivated'
        db.session.commit()
        
    def is_account_manager(self):
        """Check if user is a manager (can manage admins)"""
        return self.is_manager
    
    def can_manage_user(self, user):
        """Check if this user can manage another user based on roles"""
        # Managers can manage admins and regular users
        if self.is_manager:
            return not user.is_manager  # Managers can't manage other managers
        
        # Admins can only manage regular users
        if self.is_admin:
            return not user.is_admin and not user.is_manager
            
        # Regular users can't manage anyone
        return False

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    amount = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    transaction_type = db.Column(db.String(20), default='transfer')  # 'transfer', 'deposit', 'user_edit', etc.
    details = db.Column(db.Text, nullable=True)  # For storing additional details (e.g., fields modified)
    
    def __repr__(self):
        return f'<Transaction {self.id} - {self.amount}>' 