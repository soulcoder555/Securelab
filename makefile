.PHONY: help install run test clean docker-build docker-run

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-15s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: ## Install dependencies
	pip install -r requirements.txt

run: ## Run the Flask development server
	flask --app wsgi:app run

run-prod: ## Run with gunicorn
	gunicorn --bind 0.0.0.0:8000 wsgi:app

test: ## Run tests
	pytest

test-cov: ## Run tests with coverage
	pytest --cov=app --cov-report=html

clean: ## Clean up cache files
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	rm -rf .coverage htmlcov/

docker-build: ## Build Docker image
	docker build -t securelab .

docker-run: ## Run with Docker Compose
	docker-compose up --build

init-db: ## Initialize the database
	flask --app wsgi:app shell -c "from app import db; db.create_all(); print('Database initialized')"

create-admin: ## Create an admin user
	flask --app wsgi:app shell -c "
from app import db
from app.models import User
admin = User(username='admin', email='admin@example.com', role='admin')
admin.set_password('admin123')
db.session.add(admin)
db.session.commit()
print('Admin user created: admin/admin123')
"

seed-data: ## Add some sample data
	flask --app wsgi:app shell -c "
from app import db
from app.models import User, Note
# Create sample user
user = User(username='demo', email='demo@example.com')
user.set_password('demo123')
db.session.add(user)
db.session.commit()

# Create sample notes
notes = [
    Note(title='Welcome', content='Welcome to SecureLab!', user_id=user.id),
    Note(title='Security Notes', content='This app demonstrates secure coding practices.', user_id=user.id),
]
for note in notes:
    db.session.add(note)
db.session.commit()
print('Sample data created')
"