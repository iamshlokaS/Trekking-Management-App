# 🚀 Quick Start Guide - Trekking Management Application

Get up and running in 5 minutes!

## ⚡ Super Quick (Windows)

1. **Download and Extract** the project files
2. **Double-click** `run.bat`
3. **Open browser** to `http://localhost:5000`
4. **Login** with username: `admin`, password: `admin123`

Done! ✅

---

## ⚡ Super Quick (Mac/Linux)

1. **Download and Extract** the project files
2. **Open Terminal** in project directory
3. **Run**: `chmod +x run.sh && ./run.sh`
4. **Open browser** to `http://localhost:5000`
5. **Login** with username: `admin`, password: `admin123`

Done! ✅

---

## 📋 Step-by-Step Guide

### Step 1: Check Python Installation
```bash
python --version
# Should be 3.8 or higher
```

If Python is not installed, download from https://www.python.org

### Step 2: Navigate to Project Directory
```bash
cd path/to/trekking-management
```

### Step 3: Create Virtual Environment (One-time setup)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

Your terminal should now show `(venv)` at the beginning.

### Step 4: Install Dependencies
```bash
pip install -r requirements.txt
```

Wait for installation to complete (~1-2 minutes).

### Step 5: Run the Application
```bash
python app.py
```

You should see:
```
 * Running on http://localhost:5000
 * Debug mode: on
```

### Step 6: Open in Browser
Visit: **http://localhost:5000**

### Step 7: Login
Use these credentials:
- **Username**: `admin`
- **Password**: `admin123`

---

## 🎯 First Steps After Login

### As Admin:
1. ➕ **Create a Trek** (Manage Treks → Create New Trek)
2. 👤 **Approve Staff** (Manage Staff - if any staff registered)
3. 👥 **Assign Staff** to treks (click Assign on trek)

### As Staff Member:
1. 📝 **Register** (click Register on home page)
2. ⏳ **Wait** for admin approval
3. ✅ **Login** once approved
4. 📋 **Check** your assigned treks
5. ✏️ **Update** trek slots/status

### As User (Trekker):
1. 📝 **Register** (click Register on home page)
2. ✅ **Login** immediately
3. 🔍 **Browse Treks** (available ones)
4. 📍 **Book Trek** (if status is "Open")
5. 📋 **View Bookings** (check status and history)

---

## 🔍 Key Features Demo

### Admin Dashboard
- View statistics (total treks, users, staff, bookings)
- Quick action buttons
- Pending approvals alerts

### Create a Trek
1. Click "Create New Trek"
2. Fill in details:
   - Name: "Himalayan Adventure"
   - Location: "Nepal"
   - Difficulty: "Moderate"
   - Duration: "7" days
   - Slots: "20"
   - Start Date: Pick a future date
3. Click "Create Trek"

### Approve Staff
1. Go to "Manage Staff"
2. Click "Approve" on pending staff members

### Assign Staff to Trek
1. Go to "Manage Treks"
2. Click "Assign" button
3. Select staff member from dropdown
4. Click "Assign Staff"

### Browse & Book Trek (as User)
1. Click "Browse Treks"
2. Filter by difficulty or location
3. Click "Book Now" on any trek
4. Agree to terms
5. Click "Confirm Booking"
6. Check "My Bookings" to see your booking

---

## 🛑 Stopping the Server

Press **CTRL + C** in the terminal where Flask is running.

To deactivate virtual environment:
```bash
deactivate
```

---

## ⚙️ Configuration

### Change Port
Edit `app.py`, find this line:
```python
app.run(debug=True, host='localhost', port=5000)
```

Change `5000` to any other port (e.g., `5001`)

### Change Admin Password
Edit `app.py`, find the `init_db()` function:
```python
admin = Admin(
    username='admin',
    email='admin@trekking.com',
    password='YOUR_NEW_PASSWORD',  # Change here
    full_name='System Administrator'
)
```

---

## 🆘 Troubleshooting

### "Module not found" error
```bash
pip install -r requirements.txt
```

### "Port 5000 already in use"
Change the port in `app.py` (see Configuration section)

### Database errors
Delete `trekking_app.db` and restart the app. Database will be recreated.

### Can't access http://localhost:5000
- Check if Flask is running (look for "Running on..." message)
- Try `http://127.0.0.1:5000` instead
- Check firewall settings

### Forgot Admin Password
Delete `trekking_app.db`, restart app, and use default credentials again.

---

## 📚 File Structure

```
trekking-management/
├── app.py                 ← Main application (run this!)
├── requirements.txt       ← Dependencies
├── README.md             ← Full documentation
├── QUICKSTART.md         ← This file
├── run.bat               ← Quick start (Windows)
├── run.sh                ← Quick start (Mac/Linux)
├── trekking_app.db       ← Database (auto-created)
└── templates/            ← HTML files
    ├── base.html
    ├── home.html
    ├── login.html
    ├── register.html
    ├── error.html
    ├── admin/            ← Admin pages
    ├── staff/            ← Staff pages
    └── user/             ← User pages
```

---

## 🎓 What You're Learning

- **Flask**: Python web framework
- **Jinja2**: Template engine
- **SQLAlchemy**: Database ORM
- **Bootstrap**: Responsive design
- **Authentication**: User login/roles
- **SQL**: Database concepts

---

## ✅ Checklist

- [ ] Python installed (3.8+)
- [ ] Project extracted
- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] Application running
- [ ] Can access http://localhost:5000
- [ ] Can login with admin credentials
- [ ] Created a test trek
- [ ] Registered a test staff member
- [ ] Registered a test user

---

## 🎉 You're Ready!

The application is fully functional and ready to use. Start by:
1. Creating some treks
2. Approving test staff
3. Registering as a user and booking treks

**Enjoy! 🏔️**

---

## 📞 Need Help?

Refer to `README.md` for detailed documentation on:
- All features
- Database schema
- Security notes
- Future enhancements

---

**Last Updated**: 2026
**Version**: 1.0
