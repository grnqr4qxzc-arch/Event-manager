🎬 Event & Movie Booking Backend (Django REST API)

This repository contains the backend API for a movie & event booking platform built using Django REST Framework.
It supports role-based access for managers and users, movie & theatre management, show scheduling, and ticket booking.

👉 Frontend repository:
🔗 https://github.com/grnqr4qxzc-arch/<frontend-repo-name>

🚀 Features
👤 Authentication & Roles

JWT-based authentication

Role-based access:

Manager – manage theatres, screens, movies, shows

User – browse movies, view shows, book tickets

🎥 Movies

Managers can:

Add movies with images

Manage shows for their own theatres

Public users can:

View movies

View showtimes across theatres

🏢 Theatres & Screens

Managers can:

Register a theatre

Create multiple screens

Assign shows to specific screens

🕒 Shows

Each show is linked to:

Movie

Screen

🧱 Tech Stack

Backend: Django, Django REST Framework

Auth: JWT (SimpleJWT)

Database: SQLite (dev) / PostgreSQL (prod-ready)

Media: Django media storage for images

🧠 Key Engineering Highlights

Enforced data ownership (managers can only manage their own data)

Prevented silent foreign-key data loss via serializer validation

Proper handling of media URLs using request context

Clean separation of public vs manager APIs

⚙️ Setup Instructions

# Clone repo
git clone https://github.com/<your-username>/<backend-repo-name>
cd event_backend

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start server
python manage.py runserver

Admin Panel

Access at: http://127.0.0.1:8000/admin

Used for debugging and validating DB integrity

Theatre (via screen)

Accurate ownership & data-integrity checks enforced
