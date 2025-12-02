# Quick Start Guide - HostelEase

## ✅ Errors Fixed!

All CSS and JavaScript syntax errors have been fixed:
- ✅ Fixed CSS class selector with extra space (`.info-card-title`)
- ✅ Fixed malformed HTML in JavaScript template literals
- ✅ All code is now ready to run!

## 🚀 How to Run

### Option 1: Frontend Only (Quick Test)

1. **Open the frontend directly:**
   - Navigate to: `frontend/index.html`
   - Right-click and open with your browser
   - You'll see the beautiful UI, but API calls won't work without backend

### Option 2: Full Stack (Recommended)

#### Step 1: Install Python
If you don't have Python installed:
- Download from: https://www.python.org/downloads/
- **Important**: Check "Add Python to PATH" during installation

#### Step 2: Setup Backend
```bash
# Navigate to backend folder
cd backend

# Create virtual environment (use 'py' or 'python3' depending on your system)
py -m venv venv
# OR
python3 -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create database (you need PostgreSQL installed)
# Edit .env file with your PostgreSQL credentials first
python manage.py migrate

# Load sample data
python manage.py shell < seed_data.py

# Run server
python manage.py runserver
```

#### Step 3: Open Frontend
- Open `frontend/index.html` in browser
- Or use a local server: `python -m http.server 3000` (from frontend folder)

## 🔑 Test Credentials

After loading seed data:
- **Admin**: username=`admin`, password=`admin123`
- **Warden**: username=`warden`, password=`warden123`
- **Student**: username=`ali_khan`, password=`student123`

## 📝 Database Note

The app is configured for PostgreSQL. If you don't have it:
1. Install PostgreSQL from: https://www.postgresql.org/download/
2. Create a database named `hostel_db`
3. Update `backend/.env` with your credentials

## 🎯 What's Working

✅ Complete frontend with modern design
✅ All CSS animations and responsive layouts
✅ JavaScript modules for API, auth, animations
✅ Django backend with all models
✅ RESTful API endpoints
✅ Role-based authentication
✅ Seed data ready to load

## 💡 Alternative: SQLite (Easy Setup)

If PostgreSQL is too complex, you can use SQLite:

1. Edit `backend/hostel_management/settings.py`
2. Change DATABASES to:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

Then run migrations and everything will work!
