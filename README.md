# IUBAT Course Offering System

A Django-based web application for managing course offerings, student enrollments, and class schedules for educational institutions.

## 🚀 Features

- **Student Management**: Registration, authentication, and profile management
- **Course Management**: Course creation, scheduling, and department assignment
- **Enrollment System**: Course enrollment/unenrollment with validation
- **Schedule Management**: Weekly routine generation and time slot management
- **Admin Interface**: Comprehensive Django admin with custom configurations
- **Responsive Design**: AdminLTE-based responsive interface

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8+** (Recommended: Python 3.10 or higher)
- **pip** (Python package manager)
- **Git** (for version control)

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd iubat-course-offering
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv env

# Activate virtual environment
# On macOS/Linux:
source env/bin/activate

# On Windows:
env\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Configuration

Create a `.env` file in the project root (optional but recommended for production):

```bash
# .env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### 5. Database Setup

```bash
# Create database tables
python manage.py makemigrations
python manage.py migrate

# Create superuser account
python manage.py createsuperuser
```

### 6. Collect Static Files

```bash
python manage.py collectstatic
```

### 7. Create Sample Data (Optional)

```bash
# Generate sample departments, courses, and schedules
python manage.py create_sample_data
```

## ▶️ Running the Application

### Development Server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` to access the application.

### Admin Interface

Access the Django admin at `http://127.0.0.1:8000/admin/` using your superuser credentials.

## 👥 Default User Accounts

After running `create_sample_data`, you can use these test accounts:

**Admin Account:**
- Use the superuser account you created during installation

**Student Accounts:**
- Username: `20210001` | Password: `student123`
- Username: `20210002` | Password: `student123`
- Username: `20210003` | Password: `student123`

## 📁 Project Structure

```
iubat-course-offering/
├── core/                   # Main Django project settings
│   ├── settings.py        # Django configuration
│   ├── urls.py           # URL routing
│   └── wsgi.py           # WSGI application
├── offering/              # Main application
│   ├── models.py         # Database models
│   ├── views.py          # View functions
│   ├── admin.py          # Admin configurations
│   ├── urls.py           # App URL patterns
│   └── management/       # Custom Django commands
├── templates/            # HTML templates
│   ├── base.html        # Base template
│   ├── auth/            # Authentication templates
│   └── student/         # Student interface templates
├── static/              # Static files (CSS, JS, images)
├── requirements.txt     # Python dependencies
├── manage.py           # Django management script
└── db.sqlite3          # SQLite database
```

## 🎯 Key Models

- **Department**: Academic departments
- **Semester**: Academic semesters
- **Course**: Course definitions
- **CourseSchedule**: Class schedules and sections
- **Student**: Student profiles linked to Django User
- **Enrollment**: Student course enrollments

## 🌐 Deployment

### Production Setup

1. **Environment Variables**:
```bash
DEBUG=False
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
SECRET_KEY=your-production-secret-key
DATABASE_URL=your-database-url  # If using PostgreSQL
```

2. **Database Migration** (PostgreSQL recommended):
```bash
# Install PostgreSQL adapter
pip install psycopg2

# Update settings.py with PostgreSQL configuration
# Run migrations
python manage.py migrate
```

3. **Static Files**:
```bash
python manage.py collectstatic --noinput
```

4. **Web Server Configuration** (Example with Nginx + Gunicorn):

Install Gunicorn:
```bash
pip install gunicorn
```

Run with Gunicorn:
```bash
gunicorn core.wsgi:application --bind 0.0.0.0:8000
```

### Docker Deployment (Optional)

Create `Dockerfile`:
```dockerfile
FROM python:3.10
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000"]
```

Create `docker-compose.yml`:
```yaml
version: '3.8'
services:
  web:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - .:/app
    environment:
      - DEBUG=False
```

## 🔧 Configuration

### Settings Configuration

Key settings in `core/settings.py`:

- `INSTALLED_APPS`: Includes Django admin, auth, and custom apps
- `MIDDLEWARE`: Security and session middleware
- `TEMPLATES`: Template engine configuration
- `DATABASES`: SQLite default, easily configurable for PostgreSQL
- `STATIC_FILES`: Static file handling configuration

### Admin Interface

The application uses **Django Jazzmin** for an enhanced admin interface. Configuration can be modified in `settings.py`.

## 🚨 Troubleshooting

### Common Issues

1. **Module Not Found Error**:
   ```bash
   # Ensure virtual environment is activated
   source env/bin/activate
   pip install -r requirements.txt
   ```

2. **Database Issues**:
   ```bash
   # Reset database
   rm db.sqlite3
   python manage.py makemigrations
   python manage.py migrate
   ```

3. **Static Files Not Loading**:
   ```bash
   python manage.py collectstatic
   ```

4. **Permission Denied**:
   ```bash
   # On macOS/Linux, ensure proper permissions
   chmod +x manage.py
   ```

### Development Tips

- Use `python manage.py shell` for interactive Django shell
- Enable Django debug toolbar for development
- Use `python manage.py dbshell` for direct database access
- Monitor logs with `python manage.py runserver --verbosity=2`

## 📝 API Endpoints

### Student Interface
- `/` - Home (redirects to dashboard)
- `/login/` - Student login
- `/dashboard/` - Student dashboard
- `/enrollment/` - Course enrollment page
- `/routine/` - Student weekly schedule

### Admin Interface
- `/admin/` - Django admin interface

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

For support and questions:
- Create an issue in the repository
- Contact the development team
- Check the Django documentation: https://docs.djangoproject.com/

## 🔄 Version History

- **v1.0.0** - Initial release with core functionality
- Student authentication and enrollment system
- Admin interface for data management
- Responsive design with AdminLTE

---

**Note**: This system is designed for educational institutions and can be customized according to specific requirements.