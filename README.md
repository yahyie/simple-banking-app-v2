# Simple Banking App (version 2.0)

---

## Group Members:
- Bazar, Jayp
- Magno, Quennie
- Nanale, Krizia Belle

---

## Introduction 
A user-friendly and responsive Flask-based banking application designed for deployment on PythonAnywhere. This application allows users to create accounts, perform simulated money transfers between accounts, view transaction history, and securely manage their credentials.

---

## Objectives
1. Provide a secure and intuitive digital banking platform for users to manage their finances online.
2. Implement robust user authentication and role-based access control to safeguard user accounts and sensitive operations.
3. Integrate Philippine Standard Geographic Code (PSGC) data for standardized address management and validation.

--- 

## Original Application Features

- **User Authentication**
  - Secure login with username/password
  - Registration of new users
  - Password recovery mechanism (email-based)

- **Account Management**
  - Display of account balance
  - View recent transaction history (last 10 transactions)

- **Fund Transfer**
  - Transfer money to other registered users
  - Confirmation screen before completing transfers
  - Transaction history updated after transfers

- **User Role Management**
  - Regular user accounts
  - Admin users with account approval capabilities
  - Manager users who can manage admin accounts

- **Location Data Integration**
  - Philippine Standard Geographic Code (PSGC) API integration
  - Hierarchical location data selection (Region, Province, City, Barangay)
  - Form fields pre-populated with location data

- **Admin Features**
  - User account approval workflow
  - Account activation/deactivation
  - Deposit funds to user accounts
  - Create new accounts
  - Edit user information

- **Manager Features**
  - Create and manage admin accounts
  - View admin transaction logs
  - Monitor all system transfers

- **Security**
  - Password hashing with bcrypt for secure storage
  - Secure session management
  - Token-based password reset
  - API rate limiting to prevent abuse
  - CSRF protection for all forms

---

## Found Vulnerabilities
- Weak password validation
- Weak form input validation
- Weak limit handling
- No confirmation when doing large transactions

---

## Security Improvements Implemented
- Enforced strong password validation rules.
- Implemented thorough input validation for all user forms.
- Improved rate limiting and transaction throttling to prevent abuse.
- Added explicit confirmation steps for large transactions.
- Enhanced CSRF protection and session security.
- Adopted bcrypt for password hashing and secure storage.
- Integrated admin approval workflow for new accounts.
- Two-step transaction confirmation for sensitive operations.



