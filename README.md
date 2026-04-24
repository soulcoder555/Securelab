# SecureLab

A comprehensive, security-focused Flask web application featuring both a functional application and a **complete Hack The Box-style learning platform**. Learn cybersecurity by exploiting real vulnerabilities in a safe, educational environment.

## 🎓 🏛️ Learning Platform - NEW!

SecureLab now includes a **full-featured security learning platform** with royal aesthetic design.

### 📚 Learning Features

- **Interactive Challenges**: 5+ hands-on security challenges (XSS, SQL Injection, Authentication, etc.)
- **Vulnerability Database**: Learn about real security flaws with code examples
- **Structured Learning Paths**: 4 predefined learning tracks (Web Security, API Security, Authentication, Injection Attacks)
- **Gamification System**: Points, leaderboards, and progress tracking
- **Hint System**: Progressive hints to guide without spoiling
- **Write-ups**: Detailed explanations after challenge completion
- **Progress Analytics**: Visualize your security learning journey
- **Leaderboard**: Compete with other learners

### 🎮 Quick Start - Learning Platform

1. **Log in** to your account
2. Click **"🎓 Learn"** in the navigation menu
3. Choose from:
   - **Challenges** → Practice extracting real vulnerabilities
   - **Learning Paths** → Follow structured curricula
   - **Vulnerabilities** → Study security flaws in depth
   - **Leaderboard** → Compete globally
   - **Progress** → Track your learning

### 📖 Documentation

- **[LEARNING_PLATFORM_GUIDE.md](LEARNING_PLATFORM_GUIDE.md)** - Comprehensive user guide (50+ pages)
- **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - Quick access card
- **[PLATFORM_BUILD_SUMMARY.md](PLATFORM_BUILD_SUMMARY.md)** - Technical architecture

### 💎 Royal Aesthetic

The platform features an elegant **royal futuristic design**:
- Gold and purple color scheme
- Sophisticated animations and glows
- Professional typography
- Clean, organized layout
- Fully responsive design

## 🚀 Features

### Core Application
- **User Authentication**: Secure registration, login, and logout with Flask-Login
- **Role-Based Access Control**: User and admin roles with protected routes
- **Notes/Task Management**: Create, edit, delete, and search notes
- **Secure File Upload**: Safe file handling with type validation and size limits
- **Activity Logging**: Comprehensive audit trail for security monitoring
- **Search & Filter**: Full-text search across user content
- **Security Headers**: HTTP security headers with Flask-Talisman
- **Input Validation**: Comprehensive input sanitization and validation
- **Session Protection**: Secure session management with CSRF protection

### Learning Platform
- **5+ Ready-to-Use Challenges** with hints and write-ups
- **Vulnerability Knowledge Base** with code examples
- **Interactive Challenge Workspace** with hint system
- **Global Leaderboard** for competitive learning
- **Personal Progress Dashboard** with analytics
- **Learning Resource Library** with tools and guides

## 🛡️ Security Features

### Threat Model

**Assets to Protect:**
- User accounts and authentication
- User-generated content (notes, files)
- System integrity and availability
- Audit logs and activity monitoring

**Potential Threats:**
- Unauthorized access (authentication bypass)
- Data injection (SQL injection, XSS)
- Session hijacking and fixation
- File upload vulnerabilities
- CSRF attacks
- Information disclosure

### Security by Design

- **Defense in Depth**: Multiple security layers (authentication, authorization, validation, sanitization)
- **Principle of Least Privilege**: Users can only access their own data
- **Fail-Safe Defaults**: Secure defaults with explicit opt-in for risky features
- **Input Validation**: All user input is validated and sanitized
- **Secure Headers**: Comprehensive HTTP security headers
- **Session Security**: Secure session configuration with proper timeouts
- **Audit Logging**: All security-relevant actions are logged

### How This Project Teaches Security

1. **Authentication & Authorization**: Learn proper session management and role-based access
2. **Input Validation**: See real-world input sanitization and validation patterns
3. **File Upload Security**: Understand safe file handling and storage
4. **CSRF Protection**: Experience CSRF token implementation
5. **Security Headers**: Learn about HTTP security headers and their importance
6. **Audit Trails**: Understand the importance of logging for security monitoring
7. **Secure Coding Patterns**: See secure coding practices throughout the codebase

## 📋 Requirements

