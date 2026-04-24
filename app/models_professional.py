"""
Professional Learning Platform Models
=====================================

Core philosophy: Track UNDERSTANDING, not just completion.
Every model serves the guided reasoning experience.

Entity Relationships:
  VulnerabilityTopic (with teaching backbone)
    ├── GuidedLesson (step-by-step flows)
    │   ├── LessonStep (atomic reasoning steps)
    │   ├── SocraticQuestion (predict-then-explain)
    │   ├── SafeScenario (interactive demos)
    │   └── ComparisonNote (real-world differences)
    ├── SkillGraph (prerequisites & relationships)
    ├── Misconception (common wrong assumptions)
    └── LessonVersion (versioning & history)
  
  StudentLearningProgress
    ├── TopicMastery (understanding level per topic)
    ├── StepCompletion (which steps, which hints needed)
    ├── MisconceptionEncounter (did student hit this error?)
    ├── StudentReflection (teach-back explanations)
    └── RevisionDue (spaced repetition scheduling)
"""

from datetime import datetime, timedelta
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import json

from app.extensions import db


# ============================================================================
# EXISTING MODELS (Keep These)
# ============================================================================

class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), default='user', nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    
    # Learning profile
    skill_level = db.Column(db.String(20), default='beginner')  # beginner, intermediate, advanced
    learning_style_preference = db.Column(db.String(50))  # socratic, visual, hands-on
    last_learning_at = db.Column(db.DateTime)

    notes = db.relationship('Note', backref='author', lazy='dynamic')
    activities = db.relationship('ActivityLog', backref='user', lazy='dynamic')
    learning_progress = db.relationship('StudentLearningProgress', backref='student', lazy='dynamic')
    topic_mastery = db.relationship('TopicMastery', backref='student', lazy='dynamic')
    reflections = db.relationship('StudentReflection', backref='author', lazy='dynamic')
    misconception_encounters = db.relationship('MisconceptionEncounter', backref='student', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_admin(self):
        return self.role == 'admin'

    def __repr__(self):
        return f"<User {self.username}>"


class Note(db.Model):
    __tablename__ = "notes"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    is_completed = db.Column(db.Boolean, default=False, nullable=False)

    def __repr__(self):
        return f"<Note {self.title}>"


class ActivityLog(db.Model):
    __tablename__ = "activity_logs"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    action = db.Column(db.String(100), nullable=False)
    details = db.Column(db.Text)
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<ActivityLog {self.action}>"


# ============================================================================
# NEW PROFESSIONAL LEARNING MODELS
# ============================================================================

class VulnerabilityTopic(db.Model):
    """
    Core teaching entity. Not just a vulnerability description,
    but a complete pedagogical object with teaching backbone.
    
    Teaching layers:
    1. Simple concept explanation
    2. Root cause (why it exists)
    3. Mental model (how attacker thinks)
    4. Detection clues (how to spot it)
    5. Real-world variations
    6. Defense strategies
    """
    __tablename__ = "vulnerability_topics"

    id = db.Column(db.Integer, primary_key=True)
    
    # Basic metadata
    title = db.Column(db.String(200), nullable=False, unique=True)  # e.g., "SQL Injection"
    slug = db.Column(db.String(200), unique=True, index=True)  # e.g., "sql-injection"
    severity = db.Column(db.String(20))  # Critical, High, Medium, Low
    category = db.Column(db.String(100))  # Injection, Broken Auth, XSS, etc.
    cve_ids = db.Column(db.Text)  # JSON array of CVE IDs
    
    # Teaching backbone (these are the pedagogical layers)
    concept_explanation_simple = db.Column(db.Text, nullable=False)  # Plain language "what"
    concept_explanation_detailed = db.Column(db.Text)  # Deeper dive into mechanics
    
    root_cause = db.Column(db.Text, nullable=False)  # WHY this vulnerability exists
    
    mental_model = db.Column(db.Text)  # How does an attacker think about this?
    mental_model_diagram_url = db.Column(db.String(500))  # Visual representation
    
    detection_thought_process = db.Column(db.Text)  # Step-by-step: how to identify?
    detection_clues = db.Column(db.Text)  # JSON array of observable signals
    
    # Real-world context
    real_world_scenarios = db.Column(db.Text)  # JSON: examples in actual applications
    common_implementations = db.Column(db.Text)  # How it appears in the wild
    
    # Defense strategies
    defense_primary = db.Column(db.Text)  # Main defense mechanism
    defense_alternatives = db.Column(db.Text)  # JSON array of alternative defenses
    defense_tradeoffs = db.Column(db.Text)  # What are the tradeoffs?
    
    # Content management
    difficulty_min = db.Column(db.String(20), default='beginner')
    difficulty_max = db.Column(db.String(20), default='advanced')
    estimated_learning_hours = db.Column(db.Float, default=1.5)
    prerequisites_json = db.Column(db.Text)  # JSON: prerequisite skill IDs
    
    is_published = db.Column(db.Boolean, default=False)
    created_by_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    version = db.Column(db.Integer, default=1)
    
    # Relationships
    guided_lessons = db.relationship('GuidedLesson', backref='topic', lazy='dynamic', cascade='all, delete-orphan')
    skill_graph_nodes = db.relationship('SkillGraph', backref='topic', lazy='dynamic', cascade='all, delete-orphan')
    misconceptions = db.relationship('Misconception', backref='topic', lazy='dynamic', cascade='all, delete-orphan')
    comparison_notes = db.relationship('ComparisonNote', backref='topic', lazy='dynamic', cascade='all, delete-orphan')
    topic_mastery = db.relationship('TopicMastery', backref='topic', lazy='dynamic', cascade='all, delete-orphan')
    versions = db.relationship('LessonVersion', backref='topic', lazy='dynamic', cascade='all, delete-orphan')

    def get_prerequisites(self):
        """Return list of prerequisite topic IDs"""
        if self.prerequisites_json:
            return json.loads(self.prerequisites_json)
        return []
    
    def get_detection_clues(self):
        """Return structured detection clues"""
        if self.detection_clues:
            return json.loads(self.detection_clues)
        return []

    def __repr__(self):
        return f"<VulnerabilityTopic {self.title}>"


class SkillGraph(db.Model):
    """
    Prerequisite mapping and skill relationships.
    Shows what skills are needed, what they enable, related concepts.
    """
    __tablename__ = "skill_graph"

    id = db.Column(db.Integer, primary_key=True)
    
    topic_id = db.Column(db.Integer, db.ForeignKey('vulnerability_topics.id'), nullable=False)
    
    # Relationship types
    relationship_type = db.Column(db.String(50), nullable=False)  # 'prerequisite', 'related', 'buildsOn', 'enablesDefense'
    
    # What's the related skill?
    prerequisite_topic_id = db.Column(db.Integer)  # If this is a prerequisite edge
    prerequisite_topic_name = db.Column(db.String(200))  # Cached name for quick lookup
    
    # Why is this relationship important?
    relationship_description = db.Column(db.Text)  # "Understanding X helps you recognize Y"
    suggested_order = db.Column(db.Integer)  # For rendering learning paths
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<SkillGraph {self.topic_id}->{self.prerequisite_topic_id}>"


class GuidedLesson(db.Model):
    """
    A complete lesson = step-by-step guided reasoning flow
    Not a challenge to solve blindly, but a structured thought journey
    
    Structure:
    - Intro (set context)
    - Series of LessonSteps (atomic reasoning tasks)
    - Comparisons (real-world differences shown at appropriate moments)
    - SocraticQuestions (predict before revealing)
    - Reflection checkpoint (teach-back)
    """
    __tablename__ = "guided_lessons"

    id = db.Column(db.Integer, primary_key=True)
    
    topic_id = db.Column(db.Integer, db.ForeignKey('vulnerability_topics.id'), nullable=False)
    
    # Lesson metadata
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), unique=True, index=True)
    descr = db.Column(db.Text)  # Brief description of this lesson's focus
    
    # Target audience
    target_difficulty = db.Column(db.String(20))  # beginner, intermediate, advanced
    estimated_duration_minutes = db.Column(db.Integer, default=15)
    learning_objectives = db.Column(db.Text)  # JSON array of learning goals
    
    # Lesson flow
    introduction_content = db.Column(db.Text)  # Hook and context-setting
    conclusion_content = db.Column(db.Text)  # Summary + key takeaway
    
    # Interactive elements
    has_interactive_demo = db.Column(db.Boolean, default=False)
    has_socratic_questions = db.Column(db.Boolean, default=True)
    has_reflection_checkpoint = db.Column(db.Boolean, default=True)
    
    # Safe scenario reference
    safe_scenario_id = db.Column(db.Integer, db.ForeignKey('safe_scenarios.id'))
    
    # Content management
    order_in_topic = db.Column(db.Integer, default=1)
    is_published = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    steps = db.relationship('LessonStep', backref='lesson', lazy='dynamic', cascade='all, delete-orphan')
    socratic_questions = db.relationship('SocraticQuestion', backref='lesson', lazy='dynamic', cascade='all, delete-orphan')
    comparison_notes = db.relationship('ComparisonNote', backref='lesson', foreign_keys='ComparisonNote.lesson_id', cascade='all, delete-orphan')
    learning_progress = db.relationship('StudentLearningProgress', backref='lesson', lazy='dynamic')
    student_reflections = db.relationship('StudentReflection', backref='lesson', lazy='dynamic')

    def __repr__(self):
        return f"<GuidedLesson {self.title}>"


