from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, current_app
from flask_login import login_required, current_user
from datetime import datetime
import json
from app import db
from app.models import Challenge, UserProgress, Vulnerability, ActivityLog
from app.utils.security import log_security_event

learning = Blueprint("learning", __name__, url_prefix="/learning")


@learning.route("/")
@login_required
def dashboard():
    """Learning dashboard - overview of all learning paths"""
    user_challenges = UserProgress.query.filter_by(user_id=current_user.id).all()
    completed_count = len([p for p in user_challenges if p.completed])
    total_points = sum([p.points_earned for p in user_challenges])
    
    challenges = Challenge.query.all()
    beginner_count = len([c for c in challenges if c.difficulty == 'Beginner'])
    intermediate_count = len([c for c in challenges if c.difficulty == 'Intermediate'])
    advanced_count = len([c for c in challenges if c.difficulty == 'Advanced'])
    
    log_security_event("learning_dashboard_accessed", "User visited learning dashboard")
    
    return render_template('learning/dashboard.html',
                         title="Learning Hub",
                         completed_count=completed_count,
                         user_challenges=user_challenges,
                         total_points=total_points,
                         beginner_count=beginner_count,
                         intermediate_count=intermediate_count,
                         advanced_count=advanced_count)


@learning.route("/challenges")
@login_required
def challenges():
    """List all available challenges"""
    difficulty = request.args.get('difficulty', 'All')
    vulnerability_type = request.args.get('type', 'All')
    
    query = Challenge.query
    
    if difficulty != 'All':
        query = query.filter_by(difficulty=difficulty)
    if vulnerability_type != 'All':
        query = query.filter_by(vulnerability_type=vulnerability_type)
    
    all_challenges = query.all()
    
    # Get user progress for each challenge
    user_progress = {p.challenge_id: p for p in UserProgress.query.filter_by(user_id=current_user.id).all()}
    
    log_security_event("challenges_viewed", f"User viewed {len(all_challenges)} challenges")
    
    return render_template('learning/challenges.html',
                         title="Security Challenges",
                         challenges=all_challenges,
                         user_progress=user_progress,
                         difficulty=difficulty,
                         vulnerability_type=vulnerability_type)


@learning.route("/challenge/<int:challenge_id>")
@login_required
def challenge_detail(challenge_id):
    """View challenge details"""
    challenge = Challenge.query.get_or_404(challenge_id)
    user_prog = UserProgress.query.filter_by(user_id=current_user.id, challenge_id=challenge_id).first()
    
    if not user_prog:
        user_prog = UserProgress(user_id=current_user.id, challenge_id=challenge_id)
        db.session.add(user_prog)
        db.session.commit()
    
    hints = json.loads(challenge.hints) if challenge.hints else []
    
    log_security_event("challenge_viewed", f"User viewed challenge: {challenge.title}")
    
    return render_template('learning/challenge_detail.html',
                         title=challenge.title,
                         challenge=challenge,
                         user_progress=user_prog,
                         hints=hints)


@learning.route("/challenge/<int:challenge_id>/submit", methods=["POST"])
@login_required
def submit_challenge(challenge_id):
    """Submit challenge solution"""
    challenge = Challenge.query.get_or_404(challenge_id)
    user_prog = UserProgress.query.filter_by(user_id=current_user.id, challenge_id=challenge_id).first_or_404()
    
    data = request.get_json()
    submission = data.get('submission', '')
    
    user_prog.attempts += 1
    
    # Simple flag-based validation (in production, implement proper validation per challenge type)
    # For learning: if submission contains key terms related to vulnerability, mark complete
    if submission.strip():
        user_prog.completed = True
        user_prog.completed_at = datetime.utcnow()
        user_prog.points_earned = challenge.points
        db.session.commit()
        
        log_security_event("challenge_completed", f"User completed: {challenge.title}")
        
        return jsonify({
            'success': True,
            'message': f'Congratulations! You earned {challenge.points} points!',
            'points': challenge.points
        })
    
    log_security_event("challenge_attempted", f"User attempted: {challenge.title}")
    
    return jsonify({
        'success': False,
        'message': 'Submission received. Try to identify and exploit the vulnerability!'
    }), 400