- Python 3.8+
- pip
- Virtual environment (recommended)

## 🛠️ Installation

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/securelab.git
   cd securelab
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

5. **Initialize database**
   ```bash
   make init-db
   ```

6. **Create admin user**
   ```bash
   make create-admin
   ```

7. **Run the application**
   ```bash
   make run
   ```

   Visit `http://127.0.0.1:5000`

### Docker Deployment

```bash
# Build and run with Docker Compose
make docker-run

# Or manually:
docker-compose up --build
```

## 🧪 Testing

```bash
# Run all tests
make test

# Run with coverage
make test-cov
```

## 📁 Project Structure

```
securelab/
├── app/
│   ├── __init__.py              # App factory
│   ├── extensions.py            # Flask extensions
│   ├── config.py                # Configuration classes
│   ├── models.py                # SQLAlchemy models
│   │
│   ├── blueprints/
│   │   ├── auth/                # Authentication routes
│   │   ├── core/                # Main application routes
│   │   └── admin/               # Admin panel routes
│   │
│   ├── static/
│   │   ├── css/                 # Stylesheets
│   │   └── uploads/             # File uploads
│   │
│   ├── templates/               # Jinja2 templates
│   └── utils/                   # Utility functions
│
├── tests/                       # Test suite
├── .env.example                 # Environment template
├── docker-compose.yml           # Docker configuration
├── Dockerfile                   # Docker image
├── Makefile                     # Development shortcuts
├── requirements.txt             # Python dependencies
├── README.md                    # This file
└── wsgi.py                      # Production entry point
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | Flask secret key | Required |
| `DATABASE_URL` | Database connection string | `sqlite:///app.db` |
| `TRAINING_MODE` | Enable security training features | `false` |

### Security Settings

- **Session Timeout**: 30 minutes
- **File Upload Limit**: 16MB
- **Allowed File Types**: txt, pdf, png, jpg, jpeg, gif
- **Password Requirements**: Minimum 8 characters
- **CSRF Protection**: Enabled on all forms

## 🚦 Usage

### User Registration & Login

1. Visit the application
2. Click "Register" to create a new account
3. Login with your credentials
4. Access your personal dashboard

### Managing Notes

- Create new notes with title and content
- Mark notes as completed
- Edit existing notes
- Delete notes you no longer need
- Search through your notes

### File Upload

- Upload files securely (max 16MB)
- Only allowed file types accepted
- View uploaded files
- Files stored in `app/static/uploads/`

### Admin Features

- Access admin panel (admin role required)
- View all users
- Manage user roles and status
- Monitor system activity logs

## 🔍 API Endpoints

### Authentication
- `GET/POST /auth/login` - User login
- `GET/POST /auth/register` - User registration
- `GET /auth/logout` - User logout

### Core Features
- `GET /` - Home dashboard
- `GET/POST /notes` - List/create notes
- `GET/POST /notes/<id>/edit` - Edit note
- `POST /notes/<id>/delete` - Delete note
- `GET/POST /upload` - File upload
- `GET /uploads/<filename>` - View uploaded file
- `GET/POST /search` - Search notes

### Admin
- `GET /admin/dashboard` - Admin panel
- `GET/POST /admin/users/<id>` - Manage user
- `POST /admin/users/<id>/toggle` - Activate/deactivate user

## 🧪 Security Testing

### Training Mode

Enable training mode to explore common security issues:

```bash
export TRAINING_MODE=true
flask --app wsgi:app run
```

This enables educational endpoints that demonstrate (but don't exploit) security concepts.

### Manual Testing

1. **Authentication Testing**
   - Try SQL injection in login form
   - Test session fixation
   - Attempt unauthorized access

2. **Input Validation**
   - Submit XSS payloads
   - Test file upload restrictions
   - Try directory traversal

3. **CSRF Testing**
   - Attempt cross-site request forgery
   - Verify CSRF token validation

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Write tests for new features
4. Ensure all tests pass
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚠️ Disclaimer

This application is for educational purposes. While it implements security best practices, no software is completely secure. Always follow security best practices and keep dependencies updated.

## 📚 Further Reading

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Flask Security Documentation](https://flask.palletsprojects.com/en/2.0.x/security/)
- [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/)
- [Secure Coding Practices](https://www.owasp.org/index.php/Secure_Coding_Practices_Quick_Reference_Guide) 
