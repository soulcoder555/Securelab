"""
prototype_of_secure_lab.py
Standalone prototype of SecureLab with backend data and minimal UI.
This file is intentionally separate from the existing SecureLab application.
"""

from flask import Flask, render_template_string, request, redirect, url_for, flash
from datetime import datetime

app = Flask(__name__)
app.secret_key = "prototype-secure-key"

challenges = [
    {
        "id": 1,
        "title": "SQL Injection - Login Bypass",
        "vulnerability_type": "SQL Injection",
        "difficulty": "Beginner",
        "points": 150,
        "description": "Bypass authentication by injecting SQL into the login form.",
        "exploitation_steps": [
            {"step": 1, "title": "Inspect the login form", "description": "Identify the username and password fields."},
            {"step": 2, "title": "Send malformed credentials", "description": "Try payloads such as \"' OR '1'='1\"."},
            {"step": 3, "title": "Confirm access", "description": "If login succeeds, capture the success response."}
        ],
        "required_tools": [
            {"name": "Browser", "command_template": "N/A", "example_usage": "Use the browser to submit the login form."},
            {"name": "Burp Suite", "command_template": "N/A", "example_usage": "Intercept the request and modify form fields."}
        ],
        "attack_payloads": [
            {"name": "Basic bypass", "payload": "' OR '1'='1", "explanation": "Always-true condition", "expected_result": "Login succeeds without valid credentials."}
        ],
        "security_defenses": [
            {"defense_name": "Parameterized queries", "how_it_works": "Separates data from SQL syntax.", "bypass_method": "Proper parameterization prevents this injection."}
        ],
        "bypass_techniques": [
            {"bypass_name": "Quote termination", "steps": "Close the quoted string and append OR expression.", "tools_needed": "None"}
        ],
        "cvss_score": 8.8,
        "cwe_id": "CWE-89",
        "attack_flow_description": "User -> Login Form -> SQL query injection -> Auth bypass",
        "lab_environment": "Beginner SQLi lab"
    },
    {
        "id": 2,
        "title": "Stored XSS - Comment System",
        "vulnerability_type": "Stored XSS",
        "difficulty": "Intermediate",
        "points": 220,
        "description": "Store a malicious script in user comments to execute in another user's browser.",
        "exploitation_steps": [
            {"step": 1, "title": "Locate the comment submission function", "description": "Find a page that stores user input."},
            {"step": 2, "title": "Submit a payload", "description": "Use a script tag such as \"<script>alert('xss')</script>\"."},
            {"step": 3, "title": "View the comment as another user", "description": "Confirm the payload executes when the page is loaded."}
        ],
        "required_tools": [
            {"name": "Browser", "command_template": "N/A", "example_usage": "Submit the malicious comment and reload the page."},
            {"name": "Developer tools", "command_template": "N/A", "example_usage": "Inspect rendered HTML and script execution."}
        ],
        "attack_payloads": [
            {"name": "Alert payload", "payload": "<script>alert('xss')</script>", "explanation": "Stored script executes in victim browser.", "expected_result": "Browser runs the alert when page loads."}
        ],
        "security_defenses": [
            {"defense_name": "Output encoding", "how_it_works": "Encodes HTML characters before rendering.", "bypass_method": "Ensures raw script text is not executed."}
        ],
        "bypass_techniques": [
            {"bypass_name": "DOM rendering", "steps": "Use DOM injection if filtering is inconsistent.", "tools_needed": "Browser devtools"}
        ],
        "cvss_score": 9.0,
        "cwe_id": "CWE-79",
        "attack_flow_description": "Attacker -> Comment form -> Stored payload -> Victim browser executes script",
        "lab_environment": "Intermediate XSS lab"
    }
]

