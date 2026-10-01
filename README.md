# Django Task Manager

A simple multi-user task manager built with Django. Users can sign up, log in, and manage their own tasks.

## Features
- User sign up, log in, and log out
- Create, edit, and delete tasks
- Task status (To Do, In Progress, Done) and optional due date
- Users only see and change their own tasks
- Django admin for management
- Automated tests

## Tech Stack
- Python 3
- Django
- SQLite (default database)

## Getting Started

```bash
git clone https://github.com/CodeNova55/django-task-manager.git
cd django-task-manager
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Then open http://127.0.0.1:8000

## Running Tests

```bash
python manage.py test
```

## Project Structure

```
config/   project settings and root URLs
tasks/    app: models, views, forms, templates, tests
```

## Git Workflow
- One feature branch per piece of work
- Feature branch -> PR into `develop`
- `develop` -> PR into `main`
- No direct pushes to `develop` or `main`

## Roadmap
- Task search and filtering
- Deployment