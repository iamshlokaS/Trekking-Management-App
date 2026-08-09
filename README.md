# 🏔️ Trekking Management Application

A comprehensive web-based management system for trekking organizations to manage trek events, staff, users, and bookings.

## 📋 Features

### 🔐 Authentication & Authorization
- **Admin**: Pre-existing superuser with full control
- **Trek Staff**: Self-registration with admin approval required
- **Users (Trekkers)**: Self-registration for trek participation
- Role-based access control for secure operations

### 👨‍💼 Admin Features
- Create, edit, and delete trek events
- Approve and manage trek staff registrations
- Assign staff to specific treks
- View and manage all users and bookings
- Search and filter users, staff, and treks by name/ID
- Blacklist users or staff members

### 👤 Trek Staff Features
- Self-register and wait for admin approval
- View assigned treks and participant lists
- Update trek slots and status
- Manage trek details (open/close bookings)
- Track registered participants

### 🥾 User (Trekker) Features
- Self-register and login
- Browse available treks with filters
- Filter treks by difficulty and location
- Book treks with available slots
- View booking status and history
- Cancel bookings
- Edit user profile

### 📊 Key Functionalities
- Prevent overbooking beyond available slots
- Only assigned staff can manage treks
- Users can book only when trek status is "Open"
- Complete booking history maintenance
- Trek status management (Pending, Approved, Open, Closed, Completed)

## 🛠️ Technology Stack

- **Backend**: Flask (Python Web Framework)
- **Frontend**: Jinja2 Templates, HTML5, CSS3, Bootstrap 5
- **Database**: SQLite
- **Authentication**: Flask-Login
- **ORM**: SQLAlchemy

## 📦 Installation & Setup

### Step 1: Install Python
Make sure you have Python 3.8 or higher installed on your machine.

```bash
python --version
```

### Step 2: Clone or Download the Project
Extract the project files to your desired location.

### Step 3: Create Virtual Environment (Recommended)
Navigate to the project directory and create a virtual environment:

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 4: Install Dependencies
Install all required Python packages:

```bash
pip install -r requirements.txt
```

### Step 5: Run the Application
Start the Flask development server:

```bash
python app.py
```

You should see output like:
```
WARNING in app.run_simple (...)
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://localhost:5000
```

### Step 6: Access the Application
Open your web browser and navigate to:
```
http://localhost:5000
```

## 🔑 Default Credentials

### Admin Login
- **Username**: `admin`
- **Password**: `admin123`
- **User Type**: Admin

> ⚠️ **Security Note**: Change these credentials in production!

## 📁 Project Structure

```
trekking-management/
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── trekking_app.db            # SQLite database (auto-created)
└── templates/
    ├── base.html              # Base template with navigation
    ├── home.html              # Landing page
    ├── login.html             # Login form
    ├── register.html          # Registration form
    ├── error.html             # Error page
    ├── admin/
    │   ├── dashboard.html     # Admin dashboard
    │   ├── treks.html         # Manage treks
    │   ├── create_trek.html   # Create trek form
    │   ├── edit_trek.html     # Edit trek form
    │   ├── assign_staff.html  # Assign staff to trek
    │   ├── staff.html         # Manage staff
    │   ├── users.html         # Manage users
    │   └── bookings.html      # View bookings
    ├── staff/
    │   ├── dashboard.html     # Staff dashboard
    │   ├── update_slots.html  # Update trek details
    │   └── participants.html  # View trek participants
    └── user/
        ├── dashboard.html     # User dashboard
        ├── browse_treks.html  # Browse available treks
        ├── book_trek.html     # Book trek form
        ├── bookings.html      # View booking history
        └── profile.html       # Edit profile
```

## 🚀 Usage Guide

### For Administrators

1. **Login** with default admin credentials
2. **Create Treks**: Navigate to "Manage Treks" → "Create New Trek"
3. **Approve Staff**: Go to "Manage Staff" → Review pending registrations
4. **Assign Staff**: Click "Assign" on a trek to assign staff members
5. **Manage Users**: View and blacklist users if necessary
6. **View Bookings**: Monitor all trek bookings and status