---
![Home](https://github.com/yahyie/simple-banking-app-v2/blob/main/Screenshots/Home.png?raw=true)
![022dd193-a0b4-4bd4-a5f0-622e33bb9fb0](https://github.com/yahyie/simple-banking-app-v2/blob/main/Screenshots/022dd193-a0b4-4bd4-a5f0-622e33bb9fb0.jfif?raw=true)
![5a0ac7ea-2798-4981-a336-65b1659ec5a5](https://github.com/yahyie/simple-banking-app-v2/blob/main/Screenshots/5a0ac7ea-2798-4981-a336-65b1659ec5a5.jfif?raw=true)
![09448b1e-6966-41db-a8f5-8fafbeb51a8a](https://github.com/yahyie/simple-banking-app-v2/blob/main/Screenshots/09448b1e-6966-41db-a8f5-8fafbeb51a8a.jfif?raw=true)




## Access the deployed application
- Link to application: https://bovopo4471.pythonanywhere.com/login

---

## How to Run Application

### Prerequisites
- Python 3.7+
- pip (Python package manager)
- MySQL Server 5.7+ or MariaDB 10.2+

### Database Setup

1. Install MySQL Server or MariaDB if you haven't already:
   ```
   # For Ubuntu/Debian
   sudo apt update
   sudo apt install mysql-server

   # For macOS with Homebrew
   brew install mysql

   # For Windows
   # Download and install from the official website
   ```

2. Create a database user and set privileges:
   ```
   mysql -u root -p

   # In MySQL prompt
   CREATE USER 'bankapp'@'localhost' IDENTIFIED BY 'your_password';
   GRANT ALL PRIVILEGES ON *.* TO 'bankapp'@'localhost';
   FLUSH PRIVILEGES;
   EXIT;
   ```

3. Update the `.env` file with your MySQL credentials:
   ```
   DATABASE_URL=mysql+pymysql://bankapp:your_password@localhost/simple_banking
   MYSQL_USER=bankapp
   MYSQL_PASSWORD=your_password
   MYSQL_HOST=localhost
   MYSQL_PORT=3306
   MYSQL_DATABASE=simple_banking
   ```

4. Initialize the database:
   ```
   python init_db.py
   ```

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/jaypbazar/simple-banking-app-v2.git
   cd simple-banking-app
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```
   
3. Initialize the database:
   ```
   python init_db.py
   ```
   
4. Run the application:
   ```
   python app.py
   ```

5. Access the application at `http://localhost:5000`

---

## Usage

### Registration
- Navigate to the registration page
- Enter username, email, and password
- Confirm your password
- Submit the form to create your account (pending admin approval)

### Login
- Enter your username and password
- Click "Sign In"

### Account Overview
- View your current balance
- See your recent transaction history

### Transfer Funds
- Navigate to the Transfer page
- Enter recipient's username or account number
- Enter the amount to transfer
- Confirm the transfer details on the confirmation screen
- Complete the transfer

### Password Reset
- Click "Forgot your password?" on the login page
- Enter your registered email address
- Follow the link in the email (simulated in this demo)
- Create a new password

### Admin Features
- Approve new user registrations
- Activate/deactivate user accounts
- Create new user accounts
- Make over-the-counter deposits to user accounts
- Edit user details including location information

### Manager Features
- Create new admin accounts
- Toggle admin status for users
- View all user transactions
- Monitor and audit admin activities

---

## User Roles

The system supports three types of user roles:

1. **Regular Users** - Can manage their own account, make transfers, and view their transaction history.

2. **Admin Users** - Have all regular user privileges plus:
   - Approve/reject new user registrations
   - Activate/deactivate user accounts
   - Create new user accounts
   - Make deposits to user accounts
   - Edit user information

3. **Manager Users** - Have all admin privileges plus:
   - Create and manage admin accounts
   - View admin transaction logs
   - Monitor all system transfers
   - System-wide oversight capabilities

---

## Address Management with PSGC API

The application integrates with the Philippine Standard Geographic Code (PSGC) API to provide standardized address selection for user profiles. The address system follows the Philippine geographical hierarchy:

- Region
- Province
- City/Municipality
- Barangay

This integration ensures addresses are standardized and validates location data according to the Philippine geographical structure.

---

## Technologies Used

- **Backend**: Python, Flask
- **Database**: MySQL (with SQLAlchemy ORM)
- **Frontend**: HTML, CSS, Bootstrap 5
- **Authentication**: Flask-Login, Werkzeug, Flask-Bcrypt
- **Forms**: Flask-WTF, WTForms
- **Security**: Flask-Limiter for API rate limiting, CSRF protection
- **External API**: PSGC API for Philippine geographic data

---

## Rate Limiting

The application uses Flask-Limiter to implement API rate limiting, which protects against potential DoS attacks and abusive bot activity. The rate limits are configured as follows:

- **Login**: 10 attempts per minute
- **Registration**: 5 attempts per minute
- **Password Reset**: 5 attempts per hour
- **Money Transfer**: 20 attempts per hour
- **API Endpoints**: 30 requests per minute
- **Admin Dashboard**: 60 requests per hour
- **Admin Account Creation**: 20 accounts per hour
- **Admin Deposits**: 30 deposits per hour
- **Manager Dashboard**: 60 requests per hour
- **Admin Creation**: 10 admin accounts per hour

By default, the rate limiting data is stored in memory. For production use, it's recommended to use Redis as a storage backend for persistence across application restarts. To enable Redis storage:

1. Install Redis server on your system
2. Update the `.env` file with your Redis URL:
   ```
   REDIS_URL=redis://localhost:6379/0
   ```

If Redis is not available, the application will automatically fall back to in-memory storage.

---

## License

This project is licensed under the MIT License - see the LICENSE file for details.
