# SaaS Django Project

A modular Django web application designed to demonstrate user authentication, protected routes, template inheritance, sub-templates (snippets), and database interaction by tracking and displaying page visit statistics.

---

## Features

- **User Authentication**: Login, registration, and account management using Django's auth system and `django-allauth`.
- **Access Control & Protected Routes**:
  - User-only pages (`@login_required`).
  - Staff-only pages (`@staff_member_required`).
  - Password-protected routes.
- **Page Visit Tracking**: Persists visit path and timestamp to a SQLite database using the `PageVisit` model.
- **Dynamic Metrics**: Calculates and displays:
  - Visits to the current path.
  - Total visits across the entire site.
  - The percentage of visits the current path represents relative to total visits.
- **Template Inheritance**: Uses a core base layout (`templates/base.html`) with customizable blocks for content and titles.
- **Re-usable Snippets**: Includes reusable HTML snippets (e.g., navigation bar, welcome user messages).
- **Custom Management Commands**: Built-in `commando` app for custom management utility tasks.
- **Deployment-Ready Config**: Includes static file configuration and environment setup for production hosting.

---

## Tech Stack

- **Backend**: Python 3.12, Django 5.x / 6.x
- **Authentication**: Django Auth & `django-allauth`
- **Database**: SQLite (default)
- **Environment & Dependency Manager**: Python `venv` & `requirements.txt`

---

## Project Structure

```text
├── manage.py                  # Django CLI entrypoint
├── requirements.txt           # Python dependencies
├── Saas_Django/               # Core project configuration
│   ├── settings.py            # Global project settings (database, apps, hostnames)
│   ├── urls.py                # Route controllers / URL routing mapping
│   └── views.py               # View controllers (home_view, protected views, etc.)
├── auth/                      # Authentication application (login, register views)
├── commando/                  # Custom Django management commands app
├── helpers/                   # General utility functions and helper modules
├── templates/                 # Global templates directory
│   ├── base.html              # Base layout template
│   ├── home.html              # Homepage view template inheriting from base
│   ├── protected/             # Protected page templates
│   └── snippets/              # Reusable sub-template components
└── visits/                    # App tracking page visits
    ├── models.py              # PageVisit model definition
    └── migrations/            # Database schema migrations
```

---

## Getting Started

### 1. Clone the Repository & Set Up Virtual Environment
Ensure you have Python 3.12 installed:

```bash
# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
# Linux/macOS:
source venv/bin/activate
# Windows (Command Prompt):
# venv\Scripts\activate.bat
# Windows (PowerShell):
# venv\Scripts\Activate.ps1

# Install dependencies from requirements.txt
pip install -r requirements.txt
```

### 2. Run Database Migrations
Set up your SQLite database structure:
```bash
python manage.py migrate
```

### 3. Run the Development Server
```bash
python manage.py runserver
```
The server will start at `http://127.0.0.1:8000/`.

---

## URL Routes

- `http://127.0.0.1:8000/` – Root homepage (tracks visit metrics).
- `http://127.0.0.1:8000/login/` – User login page.
- `http://127.0.0.1:8000/register/` – User registration page.
- `http://127.0.0.1:8000/about/` – About page.
- `http://127.0.0.1:8000/accounts/` – `django-allauth` account routes (e.g. login, signup, password reset).
- `http://127.0.0.1:8000/protected/` – Password-protected view.
- `http://127.0.0.1:8000/protected/user_only/` – Login-required user view.
- `http://127.0.0.1:8000/protected/staff_only/` – Staff-only view.
- `http://127.0.0.1:8000/admin/` – Django Administration panel.