vulnerabilities = [
    {
        "id": 1,
        "name": "SQL Injection",
        "severity": "Critical",
        "category": "Injection",
        "description": "Allows an attacker to alter SQL queries through unsanitized input.",
        "testing_methodology": "Review SQL queries, submit quote-terminated payloads, inspect responses.",
        "security_defenses": [
            {"measure": "Use parameterized queries", "implementation": "Prepared statements with bound variables.", "bypass_technique": "Not possible when implemented correctly."}
        ],
        "real_world_impact": "Can lead to authentication bypass, data theft, and full database compromise.",
        "mitigation_checklist": [
            {"item": "Validate input types", "priority": "High", "implementation": "Reject unexpected characters before database use."},
            {"item": "Use least privilege DB accounts", "priority": "Medium", "implementation": "Grant only required permissions."}
        ],
        "tool_recommendations": [
            {"tool_name": "sqlmap", "command": "sqlmap -u 'http://localhost/login' --data='username=admin&password=PASS'", "output_interpretation": "Look for injection points and database names."}
        ],
        "cwe_id": "CWE-89",
        "owasp_category": "A03:2021 - Injection"
    },
    {
        "id": 2,
        "name": "Stored Cross-Site Scripting (XSS)",
        "severity": "Critical",
        "category": "Client-side Attacks",
        "description": "Malicious script is saved on the server and served to other users.",
        "testing_methodology": "Submit sample script payloads and verify execution in page context.",
        "security_defenses": [
            {"measure": "Escape user input on output", "implementation": "HTML encode dynamic content.", "bypass_technique": "Prevents script execution if consistent."}
        ],
        "real_world_impact": "Can steal session cookies, perform actions as the victim, or deface content.",
        "mitigation_checklist": [
            {"item": "Use a secure templating engine", "priority": "High", "implementation": "Avoid raw HTML rendering from user input."}
        ],
        "tool_recommendations": [
            {"tool_name": "Burp Suite", "command": "Use repeater to inject and test payloads.", "output_interpretation": "Confirm the payload appears unencoded in the response."}
        ],
        "cwe_id": "CWE-79",
        "owasp_category": "A07:2021 - Identification and Authentication Failures"
    }
]

labs = [
    {
        "id": 1,
        "name": "SQL Injection Lab",
        "environment_type": "vulnerable_flask",
        "description": "A vulnerable login form that teaches SQLi fundamentals.",
        "intentional_vulnerabilities": [
            {"vuln_name": "SQL Injection", "location": "login endpoint", "how_to_exploit": "Submit ' OR '1'='1", "expected_result": "Login bypass."}
        ],
        "status": "stopped",
        "provisioned_at": None,
        "reset_script": "RESET SQLI LAB STATE"
    },
    {
        "id": 2,
        "name": "Stored XSS Lab",
        "environment_type": "vulnerable_flask",
        "description": "A comment board that stores scripts in comments.",
        "intentional_vulnerabilities": [
            {"vuln_name": "Stored XSS", "location": "comment submission", "how_to_exploit": "Submit <script>alert(1)</script>", "expected_result": "Payload executes when comment is viewed."}
        ],
        "status": "stopped",
        "provisioned_at": None,
        "reset_script": "RESET XSS LAB STATE"
    }
]

user_activity = []

