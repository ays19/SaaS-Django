# SaaS Django Project

A modular Django web application designed to demonstrate user authentication, user profiles, subscription permission management, Stripe billing integration, dynamic pricing pages, protected routes, template inheritance, sub-templates (snippets), vendor asset management, database interaction (tracking page visit statistics), and containerized deployment.

---

## Features

- **User Authentication & Accounts**: Login, registration, email confirmation, and account management powered by `django-allauth`.
- **Automated Customer Profile & Stripe Customer Sync**:
  - `Customer` model auto-created upon user signup (`allauth_user_signed_up` signal).
  - Stripe Customer creation triggered automatically via `django-allauth` signals upon email verification.
- **Stripe Billing Integration**:
  - `Subscription` model mapped to Stripe Products with automatic creation on `save()`.
  - `SubscriptionPrice` model mapped to Stripe Prices supporting monthly and yearly intervals.
  - Automatic single-featured price enforcement per interval.
- **Dynamic Pricing Page**:
  - `/pricing/` route showcasing featured monthly and yearly plans.
  - Custom subtitle and feature lists per plan with reusable pricing card sub-templates (`templates/subscriptions/snippets/pricing-card.html`).
- **User Profiles**:
  - Profile listing view (`/profiles/`) displaying active users.
  - User detail profile pages (`/profiles/<username>/`).
- **Subscription & Permission Tier Management**:
  - Custom permissions framework (`subscriptions.basic`, `subscriptions.basic_ai`, `subscriptions.pro`, `subscriptions.advanced`).
  - `Subscription` and `UserSubscription` models mapped to Django Groups and Permissions for feature access control.
  - Automatic user group synchronization via `post_save` Django signals when a user's subscription changes.
  - Django Admin inline management (`SubscriptionPrice` stacked inline within `SubscriptionAdmin`).
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
- **Re-usable Snippets**: Includes reusable HTML snippets (navigation bar, pricing cards, user messages).
- **Custom Management Commands**:
  - `vendor_pull`: Automated downloading of external vendor static files (Flowbite CSS/JS).
  - `sync_subs`: Synchronizes subscription permissions across active user groups.
- **Containerization & Deployment Ready**:
  - Includes multi-stage `Dockerfile` with Gunicorn production server and runtime initialization script (`paracord_runner.sh`).
  - Cloud deployment configuration via `railway.json` for seamless deployment on Railway.

---

## Tech Stack

- **Backend**: Python 3.12, Django 5.x / 6.x
- **Payments & Billing**: Stripe SDK (`stripe`)
- **Authentication**: Django Auth & `django-allauth`
- **UI & Frontend**: Flowbite (pulled via vendor command), Tailwind CSS classes, HTML5
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
├── auth/                      # Custom auth helper views
├── commando/                  # Custom Django management commands (e.g., vendor_pull)
├── customers/                 # Customer model & Stripe customer signal handling
├── helpers/                   # General utilities & Stripe API wrappers (billing.py)
├── profiles/                  # User profiles app (user list & profile views)
├── subscriptions/             # Subscription management app
│   ├── models.py              # Subscription, SubscriptionPrice & UserSubscription models
│   ├── admin.py               # Admin inline configurations for Subscriptions & Prices
│   ├── views.py               # Subscription price listing view
│   └── management/commands/   # Custom management commands (e.g., sync_subs)
├── templates/                 # Global templates directory
│   ├── base.html              # Base layout template
│   ├── home.html              # Homepage view template inheriting from base
│   ├── protected/             # Protected page templates
│   ├── profiles/              # User profile templates
│   ├── subscriptions/         # Pricing page and card snippet templates
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

### 2. Configure Environment Variables
Set your Stripe API keys in your `.env` file:
```env
STRIPE_SECRET_KEY=sk_test_...
```

### 3. Download Vendor Static Files & Sync Subscriptions
Fetch external vendor libraries (Flowbite CSS/JS) and synchronize subscription permissions:
```bash
python manage.py vendor_pull
python manage.py sync_subs
```

### 4. Run Database Migrations
Set up your database structure:
```bash
python manage.py migrate
```

### 5. Run the Development Server
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
- `http://127.0.0.1:8000/pricing/` – Public pricing page showcasing monthly & yearly plans.
- `http://127.0.0.1:8000/about/` – About page.
- `http://127.0.0.1:8000/profiles/` – Active user profile directory.
- `http://127.0.0.1:8000/profiles/<username>/` – Individual user profile detail page.
- `http://127.0.0.1:8000/accounts/` – `django-allauth` account routes (login, signup, password reset).
- `http://127.0.0.1:8000/protected/` – Password-protected view.
- `http://127.0.0.1:8000/protected/user_only/` – Login-required user view.
- `http://127.0.0.1:8000/protected/staff_only/` – Staff-only view.
- `http://127.0.0.1:8000/admin/` – Django Administration panel.




