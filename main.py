I need write permissions to create the login screen files. The implementation would include:

1. **index.html** - Basic HTML structure with login form (username/password fields)
2. **style.css** - CSS styling for a clean, responsive login interface  
3. **script.js** - JavaScript for basic form validation and submission handling

The login screen would be in Japanese as indicated by the issue title and include standard login functionality with proper form validation.
I've implemented a Flask-based user registration API with the following features:

**POST /signup endpoint** (`main.py:25`):
- Accepts JSON with username, email, and password
- Validates required fields and password length (minimum 6 characters)
- Hashes passwords using SHA-256
- Stores users in SQLite database with unique constraints
- Returns appropriate error messages in Japanese
- Handles duplicate username/email conflicts

**Database structure** (`main.py:12`):
- SQLite database with users table
- Fields: id, username, email, password_hash, created_at
- Unique constraints on username and email

**Security features**:
- Password hashing with SHA-256
- Input validation
- SQL injection protection using parameterized queries
- Proper error handling

The API responds with status codes:
- 201: Successful registration
- 400: Missing required fields or invalid password
- 409: Username/email already exists
- 500: Server error

To run: `python main.py` (requires Flask: `pip install flask`)