### For Trek Staff

1. **Register** on the registration page (select "Trek Staff")
2. **Wait** for admin approval
3. **Login** once approved
4. **View Assigned Treks** on dashboard
5. **Update Trek Details**: Modify available slots and trek status
6. **View Participants**: See registered users for your treks

### For Users (Trekkers)

1. **Register** on the registration page (select "Trekker")
2. **Browse Treks**: Search and filter available treks
3. **Book Trek**: Click on a trek and confirm booking
4. **View Bookings**: Check booking status and history
5. **Cancel Booking**: Remove booking if needed
6. **Edit Profile**: Update contact information

## 🎯 Trek Status Workflow

```
Pending → Approved → Open → Closed → Completed
```

- **Pending**: Admin created the trek, not yet approved
- **Approved**: Admin approved; staff can prepare
- **Open**: Users can book slots
- **Closed**: No new bookings allowed
- **Completed**: Trek has finished

## 📊 Database Models

### Users Table
- ID, Username, Email, Password, Full Name, Phone, Address, Blacklist Status

### Staff Table
- ID, Username, Email, Password, Full Name, Phone, Experience, Approval Status, Blacklist Status

### Admin Table
- ID, Username, Email, Password, Full Name

### Trek Table
- ID, Name, Location, Difficulty, Duration, Description, Total Slots, Available Slots, Start Date, End Date, Status, Assigned Staff ID

### Booking Table
- ID, User ID, Trek ID, Booking Date, Status

## 🔒 Security Features

- **Password Storage**: Passwords are stored (⚠️ use hashing in production)
- **Session Management**: Flask-Login manages user sessions
- **Role-Based Access**: Different views/actions based on user role
- **Form Validation**: Both client and server-side validation

## ⚠️ Important Notes

1. **Development Mode**: This app runs in Flask debug mode. For production, use a proper WSGI server like Gunicorn.

2. **Database**: The SQLite database is created automatically on first run. No manual setup needed.

3. **Password Security**: In production, implement password hashing using `werkzeug.security`

4. **Email Notifications**: Currently, no email notifications. Consider adding Flask-Mail for real emails.

5. **Backup**: Regularly backup your `trekking_app.db` file.

## 🔧 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'flask'"
**Solution**: Install requirements: `pip install -r requirements.txt`

### Issue: "Address already in use"
**Solution**: Change the port in `app.py`:
```python
app.run(debug=True, host='localhost', port=5001)  # Use different port
```

### Issue: Database locked
**Solution**: Restart the Flask server and clear any locks on the database file.

### Issue: Login not working
**Solution**: Ensure user type (Admin/Staff/User) matches the account type.

## 📝 Creating a Test Admin Account

To create an additional admin account, modify the `init_db()` function in `app.py`:

```python
def init_db():
    with app.app_context():
        db.create_all()
        
        # Existing code...
        
        # Add another admin
        admin2 = Admin(
            username='admin2',
            email='admin2@trekking.com',
            password='admin123',
            full_name='Second Admin'
        )
        db.session.add(admin2)
        db.session.commit()
```

## 🎓 Learning Resources

This project demonstrates:
- Flask application structure
- SQLAlchemy ORM usage
- Jinja2 template rendering
- User authentication with Flask-Login
- Role-based access control
- Bootstrap responsive design
- Database relationships

## 📄 License

This project is provided for educational purposes.

## 👨‍💻 Support

For issues or questions:
1. Check the README and code comments
2. Review Flask documentation: https://flask.palletsprojects.com
3. Check SQLAlchemy docs: https://docs.sqlalchemy.org

## 🚀 Future Enhancements

- Email notifications for bookings
- Payment integration
- Trek rating and reviews
- Advanced search and filtering
- Dashboard analytics
- PDF report generation
- Mobile app version

---

**Happy Trekking! 🏔️**
