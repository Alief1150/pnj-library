# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**my_kisah** is a Django 6.0.2 web application. This is a fresh Django project with default configuration.

## Development Commands

### Running the Development Server
```bash
python manage.py runserver
```

### Database Operations
```bash
# Create and apply migrations
python manage.py makemigrations
python manage.py migrate

# Create a new app
python manage.py startapp <app_name>
```

### Django Admin
```bash
# Create superuser
python manage.py createsuperuser
```

### Testing
```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test <app_name>

# Run specific test
python manage.py test <app_name>.tests.<TestClass>
```

## Project Structure

```
my_kisah/
├── manage.py              # Django management script
├── db.sqlite3             # SQLite database (development)
└── my_kisah/              # Project configuration directory
    ├── settings.py        # Django settings
    ├── urls.py           # Root URL configuration
    ├── wsgi.py           # WSGI deployment interface
    └── asgi.py           # ASGI deployment interface
```

## Architecture Notes

- **Database**: SQLite3 for development (configured in `settings.py`)
- **Settings Module**: `my_kisah.settings`
- **Root URLconf**: `my_kisah.urls`
- **Installed Apps**: Default Django apps only (admin, auth, contenttypes, sessions, messages, staticfiles)
- **Secret Key**: Currently using development key (should be changed for production)
- **DEBUG**: Currently `True` (should be changed for production)

## Adding New Apps

When creating new apps:
1. Run: `python manage.py startapp <app_name>`
2. Add the app to `INSTALLED_APPS` in `my_kisah/settings.py`
3. Add app URLs to `urlpatterns` in `my_kisah/urls.py` using `include()`