class LessonStep(db.Model):
    """
    Atomic reasoning step in a lesson.
    
    A step is NOT "click to reveal" - it's a pedagogical moment:
    - Observation (what do you notice?)
    - Hypothesis (what do you think will happen?)
    - Action (try this)
    - Result (here's what happened)
    - Reasoning (why did it happen?)
    """
    __tablename__ = "lesson_steps"

    id = db.Column(db.Integer, primary_key=True)
    
    lesson_id = db.Column(db.Integer, db.ForeignKey('guided_lessons.id'), nullable=False)
    step_number = db.Column(db.Integer, nullable=False)
    
    # Step structure (pedagogical design)
    step_type = db.Column(db.String(50), nullable=False)  # 'observe', 'predict', 'execute', 'analyze', 'synthesize'
    
    # What the student encounters
    observation = db.Column(db.Text)  # "Look at this code/output"
    
    # Guided reasoning
    question_for_student = db.Column(db.Text)  # "What do you think will happen if...?"
    hint_if_stuck = db.Column(db.Text)  # Light hint to keep thinking
    hint_if_very_stuck = db.Column(db.Text)  # Stronger hint
    
    # The important content
    explanation = db.Column(db.Text)  # The key insight for this step
    expected_observation = db.Column(db.Text)  # What should the student see?
    
    # Why this step matters
    learning_objective = db.Column(db.Text)  # What concept does this teach?
    connection_to_concept = db.Column(db.Text)  # "This shows us that..."
    
    # Real-world comparison (optional)
    real_world_difference = db.Column(db.Text)  # "In production, this might..."
    real_world_why = db.Column(db.Text)  # Why is it different?
    
    # Step sequencing
    is_optional = db.Column(db.Boolean, default=False)
    branch_on_answer = db.Column(db.String(50))  # Can this branch to different paths?
    
    order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<LessonStep {self.lesson_id}:#{self.step_number}>"