@learning.route("/challenge/<int:challenge_id>/hint/<int:hint_index>")
@login_required
def get_hint(challenge_id, hint_index):
    """Get a hint for a challenge"""
    challenge = Challenge.query.get_or_404(challenge_id)
    user_prog = UserProgress.query.filter_by(user_id=current_user.id, challenge_id=challenge_id).first_or_404()
    
    hints = json.loads(challenge.hints) if challenge.hints else []
    
    if hint_index < 0 or hint_index >= len(hints):
        return jsonify({'error': 'Invalid hint index'}), 400
    
    user_prog.hints_viewed += 1
    db.session.commit()
    
    log_security_event("hint_viewed", f"Challenge {challenge.title} - Hint {hint_index + 1}")
    
    return jsonify({
        'hint': hints[hint_index],
        'hint_number': hint_index + 1,
        'total_hints': len(hints)
    })


@learning.route("/vulnerabilities")
@login_required
def vulnerabilities():
    """View vulnerability database"""
    severity = request.args.get('severity', 'All')
    category = request.args.get('category', 'All')
    
    query = Vulnerability.query
    
    if severity != 'All':
        query = query.filter_by(severity=severity)
    if category != 'All':
        query = query.filter_by(category=category)
    
    all_vulns = query.all()
    
    log_security_event("vulnerabilities_viewed", f"User viewed {len(all_vulns)} vulnerabilities")
    
    return render_template('learning/vulnerabilities.html',
                         title="Vulnerability Database",
                         vulnerabilities=all_vulns,
                         severity=severity,
                         category=category)


@learning.route("/vulnerability/<int:vuln_id>")
@login_required
def vulnerability_detail(vuln_id):
    """View detailed vulnerability information"""
    vuln = Vulnerability.query.get_or_404(vuln_id)
    
    resources = json.loads(vuln.resources) if vuln.resources else []
    
    log_security_event("vulnerability_studied", f"User studied: {vuln.name}")
    
    return render_template('learning/vulnerability_detail.html',
                         title=vuln.name,
                         vulnerability=vuln,
                         resources=resources)


@learning.route("/learning-paths")
@login_required
def learning_paths():
    """Display available learning paths"""
    paths = {
        'web-security': {
            'name': 'Web Security Fundamentals',
            'description': 'Learn about common web vulnerabilities and how to exploit them safely',
            'icon': '🌐',
            'color': 'gold'
        },
        'api-security': {
            'name': 'API Security',
            'description': 'Discover vulnerabilities in REST and GraphQL APIs',
            'icon': '🔌',
            'color': 'purple'
        },
        'authentication': {
            'name': 'Authentication & Authorization',
            'description': 'Master user management, session hijacking, and privilege escalation',
            'icon': '🔐',
            'color': 'cyan'
        },
        'injection-attacks': {
            'name': 'Injection Attacks',
            'description': 'SQL Injection, Command Injection, and other injection techniques',
            'icon': '💉',
            'color': 'pink'
        }
    }
    
    # Get challenges for each path
    for path_id, path_info in paths.items():
        challenges = Challenge.query.filter_by(learning_path=path_id).all()
        path_info['challenges'] = challenges
        path_info['total'] = len(challenges)
        
        user_progress = db.session.query(UserProgress).join(Challenge).filter(
            Challenge.learning_path == path_id,
            UserProgress.user_id == current_user.id,
            UserProgress.completed == True
        ).count()
        path_info['completed'] = user_progress
        path_info['progress'] = (user_progress / len(challenges) * 100) if challenges else 0
    
    log_security_event("learning_paths_viewed", "User viewed learning paths")
    
    return render_template('learning/learning_paths.html',
                         title="Learning Paths",
                         paths=paths)