base_template = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{{ title }} - SecureLab Prototype</title>
  <style>
    body { background: #090b17; color: #e6e8ff; font-family: Arial, sans-serif; margin: 0; }
    .page { max-width: 1080px; margin: 0 auto; padding: 24px; }
    .card { background: rgba(20, 24, 48, 0.96); border: 1px solid rgba(120, 130, 255, 0.25); border-radius: 18px; box-shadow: 0 0 45px rgba(88, 100, 255, 0.1); padding: 24px; margin-bottom: 20px; }
    .grid { display: grid; gap: 18px; grid-template-columns: repeat(auto-fit,minmax(280px,1fr)); }
    .badge { display: inline-block; padding: 6px 12px; border-radius: 999px; font-size: 0.8rem; letter-spacing: .4px; margin-bottom: 10px; }
    .badge-critical { background: #ff4f6d; }
    .badge-high { background: #ff9f43; }
    .badge-medium { background: #8f93ff; }
    .btn { display: inline-block; color: #fff; background: #5a6bff; text-decoration: none; padding: 10px 16px; border-radius: 10px; transition: transform .18s ease; }
    .btn:hover { transform: translateY(-1px); }
    input, textarea, select { width: 100%; padding: 10px; border-radius: 10px; border: 1px solid rgba(120, 130, 255, 0.3); background: rgba(10, 12, 32, 0.95); color: #fff; margin-top: 6px; }
    pre { background: rgba(12, 14, 40, 0.98); padding: 14px; border-radius: 12px; overflow: auto; }
    .alert { border-left: 4px solid #ff4f6d; padding-left: 14px; margin-bottom: 20px; color: #ffd9e1; }
    a { color: #99a9ff; }
  </style>
</head>
<body>
  <div class="page">
    <header class="card">
      <h1>{{ title }}</h1>
      <p>{{ subtitle }}</p>
      <p><a href="/">Home</a> · <a href="/challenges">Challenges</a> · <a href="/vulnerabilities">Vulnerabilities</a> · <a href="/labs">Labs</a></p>
    </header>
    {% with messages = get_flashed_messages() %}
      {% if messages %}
        <div class="card alert">{{ messages[0] }}</div>
      {% endif %}
    {% endwith %}
    {{ content }}
  </div>
</body>
</html>
"""

@app.route("/")
def home():
    total_challenges = len(challenges)
    total_vulns = len(vulnerabilities)
    completed = sum(1 for item in user_activity if item.get("success"))
    content = render_template_string(
        """
        <div class=\"grid\">
          <div class=\"card\">
            <h2>SecureLab Prototype</h2>
            <p>This standalone prototype demonstrates backend data, challenge flow, vulnerability documentation, and lab summaries without modifying the core application.</p>
          </div>
          <div class=\"card\">
            <h3>Stats</h3>
            <p><strong>{{ total_challenges }}</strong> challenges</p>
            <p><strong>{{ total_vulns }}</strong> vulnerabilities</p>
            <p><strong>{{ completed }}</strong> proofs submitted</p>
          </div>
          <div class=\"card\">
            <h3>Launch</h3>
            <p>Use the prototype routes below to explore the minimal SecureLab experience.</p>
            <a class=\"btn\" href=\"/challenges\">View Challenges</a>
          </div>
        </div>
        """,
        total_challenges=total_challenges,
        total_vulns=total_vulns,
        completed=completed
    )
    return render_template_string(base_template, title="Prototype Home", subtitle="A separate SecureLab prototype for testing and exploration.", content=content)

@app.route("/challenges")
def challenge_list():
    content = render_template_string(
        """
        <div class=\"grid\">{% for challenge in challenges %}
          <div class=\"card\">
            <span class=\"badge badge-{{ 'critical' if challenge.vulnerability_type == 'SQL Injection' else 'high' }}\">{{ challenge.vulnerability_type }}</span>
            <h3>{{ challenge.title }}</h3>
            <p>{{ challenge.description }}</p>
            <p><strong>{{ challenge.points }} points</strong> · {{ challenge.difficulty }}</p>
            <a class=\"btn\" href=\"/challenge/{{ challenge.id }}\">Open Challenge</a>
          </div>
        {% endfor %}</div>
        """,
        challenges=challenges
    )
    return render_template_string(base_template, title="Challenges", subtitle="Practice with prototype security challenges.", content=content)

@app.route("/challenge/<int:challenge_id>")
def challenge_detail(challenge_id):
    challenge = next((item for item in challenges if item["id"] == challenge_id), None)
    if not challenge:
        return "Challenge not found", 404
    content = render_template_string(
        """
        <div class=\"card\">
          <span class=\"badge badge-critical\">CVSS {{ challenge.cvss_score }}</span>
          <h2>{{ challenge.title }}</h2>
          <p>{{ challenge.description }}</p>
          <h3>Exploitation Steps</h3>
          <ol>{% for step in challenge.exploitation_steps %}<li><strong>{{ step.title }}</strong>: {{ step.description }}</li>{% endfor %}</ol>
          <h3>Payloads</h3>
          <pre>{{ challenge.attack_payloads[0].payload }}</pre>
          <h3>Security Defenses</h3>
          <ul>{% for defense in challenge.security_defenses %}<li><strong>{{ defense.defense_name }}</strong>: {{ defense.how_it_works }}</li>{% endfor %}</ul>
          <form method=\"post\" action=\"/submit/{{ challenge.id }}\">
            <label>Proof of Exploitation</label>
            <textarea name=\"proof\" rows=4 placeholder=\"Describe the success criteria or copy the result here.\"></textarea>
            <button class=\"btn\" type=\"submit\">Submit Proof</button>
          </form>
        </div>
        """,
        challenge=challenge
    )
    return render_template_string(base_template, title=challenge["title"], subtitle="Prototype challenge detail page.", content=content)

@app.route("/submit/<int:challenge_id>", methods=["POST"])
def submit_proof(challenge_id):
    proof = request.form.get("proof", "").strip()
    if not proof:
        flash("Please provide proof of exploitation before submitting.")
        return redirect(url_for("challenge_detail", challenge_id=challenge_id))
    user_activity.append({
        "challenge_id": challenge_id,
        "proof": proof,
        "success": True,
        "timestamp": datetime.utcnow().isoformat()
    })
    flash("Proof submitted successfully. Prototype backend recorded your result.")
    return redirect(url_for("challenge_detail", challenge_id=challenge_id))

@app.route("/vulnerabilities")
def vulnerability_list():
    content = render_template_string(
        """
        <div class=\"grid\">{% for vuln in vulnerabilities %}
          <div class=\"card\">
            <span class=\"badge badge-{{ 'critical' if vuln.severity == 'Critical' else 'high' }}\">{{ vuln.severity }}</span>
            <h3>{{ vuln.name }}</h3>
            <p>{{ vuln.description }}</p>
            <a class=\"btn\" href=\"/vulnerability/{{ vuln.id }}\">View Details</a>
          </div>
        {% endfor %}</div>
        """,
        vulnerabilities=vulnerabilities
    )
    return render_template_string(base_template, title="Vulnerabilities", subtitle="Browse prototype vulnerability documentation.", content=content)

@app.route("/vulnerability/<int:vuln_id>")
def vulnerability_detail(vuln_id):
    vuln = next((item for item in vulnerabilities if item["id"] == vuln_id), None)
    if not vuln:
        return "Vulnerability not found", 404
    content = render_template_string(
        """
        <div class=\"card\">
          <span class=\"badge badge-critical\">{{ vuln.category }}</span>
          <h2>{{ vuln.name }}</h2>
          <p>{{ vuln.description }}</p>
          <h3>Testing Methodology</h3>
          <p>{{ vuln.testing_methodology }}</p>
          <h3>Real World Impact</h3>
          <p>{{ vuln.real_world_impact }}</p>
          <h3>Mitigation Checklist</h3>
          <ul>{% for item in vuln.mitigation_checklist %}<li><strong>{{ item.priority }}</strong>: {{ item.item }} — {{ item.implementation }}</li>{% endfor %}</ul>
          <h3>Tool Recommendations</h3>
          <ul>{% for tool in vuln.tool_recommendations %}<li><strong>{{ tool.tool_name }}</strong>: {{ tool.command }}</li>{% endfor %}</ul>
        </div>
        """,
        vuln=vuln
    )
    return render_template_string(base_template, title=vuln["name"], subtitle="Prototype vulnerability detail.", content=content)

@app.route("/labs")
def lab_list():
    content = render_template_string(
        """
        <div class=\"grid\">{% for lab in labs %}
          <div class=\"card\">
            <h3>{{ lab.name }}</h3>
            <p>{{ lab.description }}</p>
            <p><strong>Environment:</strong> {{ lab.environment_type }}</p>
            <p><strong>Status:</strong> {{ lab.status }}</p>
            <a class=\"btn\" href=\"/lab/{{ lab.id }}\">Open Lab</a>
          </div>
        {% endfor %}</div>
        """,
        labs=labs
    )
    return render_template_string(base_template, title="Labs", subtitle="Prototype lab environment overview.", content=content)

@app.route("/lab/<int:lab_id>")
def lab_detail(lab_id):
    lab = next((item for item in labs if item["id"] == lab_id), None)
    if not lab:
        return "Lab not found", 404
    content = render_template_string(
        """
        <div class=\"card\">
          <h2>{{ lab.name }}</h2>
          <p>{{ lab.description }}</p>
          <p><strong>Environment Type:</strong> {{ lab.environment_type }}</p>
          <h3>Intentional Vulnerabilities</h3>
          <ul>{% for vuln in lab.intentional_vulnerabilities %}<li><strong>{{ vuln.vuln_name }}</strong>: {{ vuln.how_to_exploit }}</li>{% endfor %}</ul>
          <p><strong>Reset script:</strong> {{ lab.reset_script }}</p>
          <form method=\"post\" action=\"/lab/{{ lab.id }}/provision\">
            <button class=\"btn\" type=\"submit\">Provision Lab</button>
          </form>
        </div>
        """,
        lab=lab
    )
    return render_template_string(base_template, title=lab["name"], subtitle="Prototype lab detail.", content=content)

@app.route("/lab/<int:lab_id>/provision", methods=["POST"])
def provision_lab(lab_id):
    lab = next((item for item in labs if item["id"] == lab_id), None)
    if not lab:
        return "Lab not found", 404
    lab["status"] = "running"
    lab["provisioned_at"] = datetime.utcnow().isoformat()
    flash(f'Lab {lab["name"]} is now running in prototype mode.')
    return redirect(url_for("lab_detail", lab_id=lab_id))

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=6000, debug=True)
