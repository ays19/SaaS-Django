# SaaS Django Project

A modular Django web application designed to demonstrate user authentication, user profiles, subscription permission management, protected routes, template inheritance, sub-templates (snippets), vendor asset management, database interaction (tracking page visit statistics), and containerized deployment.

---

## Features

- **User Authentication**: Login, registration, and account management using Django's auth system and `django-allauth`.
- **User Profiles**:
  - Profile listing view (`/profiles/`) displaying active users.
  - User detail profile pages (`/profiles/<username>/`).
- **Subscription & Permission Tier Management**:
  - Custom permissions framework (`subscriptions.basic`, `subscriptions.basic_ai`, `subscriptions.pro`, `subscriptions.advanced`).
  - `Subscription` model mapped to Django Groups and Permissions for feature access control.
- **Access Control & Protected Routes**:
  - User-only pages (`@login_required`).
  - Staff-only pages (`@staff_member_required`).
  - Password-protected routes.
- **Page Visit Tracking**: Persists visit path and timestamp to a SQLite database using the `PageVisit` model.
- **Dynamic Metrics**: Calculates and displays:
  - Visits to the current path.
  - Total visits across the entire site.
  - The percentage of visits the current path represents relative to total visits.
- **Template Inheritance & UI Styling**:
  - Core base layout (`templates/base.html`) with customizable blocks for content and titles.
  - Integrated Flowbite CSS/JS components.
- **Re-usable Snippets**: Includes reusable HTML snippets (e.g., navigation bar, welcome user messages).
- **Custom Management Commands**: Built-in `commando` app for management tasks, including automated vendor static file downloads (`vendor_pull`).
- **Containerization & Deployment Ready**:
  - Includes multi-stage `Dockerfile` with Gunicorn production server and runtime initialization script (`paracord_runner.sh`).
  - Cloud deployment configuration via `railway.json` for seamless deployment on Railway.

---

## Tech Stack

- **Backend**: Python 3.12, Django 5.x / 6.x
- **Authentication**: Django Auth & `django-allauth`
- **UI & Frontend**: Flowbite (pulled via vendor command), HTML5, CSS3
- **Database**: SQLite (default / dev) / PostgreSQL (supported via `libpq-dev`)
- **Production Server**: Gunicorn
- **Environment & Dependency Manager**: Python `venv` & `requirements.txt`
- **Containerization & Hosting**: Docker, Railway platform

---

## Project Structure

```text
├── manage.py                  # Django CLI entrypoint
├── requirements.txt           # Python dependencies
├── Dockerfile                 # Multi-stage Docker container specification
├── railway.json               # Railway cloud deployment configuration
├── Saas_Django/               # Core project configuration
│   ├── settings.py            # Global project settings (database, apps, hostnames)
│   ├── urls.py                # Route controllers / URL routing mapping
│   └── views.py               # View controllers (home_view, protected views, etc.)
├── auth/                      # Authentication application (login, register views)
├── commando/                  # Custom Django management commands (e.g., vendor_pull)
├── helpers/                   # General utility functions and helper modules
├── profiles/                  # User profiles app (user list & profile views)
├── subscriptions/             # Subscription tiers & permission management app
├── templates/                 # Global templates directory
│   ├── base.html              # Base layout template
│   ├── home.html              # Homepage view template inheriting from base
│   ├── protected/             # Protected page templates
│   ├── profiles/              # User profile templates
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

### 2. Download Vendor Static Files
Fetch external vendor libraries (Flowbite CSS/JS):
```bash
python manage.py vendor_pull
```

### 3. Run Database Migrations
Set up your database structure:
```bash
python manage.py migrate
```

### 4. Run the Development Server
```bash
python manage.py runserver
```
The server will start at `http://127.0.0.1:8000/`.

---

## Docker Support

You can build and run the application locally using Docker:

```bash
# Build the Docker image
docker build -t saas-django .

# Run the container on port 8000
docker run -p 8000:8000 -e DJANGO_SECRET_KEY='your-secret-key' saas-django
```

---

## URL Routes

- `http://127.0.0.1:8000/` – Root homepage (tracks visit metrics).
- `http://127.0.0.1:8000/login/` – User login page.
- `http://127.0.0.1:8000/register/` – User registration page.
- `http://127.0.0.1:8000/about/` – About page.
- `http://127.0.0.1:8000/profiles/` – Active user profile directory.
- `http://127.0.0.1:8000/profiles/<username>/` – Individual user profile detail page.
- `http://127.0.0.1:8000/accounts/` – `django-allauth` account routes (e.g. login, signup, password reset).
- `http://127.0.0.1:8000/protected/` – Password-protected view.
- `http://127.0.0.1:8000/protected/user_only/` – Login-required user view.
- `http://127.0.0.1:8000/protected/staff_only/` – Staff-only view.
- `http://127.0.0.1:8000/admin/` – Django Administration panel.