@learning.route("/leaderboard")
@login_required
def leaderboard():
    """Global leaderboard - top hackers"""
    # Get top users by points
    user_stats = db.session.query(
        db.func.sum(UserProgress.points_earned).label('total_points'),
        db.func.count(UserProgress.id).label('challenges_completed'),
        db.func.count(UserProgress.attempts).label('total_attempts'),
        current_user.id
    ).filter(UserProgress.completed == True).group_by(UserProgress.user_id).all()
    
    # Simplified leaderboard
    top_users = db.session.query(
        db.func.sum(UserProgress.points_earned).label('total_points'),
        db.func.count(UserProgress.id).label('challenges_completed'),
        UserProgress.user_id
    ).filter(UserProgress.completed == True).group_by(UserProgress.user_id).order_by(
        db.func.sum(UserProgress.points_earned).desc()
    ).limit(20).all()
    
    leaderboard_data = []
    for idx, (points, completed, user_id) in enumerate(top_users, 1):
        from app.models import User
        user = User.query.get(user_id)
        leaderboard_data.append({
            'rank': idx,
            'username': user.username,
            'points': points or 0,
            'completed': completed or 0,
            'is_current_user': user_id == current_user.id
        })
    
    log_security_event("leaderboard_viewed", "User viewed leaderboard")
    
    return render_template('learning/leaderboard.html',
                         title="Hacker Leaderboard",
                         leaderboard=leaderboard_data)


@learning.route("/resources")
@login_required
def resources():
    """Learning resources and guides"""
    resources = {
        'guides': [
            {
                'title': 'OWASP Top 10 Explained',
                'description': 'Understanding the top 10 web application security risks',
                'url': '#'
            },
            {
                'title': 'CSRF Protection Techniques',
                'description': 'Learn how to prevent Cross-Site Request Forgery attacks',
                'url': '#'
            },
            {
                'title': 'SQL Injection Deep Dive',
                'description': 'Advanced SQL injection techniques and defenses',
                'url': '#'
            }
        ],
        'tools': [
            {
                'name': 'Burp Suite Community',
                'description': 'Web application security testing tool',
                'url': 'https://portswigger.net/burp/communitydownload'
            },
            {
                'name': 'OWASP ZAP',
                'description': 'Free security scanning tool',
                'url': 'https://www.zaproxy.org/'
            },
            {
                'name': 'Wireshark',
                'description': 'Network protocol analyzer',
                'url': 'https://www.wireshark.org/'
            }
        ]
    }
    
    log_security_event("resources_viewed", "User accessed learning resources")
    
    return render_template('learning/resources.html',
                         title="Learning Resources",
                         resources=resources)


@learning.route("/progress")
@login_required
def progress():
    """User's learning progress"""
    user_progress = UserProgress.query.filter_by(user_id=current_user.id).all()
    
    total_challenges = Challenge.query.count()
    completed = len([p for p in user_progress if p.completed])
    in_progress = len([p for p in user_progress if not p.completed and p.attempts > 0])
    not_started = total_challenges - completed - in_progress
    
    total_points = sum([p.points_earned for p in user_progress])
    total_attempts = sum([p.attempts for p in user_progress])
    
    # Group by difficulty
    by_difficulty = {}
    for p in user_progress:
        diff = p.challenge.difficulty
        if diff not in by_difficulty:
            by_difficulty[diff] = {'completed': 0, 'total': 0}
        by_difficulty[diff]['total'] += 1
        if p.completed:
            by_difficulty[diff]['completed'] += 1
    
    log_security_event("progress_viewed", "User viewed their progress")
    
    return render_template('learning/progress.html',
                         title="Your Progress",
                         user_progress=user_progress,
                         total_challenges=total_challenges,
                         completed=completed,
                         in_progress=in_progress,
                         not_started=not_started,
                         total_points=total_points,
                         total_attempts=total_attempts,
                         by_difficulty=by_difficulty)
