# HostelEase - Smart Hostel Management System

A complete, modern web application for managing university hostels with role-based access control for Admins, Wardens, and Students.

## 🌟 Features

### For Admins
- **Room Management**: Add, edit, and monitor room allocation and occupancy
- **Student Management**: Complete student profiles with room assignments
- **Fee Management**: Track payments, generate invoices, mark fees as paid/overdue
- **Comprehensive Dashboard**: Real-time statistics and analytics
- **Full System Control**: Access to all modules and features

### For Wardens
- **Attendance Tracking**: Daily attendance marking and reports
- **Visitor Management**: Log and track hostel visitors
- **Complaint Resolution**: View and resolve maintenance requests
- **Quick Actions**: Streamlined workflow for daily operations

### For Students
- **Personal Dashboard**: View room details, fees, and attendance
- **Mess Menu**: Check daily mess schedule
- **Complaint Submission**: Report maintenance issues directly
- **Fee Summary**: Track payment status and dues

## 🛠️ Technology Stack

### Backend
- **Framework**: Django 4.2.7
- **Database**: PostgreSQL
- **API**: Django REST Framework
- **Authentication**: Session-based with role-based permissions

### Frontend
- **HTML5**: Semantic structure
- **CSS3**: Modern design with CSS custom properties, dark mode
- **JavaScript**: Vanilla JS (no frameworks)
- **Design**: Responsive, mobile-first approach

## 📦 Installation

### Prerequisites
- Python 3.8+
- PostgreSQL 12+
- Git

### 1. Clone Repository
```bash
git clone <repository-url>
cd Hostel-Management-Web
```

### 2. Backend Setup

#### Create Virtual Environment
```bash
cd backend
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

#### Install Dependencies
```bash
pip install -r requirements.txt
```

#### Configure Database
1. Create PostgreSQL database:
```sql
CREATE DATABASE hostel_db;
CREATE USER postgres WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE hostel_db TO postgres;
```

2. Create `.env` file (copy from `.env.example`):
```bash
cp .env.example .env
```

3. Edit `.env` with your database credentials:
```env
DB_NAME=hostel_db
DB_USER=postgres
DB_PASSWORD=your_password_here
DB_HOST=localhost
DB_PORT=5432
SECRET_KEY=your-secret-key-here
DEBUG=True
```

#### Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

#### Create Superuser (Optional)
```bash
python manage.py createsuperuser
```

#### Load Seed Data
```bash
python manage.py shell < seed_data.py
```

This creates sample data including:
- 1 Admin user (username: `admin`, password: `admin123`)
- 1 Warden user (username: `warden`, password: `warden123`)
- 8 Student users (username: `ali_khan`, etc., password: `student123`)
- 20 Rooms
- Fee records, attendance, visitors, complaints, and mess menus

### 3. Start Backend Server
```bash
python manage.py runserver
```

Backend API will be available at: `http://127.0.0.1:8000`

### 4. Frontend Setup

Open the frontend in a browser:
- Simply open `frontend/index.html` in your browser, OR
- Use a local server (recommended):

```bash
cd frontend
# Using Python:
python -m http.server 3000
# OR using Node.js:
npx http-server -p 3000
```

Frontend will be available at: `http://localhost:3000`

## 🔑 Default Login Credentials

After running seed data:

**Admin:**
- Username: `admin`
- Password: `admin123`

**Warden:**
- Username: `warden`
- Password: `warden123`

**Student:**
- Username: `ali_khan` (or any student username)
- Password: `student123`

## 📱 Usage

### Home Page
- View features and system overview
- Access login for different roles

### Admin Dashboard
1. Login with admin credentials
2. View comprehensive statistics
3. Manage rooms, students, and fees
4. Use search and filters for data
5. Perform CRUD operations

### Warden Dashboard
1. Login with warden credentials
2. Mark daily attendance
3. Manage visitors
4. Resolve complaints

