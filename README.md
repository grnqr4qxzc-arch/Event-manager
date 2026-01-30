# 🎬 Event & Movie Booking Backend (Django REST API)

Backend API for a movie and event booking platform built using Django REST Framework.  
Supports role-based access, movie & theatre management, show scheduling, and ticket booking.

## 🔗 Related Repository
Frontend Application: https://github.com/grnqr4qxzc-arch/event-frontend

---

## 🚀 Features

### 👤 Authentication & Roles
- JWT-based authentication (SimpleJWT)
- Role-based access control:
  - **Manager** – manage theatres, screens, movies, and shows
  - **User** – browse movies, view shows, and book tickets

---

### 🎥 Movies
**Managers can:**
- Add movies with images
- Manage shows for their own theatres

**Public users can:**
- View available movies
- Browse showtimes across theatres

---

### 🏢 Theatres & Screens
**Managers can:**
- Register theatres
- Create multiple screens
- Assign shows to specific screens

---

### 🕒 Shows
Each show is associated with:
- Movie
- Screen
- Scheduled time

---

## 🧱 Tech Stack
- Backend: Django, Django REST Framework
- Authentication: JWT (SimpleJWT)
- Database: SQLite (development), PostgreSQL (production-ready)
- Media Handling: Django media storage for image uploads

---

## 🧠 Engineering Highlights
- Enforced data ownership (managers can only manage their own data)
- Prevented silent foreign-key data loss via serializer-level validation
- Proper handling of media URLs using request context
- Clean separation of public and manager-only APIs

---

## ⚙️ Setup Instructions

### Clone repository
```bash
git clone https://github.com/grnqr4qxzc-arch/Event-manager

Create virtual environment
python -m venv venv
venv\Scripts\activate   # Windows

Install dependencies
pip install -r requirements.txt

Run migrations
python manage.py migrate

Create superuser
python manage.py createsuperuser

Start development server
python manage.py runserver

🛠 Admin Panel

Access at:
http://127.0.0.1:8000/admin

Used for:

Debugging

Validating database integrity

Verifying theatre, screen, and show ownership rules
cd event_backend