class SocraticQuestion(db.Model):
    """
    Socratic questioning system: ask BEFORE revealing answer.
    Forces active thinking instead of passive reading.
    
    Flow:
    1. Student sees question
    2. Student predicts/answers
    3. System reveals answer + explanation
    4. System shows WHY their answer was right/wrong
    """
    __tablename__ = "socratic_questions"

    id = db.Column(db.Integer, primary_key=True)
    
    lesson_id = db.Column(db.Integer, db.ForeignKey('guided_lessons.id'), nullable=False)
    step_id = db.Column(db.Integer, db.ForeignKey('lesson_steps.id'))  # Can be standalone or tied to step
    
    # The question
    question_text = db.Column(db.Text, nullable=False)  # "What will this query do?"
    question_type = db.Column(db.String(50))  # 'prediction', 'analysis', 'design', 'defense'
    
    # Expected answer
    correct_answer = db.Column(db.Text, nullable=False)
    correct_answer_explanation = db.Column(db.Text)  # Why is this correct?
    
    # Common wrong answers (for learning!)
    common_wrong_answer_1 = db.Column(db.Text)
    common_wrong_answer_1_explanation = db.Column(db.Text)  # "This is wrong because..."
    
    common_wrong_answer_2 = db.Column(db.Text)
    common_wrong_answer_2_explanation = db.Column(db.Text)
    
    # Does it have multiple choice or free text?
    is_multiple_choice = db.Column(db.Boolean, default=False)
    choices_json = db.Column(db.Text)  # JSON array of options if multiple choice
    
    order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    student_answers = db.relationship('SocraticAnswer', backref='question', lazy='dynamic')

    def __repr__(self):
        return f"<SocraticQuestion {self.question_type}>"


