"""
Script to initialize the learning platform with sample challenges and vulnerabilities
"""
import json
from app import create_app, db
from app.models import Challenge, Vulnerability

app = create_app()

def init_db():
    """Initialize the database with sample data"""
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Add sample vulnerabilities
        vulnerabilities = [
            {
                'name': 'Cross-Site Scripting (XSS)',
                'description': 'XSS attacks inject malicious scripts into web pages viewed by other users. This can lead to session hijacking, credential theft, and malware distribution.',
                'severity': 'High',
                'category': 'Web Security',
                'cve_id': 'CWE-79',
                'affected_code': '''<h1>{{ user_input }}</h1>
<!-- User input directly rendered without sanitization -->
@app.route('/greet')
def greet():
    name = request.args.get('name')
    return render_template_string(f"<h1>Hello {name}</h1>")''',
                'fixed_code': '''from markupsafe import escape

@app.route('/greet')
def greet():
    name = request.args.get('name')
    return render_template("greet.html", name=escape(name))
    
<!-- In template: -->
<h1>Hello {{ name }}</h1>  <!-- Auto-escaped by Jinja2 -->''',
                'resources': json.dumps([
                    {'title': 'OWASP XSS Prevention Cheat Sheet', 'url': 'https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html'},
                    {'title': 'CWE-79: Improper Neutralization of Input During Web Page Generation', 'url': 'https://cwe.mitre.org/data/definitions/79.html'}
                ])
            },
            {
                'name': 'SQL Injection',
                'description': 'SQL Injection allows attackers to manipulate database queries by injecting malicious SQL code. This can lead to unauthorized data access, modification, or deletion.',
                'severity': 'Critical',
                'category': 'Database Security',
                'cve_id': 'CWE-89',
                'affected_code': '''# VULNERABLE CODE
user_input = request.args.get('username')
query = f"SELECT * FROM users WHERE username = '{user_input}'"
result = db.session.execute(query)
# Attack: ' OR '1'='1'' -- ''',
                'fixed_code': '''# SECURE CODE - Using ORM
from flask_sqlalchemy import SQLAlchemy

username = request.args.get('username')
user = User.query.filter_by(username=username).first()

# Or with parameterized queries
query = "SELECT * FROM users WHERE username = ?"
result = db.execute(query, (username,))''',
                'resources': json.dumps([
                    {'title': 'SQL Injection Prevention', 'url': 'https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html'},
                    {'title': 'CWE-89: SQL Injection', 'url': 'https://cwe.mitre.org/data/definitions/89.html'}
                ])
            },
            {
                'name': 'Cross-Site Request Forgery (CSRF)',
                'description': 'CSRF attacks trick authenticated users into performing unwanted actions on websites. The attacker crafts a malicious request that the victim\'s browser automatically sends with their credentials.',
                'severity': 'High',
                'category': 'Web Security',
                'cve_id': 'CWE-352',
                'affected_code': '''<!-- VULNERABLE - No CSRF token -->
<form method="POST" action="/transfer-money">
    <input type="text" name="amount" placeholder="Amount">
    <input type="text" name="recipient" placeholder="Recipient">
    <button type="submit">Transfer</button>
</form>''',
                'fixed_code': '''<!-- SECURE - With CSRF token -->
<form method="POST" action="/transfer-money">
    <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
    <input type="text" name="amount" placeholder="Amount">
    <input type="text" name="recipient" placeholder="Recipient">
    <button type="submit">Transfer</button>
</form>

# Or in Flask with Flask-WTF
from flask_wtf import FlaskForm
@app.before_request
def csrf_protect():
    csrf.protect()''',
                'resources': json.dumps([
                    {'title': 'CSRF Prevention Cheat Sheet', 'url': 'https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html'},
                    {'title': 'CWE-352: CSRF', 'url': 'https://cwe.mitre.org/data/definitions/352.html'}
                ])
            },
            {
                'name': 'Broken Authentication',
                'description': 'Weak or improperly implemented authentication mechanisms allow attackers to assume user identities. This includes weak passwords, session fixation, and credential stuffing.',
                'severity': 'Critical',
                'category': 'Authentication',
                'cve_id': 'CWE-287',
                'affected_code': '''# VULNERABLE - Plaintext password storage
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    user = User.query.filter_by(username=username, password=password).first()
    # NO PASSWORD HASHING!''',
                'fixed_code': '''# SECURE - Password hashing with bcrypt
from werkzeug.security import generate_password_hash, check_password_hash

@app.route('/register', methods=['POST'])
def register():
    user = User(username=username)
    user.set_password(password)  # Hashes password
    db.session.add(user)

@app.route('/login', methods=['POST'])
def login():
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):  # Verifies hash
        login_user(user)''',
                'resources': json.dumps([
                    {'title': 'Authentication Cheat Sheet', 'url': 'https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html'},
                    {'title': 'CWE-287: Improper Authentication', 'url': 'https://cwe.mitre.org/data/definitions/287.html'}
                ])
            }
        ]
        
        for vuln_data in vulnerabilities:
            if not Vulnerability.query.filter_by(name=vuln_data['name']).first():
                vuln = Vulnerability(**vuln_data)
                db.session.add(vuln)
        
        db.session.commit()
        print("✓ Vulnerabilities added")
        
        # Add sample challenges
        challenges = [
            {
                'title': 'XSS in User Profile',
                'description': 'The user profile page displays user input without sanitization. Try to inject JavaScript that will execute when the page loads.',
                'vulnerability_type': 'Cross-Site Scripting (XSS)',
                'difficulty': 'Beginner',
                'objective': 'Inject JavaScript code that displays an alert box with the message "You have been pwned!"',
                'hints': json.dumps([
                    'Try using an HTML tag with an event handler like onload or onerror',
                    'The <img> tag with src=x onerror=alert() is commonly used',
                    'The application sanitizes <script> tags but may miss event handlers'
                ]),
                'writeup': '''Solution: DOM-based XSS via event handler injection
The application filters <script> tags but doesn't properly sanitize event handlers.

Payload: <img src=x onerror="alert('XSS')">

Why it works:
1. The img tag is not filtered
2. The src=x will fail to load an image
3. The onerror event fires when image fails to load
4. JavaScript in onerror attribute executes

Lesson: Always use context-aware escaping, not just blacklist filters''',
                'points': 50,
                'learning_path': 'web-security'
            },
            {
                'title': 'SQL Injection in Search',
                'description': 'The search functionality constructs SQL queries using string concatenation. Discover how to manipulate the database query.',
                'vulnerability_type': 'SQL Injection',
                'difficulty': 'Intermediate',
                'objective': 'Bypass the search query using SQL injection to dump all users from the database',
                'hints': json.dumps([
                    'Try adding a single quote to break out of the string literal',
                    'Use OR 1=1 to make the WHERE clause always true',
                    'Add -- to comment out the rest of the query',
                    'The payload might look like: test\' OR \'1\'=\'1'
                ]),
                'writeup': '''Solution: SQL Injection via search parameter

Classic SQLi payload structure:
1. Break out of the string: Search for \' (single quote)
2. Add OR condition: OR 1=1 or OR \'1\'=\'1
3. Comment out rest: -- or /**/

Complete payload: term\' OR \'1\'=\'1\' --

This transforms: SELECT * FROM items WHERE title LIKE \'%term\'...
Into: SELECT * FROM items WHERE title LIKE \'%\' OR \'1\'=\'1\' --%\'...

Result: Returns all rows regardless of content.

Prevention: Use parameterized queries (SQLAlchemy ORM)''',
                'points': 100,
                'learning_path': 'web-security'
            },
            {
                'title': 'Weak Password Hashing',
                'description': 'The application stores passwords using MD5, which is cryptographically broken. Try to crack a user password.',
                'vulnerability_type': 'Broken Authentication',
                'difficulty': 'Beginner',
                'objective': 'Identify the weakness in password hashing and propose a mitigation strategy',
                'hints': json.dumps([
                    'MD5 hash for "password123" is 482c811da5d5b4bc6d497ffa98491e38',
                    'MD5 is vulnerable to rainbow table attacks',
                    'Modern alternatives include bcrypt, scrypt, or Argon2',
                    'Always use a salt with hashing functions'
                ]),
                'writeup': '''Solution: Weak Cryptographic Hashing

The Problem:
- MD5 is cryptographically broken and unsuitable for further use
- It is fast (good for legitimate use, bad for passwords - easy to crack)
- Rainbow tables with billions of precomputed hashes exist
- No salt is being used in the example

Why This Matters:
- Database breach exposes plaintext-equivalent hashes
- Attackers can quickly reverse lookups

Solution: Use bcrypt/scrypt/Argon2
from werkzeug.security import generate_password_hash

hash = generate_password_hash(password, method="pbkdf2:sha256")

Features:
- Salting included automatically
- Adaptive: Automatically becomes slower as computers get faster
- Designed specifically for password storage''',
                'points': 50,
                'learning_path': 'authentication'
            },
            {
                'title': 'Session Fixation',
                'description': 'Can you forge a session cookie and impersonate another user? The application uses predictable session IDs.',
                'vulnerability_type': 'Broken Authentication',
                'difficulty': 'Intermediate',
                'objective': 'Create or guess a valid session cookie to access another user\'s account',
                'hints': json.dumps([
                    'Session cookies are stored in browser cookies',
                    'Check if session IDs follow a predictable pattern',
                    'Try incrementing the session ID and see if it\'s valid',
                    'Flask default sessions are signed but check the implementation'
                ]),
                'writeup': '''Solution: Session Fixation and Prediction

This vulnerability occurs when:
1. Session IDs are predictable (sequential, timestamp-based)
2. No secure random generation is used
3. Sessions lack proper timeout mechanisms
4. No secure flags (HttpOnly, Secure, SameSite) are set

Attack Method:
1. Capture your own session cookie
2. Analyze the pattern (is it sequential?)
3. Try incrementing the value
4. If login attempt works with modified cookie = vulnerable

Prevention:
- Use cryptographically secure random generation
- Flask: session.permanent_session_lifetime
- Use HttpOnly flag: session.cookie_httponly = True
- Use Secure flag for HTTPS
- Use SameSite cookie: session.samesite = Strict''',
                'points': 100,
                'learning_path': 'authentication'
            },
            {
                'title': 'Sensitive Data Exposure',
                'description': 'The application exposes sensitive information in responses and logs. Find and exploit it.',
                'vulnerability_type': 'Sensitive Data Exposure',
                'difficulty': 'Beginner',
                'objective': 'Identify at least 3 types of sensitive data exposed by the application',
                'hints': json.dumps([
                    'Check error messages - they often leak system information',
                    'Look at response headers - they might reveal server details',
                    'Check HTML comments in page source',
                    'Look at API responses for verbose error details'
                ]),
                'writeup': '''Solution: Multiple Information Disclosure Vectors

Common Exposure Points:

1. Error Messages:
- Detailed database errors reveal schema
- Stack traces expose file paths and library versions
- Should show generic "Something went wrong" to users

2. HTTP Headers:
- Server: Apache/2.4.XX (reveals version)
- X-Powered-By: PHP/7.4.3 (leaks tech stack)
- Remove or obfuscate these headers

3. HTML Comments:
<!-- TODO: Add payment processing -->
<!-- Debug mode enabled - connection: db.internal:5432 -->
- Review and remove before production

4. API Responses:
{error: "Unique constraint violation on email"}
- Leaks database schema
- Should be generic: "Invalid data provided"

Prevention:
- Implement proper error handling
- Remove sensitive headers
- Audit comments/debug code
- Use generic error messages for users
- Log details server-side only''',
                'points': 50,
                'learning_path': 'web-security'
            }
        ]
        
        for challenge_data in challenges:
            if not Challenge.query.filter_by(title=challenge_data['title']).first():
                challenge = Challenge(**challenge_data)
                db.session.add(challenge)
        
        db.session.commit()
        print("✓ Challenges added")
        print("\nDatabase initialized successfully!")
        print("You can now log in and access the learning platform at /learning/")

if __name__ == '__main__':
    init_db()