### Student Portal
1. Login with student credentials
2. View personal dashboard
3. Check fee status and attendance
4. Submit complaints
5. View mess menu

## 🎨 Features Highlight

### Modern UI/UX
- **Dark Mode**: Toggle between light and dark themes
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Animations**: Smooth scroll, fade-in effects, animated counters
- **Clean Design**: Professional color palette with gradient buttons

### Security
- CSRF protection
- Password hashing (PBKDF2)
- Role-based access control
- Session-based authentication

### Performance
- Optimized queries with select_related
- Pagination support
- Efficient database indexing

## 📁 Project Structure

```
Hostel-Management-Web/
├── backend/
│   ├── hostel_management/       # Django project settings
│   ├── accounts/                # User authentication app
│   ├── hostel/                  # Main hostel app (models, views)
│   ├── manage.py
│   ├── requirements.txt
│   └── seed_data.py            # Sample data generator
├── frontend/
│   ├── css/
│   │   ├── styles.css          # Main design system
│   │   └── pages.css           # Page-specific styles
│   ├── js/
│   │   ├── api.js              # API client
│   │   ├── auth.js             # Authentication
│   │   ├── animations.js       # UI animations
│   │   └── script.js           # Main application logic
│   └── index.html              # Single-page application
└── README.md
```

## 🔧 API Endpoints

### Authentication
- `POST /api/auth/register/` - Register new user
- `POST /api/auth/login/` - User login
- `POST /api/auth/logout/` - User logout
- `GET /api/auth/me/` - Get current user

### Rooms
- `GET /api/rooms/` - List all rooms
- `POST /api/rooms/` - Create room (Admin only)
- `GET /api/rooms/{id}/` - Room details
- `PUT /api/rooms/{id}/` - Update room (Admin only)
- `DELETE /api/rooms/{id}/` - Delete room (Admin only)

### Students
- `GET /api/students/` - List all students
- `POST /api/students/` - Add student (Admin only)
- `POST /api/students/{id}/assign_room/` - Assign room

### Fees
- `GET /api/fees/` - List fees
- `POST /api/fees/` - Create fee record
- `POST /api/fees/{id}/mark_paid/` - Mark as paid

### Attendance
- `GET /api/attendance/` - List attendance
- `POST /api/attendance/` - Mark attendance
- `GET /api/attendance/summary/` - Attendance summary

### Visitors, Complaints, Mess Menu
Similar RESTful endpoints for each module.

### Dashboard
- `GET /api/dashboard/stats/` - Get role-specific statistics

## 🧪 Testing

### Manual Testing
1. Start both backend and frontend servers
2. Login with different roles
3. Test CRUD operations
4. Verify role-based access

### Browser Testing
- Chrome/Edge (recommended)
- Firefox
- Safari

## 🚀 Deployment

### Backend (Django)
1. Set `DEBUG=False` in settings
2. Configure `ALLOWED_HOSTS`
3. Use production database
4. Collect static files: `python manage.py collectstatic`
5. Deploy to: Heroku, AWS, DigitalOcean, etc.

### Frontend
1. Deploy to: Netlify, Vercel, GitHub Pages
2. Update `API_BASE_URL` in `js/api.js` to production backend URL

## 📝 TODO / Future Enhancements

- [ ] Email notifications for fee reminders
- [ ] PDF report generation
- [ ] Student ID card generation
- [ ] Advanced analytics dashboard
- [ ] Mobile app (React Native)
- [ ] Real-time notifications (WebSockets)
- [ ] Biometric attendance integration

## 🤝 Contributing

Contributions are welcome! Please follow these steps:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📄 License

This project is open source and available under the MIT License.

## 👏 Acknowledgments

- Django and Django REST Framework teams
- Google Fonts (Poppins)
- PostgreSQL community

## 📧 Support

For issues or questions:
- Open an issue on GitHub
- Check documentation
- Review API endpoints

---

**Built with ❤️ for efficient hostel management**