class SocraticAnswer(db.Model):
    """
    Records what student answered to a Socratic question.
    Used for personalization and misconception tracking.
    """
    __tablename__ = "socratic_answers"

    id = db.Column(db.Integer, primary_key=True)
    
    question_id = db.Column(db.Integer, db.ForeignKey('socratic_questions.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # What they answered
    student_answer = db.Column(db.Text, nullable=False)
    is_correct = db.Column(db.Boolean, nullable=False)
    
    # Learning signal
    time_to_answer_seconds = db.Column(db.Integer)  # How long did they think?
    confidence_self_reported = db.Column(db.Integer)  # 1-5 scale if available
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    student = db.relationship('User', backref='socratic_answers')

    def __repr__(self):
        return f"<SocraticAnswer User:{self.student_id} Q:{self.question_id}>"


class SafeScenario(db.Model):
    """
    Interactive demo / safe sandbox for students to experiment.
    
    Purpose: Show the vulnerability in a controlled, safe environment
    where students can try things without breaking anything.
    
    Can be:
    - Simulated responses (fake backend)
    - Actual vulnerable app (in sandbox)
    - Code walkthrough (highlighted, explained)
    """
    __tablename__ = "safe_scenarios"

    id = db.Column(db.Integer, primary_key=True)
    
    topic_id = db.Column(db.Integer, db.ForeignKey('vulnerability_topics.id'))
    
    # Scenario metadata
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    
    # What type of demo?
    scenario_type = db.Column(db.String(50), nullable=False)  # 'simulated', 'code_walkthrough', 'live_sandbox', 'visualization'
    
    # The vulnerable code/app
    vulnerable_code = db.Column(db.Text)  # Code that shows the vulnerability
    vulnerable_code_language = db.Column(db.String(50))  # python, php, nodejs, etc.
    vulnerable_code_highlighted_lines = db.Column(db.Text)  # JSON: which lines are vulnerable?
    
    # Safe fixed version
    fixed_code = db.Column(db.Text)  # How to fix it
    
    # Interactive elements
    can_modify_input = db.Column(db.Boolean, default=True)  # Can student change the input?
    default_input = db.Column(db.Text)  # Starting input
    
    # Simulation data (if simulated)
    sample_payloads = db.Column(db.Text)  # JSON: payloads to try
    sample_payload_results = db.Column(db.Text)  # JSON: what each payload produces
    
    # Live sandbox (if actual app)
    sandbox_url = db.Column(db.String(500))  # URL to sandbox environment
    sandbox_instructions = db.Column(db.Text)  # How to use it
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    lessons = db.relationship('GuidedLesson', backref='safe_scenario', foreign_keys='GuidedLesson.safe_scenario_id')

    def __repr__(self):
        return f"<SafeScenario {self.title}>"


class ComparisonNote(db.Model):
    """
    THE KEY FEATURE: Show differences between learning environment and real-world.
    
    This is where deep understanding comes from.
    Students need to learn that production apps have:
    - Authentication layers
    - Input sanitization/validation
    - WAF (Web Application Firewall)
    - Rate limiting
    - Logging
    - Encoding layers
    - Caching
    - Proxy layers
    - etc.
    
    These comparisons teach JUDGMENT, not just "here's the exploit"
    """
    __tablename__ = "comparison_notes"

    id = db.Column(db.Integer, primary_key=True)
    
    topic_id = db.Column(db.Integer, db.ForeignKey('vulnerability_topics.id'))
    lesson_id = db.Column(db.Integer, db.ForeignKey('guided_lessons.id'))
    
    # What's being compared
    comparison_type = db.Column(db.String(50), nullable=False)  # 'sanitization', 'authentication', 'rate_limiting', 'waf', 'encoding', 'architecture'
    
    # Simple scenario (what we show)
    simplified_scenario = db.Column(db.Text)  # "In our demo app, input goes to DB"
    simplified_code_example = db.Column(db.Text)  # Code showing simple version
    
    # Real-world scenario
    real_world_scenario = db.Column(db.Text)  # "In production, input might be..."
    real_world_code_example = db.Column(db.Text)  # Realistic code pattern
    real_world_why = db.Column(db.Text)  # Why do companies do this?
    
    # The learning moment
    what_changes = db.Column(db.Text)  # "This means the payload now..."
    implications_for_attacker = db.Column(db.Text)  # What does defender gain?
    implications_for_defender = db.Column(db.Text)  # What counter-measures work?
    
    # Visual aids
    diagram_url = db.Column(db.String(500))  # Side-by-side diagram
    
    order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<ComparisonNote {self.comparison_type}>"


class Misconception(db.Model):
    """
    Track common student mistakes and wrong assumptions.
    
    When a student makes the same wrong guess many students make,
    the platform responds: "Many students think X, but here's why that's not quite right..."
    
    This turns confusion into learning.
    """
    __tablename__ = "misconceptions"

    id = db.Column(db.Integer, primary_key=True)
    
    topic_id = db.Column(db.Integer, db.ForeignKey('vulnerability_topics.id'), nullable=False)
    
    # The wrong assumption
    misconception_statement = db.Column(db.Text, nullable=False)  # "Input validation blocks all SQL injection"
    why_students_think_this = db.Column(db.Text)  # Why is it a plausible mistake?
    
    # The correction
    correct_understanding = db.Column(db.Text)  # What's actually true?
    explanation = db.Column(db.Text)  # Why is the misconception wrong?
    counterexample = db.Column(db.Text)  # Show a case where they'd be wrong
    
    # When to show this
    appears_in_step = db.Column(db.Integer)  # Which lesson step often triggers this?
    severity = db.Column(db.String(20))  # critical (blocks learning), important, minor
    
    # Analytics
    encounter_count = db.Column(db.Integer, default=0)  # How many students hit this?
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    student_encounters = db.relationship('MisconceptionEncounter', backref='misconception', lazy='dynamic')

    def __repr__(self):
        return f"<Misconception {self.id}>"


class MisconceptionEncounter(db.Model):
    """
    Record when a student encounters/experiences a misconception.
    Helps personalize the learning experience over time.
    """
    __tablename__ = "misconception_encounters"

    id = db.Column(db.Integer, primary_key=True)
    
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    misconception_id = db.Column(db.Integer, db.ForeignKey('misconceptions.id'), nullable=False)
    
    # When and where
    encountered_at = db.Column(db.DateTime, default=datetime.utcnow)
    encounter_type = db.Column(db.String(50))  # 'wrong_answer', 'slow_progress', 'repeated_attempt'
    
    # Did they learn from it?
    resolved = db.Column(db.Boolean, default=False)
    resolved_at = db.Column(db.DateTime)
    
    # How many times?
    encounter_count = db.Column(db.Integer, default=1)

    def __repr__(self):
        return f"<MisconceptionEncounter S:{self.student_id} M:{self.misconception_id}>"


class StudentLearningProgress(db.Model):
    """
    Replaces old 'UserProgress' - tracks UNDERSTANDING, not just completion.
    
    Core metrics:
    - What steps did student complete?
    - How many hints did they need? (signals: understanding level)
    - Did they understand the concept or just guess?
    - Can they explain it back?
    """
    __tablename__ = "student_learning_progress"

    id = db.Column(db.Integer, primary_key=True)
    
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    lesson_id = db.Column(db.Integer, db.ForeignKey('guided_lessons.id'), nullable=False)
    
    # Progress tracking
    is_started = db.Column(db.Boolean, default=True)
    is_completed = db.Column(db.Boolean, default=False)
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    
    # Understanding signals
    steps_completed = db.Column(db.Integer, default=0)  # Of how many total?
    total_steps = db.Column(db.Integer)
    
    hints_used = db.Column(db.Integer, default=0)  # Track hint dependence
    hints_needed_json = db.Column(db.Text)  # JSON: which steps needed hints?
    
    # Socratic performance
    socratic_questions_attempted = db.Column(db.Integer, default=0)
    socratic_correct = db.Column(db.Integer, default=0)
    socratic_accuracy = db.Column(db.Float)  # percentage
    
    # Time invested
    time_spent_seconds = db.Column(db.Integer, default=0)
    last_activity_at = db.Column(db.DateTime)
    
    # Understanding level (our estimate)
    estimated_understanding = db.Column(db.String(20))  # naive, partial, competent, expert
    confidence_score = db.Column(db.Float)  # 0-100, our confidence in their understanding
    
    # Did they reflect?
    has_written_reflection = db.Column(db.Boolean, default=False)
    reflection_quality = db.Column(db.String(20))  # superficial, adequate, deep
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<StudentLearningProgress S:{self.student_id} L:{self.lesson_id}>"


class TopicMastery(db.Model):
    """
    How well does a student understand a TOPIC (not just a lesson)?
    
    Aggregates progress across all lessons for a topic.
    Used for personalized learning paths and the skill graph.
    """
    __tablename__ = "topic_mastery"

    id = db.Column(db.Integer, primary_key=True)
    
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    topic_id = db.Column(db.Integer, db.ForeignKey('vulnerability_topics.id'), nullable=False)
    
    # Mastery level
    mastery_level = db.Column(db.String(20))  # unfamiliar, familiar, competent, expert
    mastery_percentage = db.Column(db.Float)  # 0-100
    
    # Learning history
    first_encountered = db.Column(db.DateTime)
    last_studied = db.Column(db.DateTime)
    total_study_time_seconds = db.Column(db.Integer, default=0)
    
    # Readiness for revision (spaced repetition)
    next_revision_due = db.Column(db.DateTime)  # When should they revisit?
    revision_count = db.Column(db.Integer, default=0)
    
    # Weak areas
    identified_weaknesses_json = db.Column(db.Text)  # JSON: which aspects need work?
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<TopicMastery S:{self.student_id} T:{self.topic_id}>"


class StudentReflection(db.Model):
    """
    "Teach-back" checkpoint: students explain concept in their own words.
    
    This is powerful because:
    1. Forces them to synthesize knowledge
    2. Reveals gaps in understanding
    3. Teacher (or AI) can give feedback on their explanation
    """
    __tablename__ = "student_reflections"

    id = db.Column(db.Integer, primary_key=True)
    
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    lesson_id = db.Column(db.Integer, db.ForeignKey('guided_lessons.id'), nullable=False)
    
    # Reflection prompt
    reflection_prompt = db.Column(db.Text)  # "Explain in your own words..."
    
    # Student's response
    student_explanation = db.Column(db.Text, nullable=False)  # Free text
    
    # Evaluation
    explanation_quality = db.Column(db.String(20))  # superficial, adequate, deep, expert
    quality_reasoning = db.Column(db.Text)  # Why did we score it that way?
    
    # Feedback
    ai_feedback = db.Column(db.Text)  # LLM-generated feedback on their explanation
    instructor_feedback = db.Column(db.Text)  # Human feedback if present
    
    # Does it reveal misconceptions?
    misconceptions_revealed = db.Column(db.Text)  # JSON: what gaps did we spot?
    suggested_review_topics = db.Column(db.Text)  # JSON: topics they should revisit
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<StudentReflection S:{self.student_id}>"


class RevisionDue(db.Model):
    """
    Spaced repetition scheduling.
    
    Important topics should come back automatically at optimal intervals
    (using spacing effect from cognitive science).
    """
    __tablename__ = "revision_due"

    id = db.Column(db.Integer, primary_key=True)
    
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    topic_id = db.Column(db.Integer, db.ForeignKey('vulnerability_topics.id'), nullable=False)
    
    # Spaced repetition
    interval_days = db.Column(db.Integer)  # How many days until next review?
    next_review_at = db.Column(db.DateTime)  # When should they review?
    
    # Progression
    repetition_count = db.Column(db.Integer, default=0)  # How many times reviewed?
    ease_factor = db.Column(db.Float, default=2.5)  # Difficulty multiplier (SM-2 algorithm)
    
    # Why it's due
    reason = db.Column(db.String(100))  # 'weak_area', 'scheduled_review', 'one_time_mistake'
    
    is_completed = db.Column(db.Boolean, default=False)
    completed_at = db.Column(db.DateTime)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<RevisionDue S:{self.student_id} T:{self.topic_id}>"


class LessonVersion(db.Model):
    """
    Content versioning for lessons.
    Allows authoring, editing, and publishing workflows.
    """
    __tablename__ = "lesson_versions"

    id = db.Column(db.Integer, primary_key=True)
    
    topic_id = db.Column(db.Integer, db.ForeignKey('vulnerability_topics.id'), nullable=False)
    
    # Versioning
    version_number = db.Column(db.Integer, nullable=False)
    is_current = db.Column(db.Boolean, default=True)
    
    # Changes
    changelog = db.Column(db.Text)  # What changed in this version?
    
    # Status
    status = db.Column(db.String(50))  # 'draft', 'review', 'published'
    status_changed_at = db.Column(db.DateTime)
    
    # Who made it?
    created_by_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    reviewed_by_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    published_by_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    published_at = db.Column(db.DateTime)

    def __repr__(self):
        return f"<LessonVersion v{self.version_number}>"


# ============================================================================
# HELPER MODELS FOR PLATFORM FEATURES
# ============================================================================

class AdminContentRequest(db.Model):
    """
    Track requests for new topics or lesson improvements.
    Helps admins prioritize what to create/update.
    """
    __tablename__ = "admin_content_requests"

    id = db.Column(db.Integer, primary_key=True)
    
    requested_by_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    request_type = db.Column(db.String(50))  # 'new_topic', 'improve_lesson', 'add_comparison'
    topic_name = db.Column(db.String(200))
    description = db.Column(db.Text)
    
    votes = db.Column(db.Integer, default=1)
    status = db.Column(db.String(50), default='open')  # open, in_progress, completed
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<AdminContentRequest {self.request_type}>"


class StudentDashboardStats(db.Model):
    """
    Cached dashboard statistics for quick loading.
    Aggregates student progress and mastery across all topics.
    """
    __tablename__ = "student_dashboard_stats"

    id = db.Column(db.Integer, primary_key=True)
    
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    
    # Overall stats
    total_topics_encountered = db.Column(db.Integer, default=0)
    topics_with_competent_mastery = db.Column(db.Integer, default=0)
    topics_with_expert_mastery = db.Column(db.Integer, default=0)
    
    # Weak spots
    weak_topics_needing_work = db.Column(db.Text)  # JSON: top 3 weak areas
    
    # Streaks
    study_streak_days = db.Column(db.Integer, default=0)
    longest_study_streak = db.Column(db.Integer, default=0)
    last_studied = db.Column(db.DateTime)
    
    # Revision insights
    topics_due_for_revision = db.Column(db.Integer, default=0)
    days_since_last_revision = db.Column(db.Integer)
    
    # Performance metrics
    average_accuracy_percent = db.Column(db.Float)  # On socratic questions
    average_time_per_lesson_minutes = db.Column(db.Float)
    
    # Badges/achievements
    achievements = db.Column(db.Text)  # JSON: earned badges
    
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<StudentDashboardStats S:{self.student_id}>"
