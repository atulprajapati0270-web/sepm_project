# Smart Simhastha 2028 Management System

Academic Software Engineering project based on the supplied SRS.

## Technology
- Frontend: HTML, CSS, JavaScript, Jinja2
- Backend: Python Flask
- Database: MySQL
- ORM: Flask-SQLAlchemy
- Authentication: Flask-Login
- Deployment-ready: Gunicorn / Render configuration included

## Modules
1. User Registration and Login
2. Traffic and Route Management
3. Accommodation Management
4. Food Facility Management
5. Medical Emergency Management
6. Events and Programme Management
7. Shahi Snan Information
8. Security and Safety
9. Famous and Nearby Temples
10. Emergency Helpline
11. Complaint and Other Problems
12. Lost and Found
13. Notifications and Alerts
14. Admin Management

## Local Setup

### 1. Create MySQL database
```sql
CREATE DATABASE smart_simhastha CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 2. Create virtual environment
Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

Linux/macOS:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install packages
```bash
pip install -r requirements.txt
```

### 4. Configure environment
Copy `.env.example` to `.env` and set:
```env
SECRET_KEY=your-secret-key
DATABASE_URL=mysql+pymysql://root:YOUR_PASSWORD@localhost:3306/smart_simhastha
```

### 5. Initialize database
```bash
python seed.py
```

This creates the tables and demo data. Demo admin:
- Email: admin@simhastha.local
- Password: Admin@123

Change the demo password before real deployment.

### 6. Run
```bash
python app.py
```
Open: http://127.0.0.1:5000

## GitHub
```bash
git init
git add .
git commit -m "Initial Smart Simhastha 2028 project"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/Smart-Simhastha-2028.git
git push -u origin main
```

## Important
The SRS states that official event dates, Shahi Snan dates, routes, restrictions and emergency numbers must be verified before publication. This academic implementation uses database records that administrators can maintain. It does not replace official emergency services.

The SRS also lists live traffic/crowd data, map integration, push notifications, multilingual support and SOS integration as dependencies/future scope. These are intentionally not presented as guaranteed live services.
