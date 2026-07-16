# SaaS Django Project

A lightweight, modular Django web application designed to demonstrate template inheritance, sub-templates (snippets), and basic database interaction by tracking and displaying page visit statistics.

---

## Features

- **Page Visit Tracking**: Persists visit path and timestamp to a SQLite database using the `PageVisit` model.
- **Dynamic Metrics**: Calculates and displays:
  - Visits to the current path.
  - Total visits across the entire site.
  - The percentage of visits the current path represents relative to total visits.
- **Template Inheritance**: Uses a core base layout (`templates/base.html`) with customizable blocks for content and titles.
- **Re-usable Snippets**: Includes reusable HTML snippets (e.g., checking user authentication status).
- **Deployment-Ready Config**: Includes `ALLOWED_HOSTS` configuration for hosting on platform-as-a-service providers like Railway.

---

## Tech Stack

- **Backend**: Python 3.12, Django 6.x
- **Database**: SQLite (default)
- **Dependency Manager**: Pipenv (`Pipfile`)

---

## Project Structure

```text
├── manage.py                  # Django CLI entrypoint
├── Pipfile                    # Pipenv dependencies
├── Saas_Django/               # Core project configuration
│   ├── settings.py            # Global project settings (database, apps, hostnames)
│   ├── urls.py                # Route controllers / URLs routing mapping
│   └── views.py               # View controllers (home_view, about_view, etc.)
├── templates/                 # Global templates directory
│   ├── base.html              # Base layout template
│   ├── home.html              # Homepage view template inheriting from base
│   └── snippets/              # Reusable sub-template components
│       └── welcome-user-msg.html
└── visits/                    # App tracking page visits
    ├── models.py              # PageVisit model definition
    └── migrations/            # Database schema migrations
```

---

## Getting Started

### 1. Clone the Repository & Install Dependencies
First, ensure you have Python 3.12 and [Pipenv](https://pipenv.pypa.io/en/latest/) installed.

```bash
# Install dependencies from Pipfile
pipenv install

# Activate the virtual environment
pipenv shell
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

- `http://127.0.0.1:8000/` – Root page (renders homepage and tracks index visit).
- `http://127.0.0.1:8000/about/` – About page (renders and tracks visit).
- `http://127.0.0.1:8000/hello-world/` – Alternate root mapping.
- `http://127.0.0.1:8000/admin/` – Django Administration panel.
