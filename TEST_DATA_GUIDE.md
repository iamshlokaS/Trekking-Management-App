# 🧪 Test Data Guide - Trekking Management Application

Learn how to populate your database with sample test data for development and testing.

---

## 📋 Quick Start

### Step 1: Run Main Application
First, make sure the main application has run at least once to create the database:

```bash
python app.py
```

Wait for it to start, then press **CTRL+C** to stop.

### Step 2: Run Test Data Script
```bash
python populate_test_data.py
```

That's it! Your database is now populated with test data. ✅

### Step 3: Start Application Again
```bash
python app.py
```

Visit http://localhost:5000 and login with test credentials.

---

## 🔐 Test Credentials

### Admin Account (Pre-existing)
```
Username: admin
Password: admin123
```

### Test Staff Accounts (Auto-created)

**Rahul Kumar** (Approved - Can login)
```
Username: rahul_guide
Password: staff123
Email: rahul@trekking.com
Status: Approved ✅
Assigned Treks: 2
```

**Priya Singh** (Approved - Can login)
```
Username: priya_guide
Password: staff123
Email: priya@trekking.com
Status: Approved ✅
Assigned Treks: 2
```

**Rajesh Patel** (Pending - Cannot login yet)
```
Username: rajesh_newstaff
Password: staff123
Email: rajesh@trekking.com
Status: Pending ⏳
Note: Login as admin to approve this staff member
```

### Test User Accounts (Auto-created)

**John Doe**
```
Username: john_trekker
Password: user123
Email: john@example.com
Location: New Delhi
Bookings: 2 (1 active, 1 completed)
```

**Sarah Johnson**
```
Username: sarah_adventurer
Password: user123
Email: sarah@example.com
Location: Mumbai
Bookings: 2 (1 active, 1 with pending approval)
```

**Mike Chen**
```
Username: mike_explorer
Password: user123
Email: mike@example.com
Location: Bangalore
Bookings: 1 (active)
```

**Emma Wilson**
```
Username: emma_hiker
Password: user123
Email: emma@example.com
Location: Pune
Bookings: 1 (active)
```

---

## 🏔️ Test Treks

The script creates 5 treks with different statuses:

### 1. Everest Base Camp ⭐
```
Location: Nepal
Difficulty: Hard 🔴
Duration: 14 days
Status: Open (Accepting bookings) ✅
Available Slots: 8/15
Assigned Staff: Rahul Kumar
Bookings: John Doe, Sarah Johnson
```

**Description**: Challenge yourself with the most iconic trek in the world.

### 2. Annapurna Circuit 🏔️
```
Location: Nepal
Difficulty: Moderate 🟡
Duration: 21 days
Status: Open (Accepting bookings) ✅
Available Slots: 12/20
Assigned Staff: Priya Singh
Bookings: Mike Chen
```

**Description**: Spectacular journey around Annapurna massif.

### 3. Manali to Leh Highway Trek 🗻
```
Location: Himachal Pradesh
Difficulty: Moderate 🟡
Duration: 7 days
Status: Open (Accepting bookings) ✅
Available Slots: 18/25
Assigned Staff: Rahul Kumar
Bookings: Sarah Johnson
```

**Description**: Thrilling mountain roads and high altitude passes.

### 4. Kedarkantha Trek 💚
```
Location: Uttarakhand
Difficulty: Easy 🟢
Duration: 4 days
Status: Open (Accepting bookings) ✅
Available Slots: 20/30
Assigned Staff: Priya Singh
Bookings: Emma Wilson (Completed)
```

**Description**: Perfect beginner trek with stunning views.

### 5. Roopkund Trek 👻
```
Location: Uttarakhand
Difficulty: Hard 🔴
Duration: 6 days
Status: Approved (Not yet open) 🔒
Available Slots: 15/20
Assigned Staff: NOT ASSIGNED (Needs admin assignment)
Bookings: None
```

**Description**: Trek to mysterious glacial lake.
**Note**: This trek is approved but not open yet. Admin can assign staff and open it for bookings.

---

## 📋 Sample Bookings

| User | Trek | Status | Notes |
|------|------|--------|-------|
| John Doe | Everest Base Camp | Booked | Active booking |
| John Doe | Kedarkantha Trek | Completed | Trek completed |
| Sarah Johnson | Everest Base Camp | Booked | Active booking |
| Sarah Johnson | Manali to Leh | Booked | Active booking |
| Mike Chen | Annapurna Circuit | Booked | Active booking |
| Emma Wilson | Kedarkantha Trek | Booked | Active booking |

---

## 🎯 Test Scenarios

### Scenario 1: Admin Workflow

**Login as Admin**: admin / admin123

**Tasks**:
1. ✅ Create a new trek
2. ✅ Approve Rajesh Patel (pending staff)
3. ✅ Assign Rajesh to Roopkund Trek
4. ✅ Change Roopkund Trek status to "Open"
5. ✅ View all bookings
6. ✅ Blacklist a user (test functionality)

**Expected Outcomes**:
- Trek appears in system
- Staff can login
- Trek opens for bookings
- Booking counts update

---

### Scenario 2: Staff Workflow

**Login as Staff**: rahul_guide / staff123

**Available Treks**:
- Everest Base Camp (14 participants can register)
- Manali to Leh Highway Trek

**Tasks**:
1. ✅ View dashboard
2. ✅ Click on Everest Base Camp
3. ✅ Update total slots (increase/decrease)
4. ✅ Change trek status
5. ✅ View participant list
6. ✅ Print participant list

**Expected Outcomes**:
- Can see 2 assigned treks
- Can modify trek details
- Can see registered participants
- Cannot access other staff's treks

---

### Scenario 3: User Workflow

**Login as User**: john_trekker / user123

**Current Bookings**:
- Everest Base Camp (Booked)
- No other active bookings

**Tasks**:
1. ✅ View dashboard
2. ✅ Browse all available treks
3. ✅ Filter by difficulty (Easy)
4. ✅ Filter by location (Nepal)
5. ✅ Book a trek (if slots available)
6. ✅ Cancel a booking
7. ✅ View booking history
8. ✅ Edit profile

**Expected Outcomes**:
- Can see 4 open treks
- Can book available treks
- Can cancel bookings
- Booking history shows completed treks

---

## 🧑‍💻 Workflows to Test

### Admin Approving New Staff
```
1. Login as admin
2. Go to "Manage Staff"
3. Find "Rajesh Patel" (Pending)
4. Click "Approve"
5. Rajesh can now login
6. Assign Rajesh to a trek
```

### Staff Managing Trek
```
1. Login as rahul_guide
2. Click on assigned trek
3. Update available slots
4. Change status to "Closed" (test)
5. Change status back to "Open"
6. View registered participants
7. Print the list
```

### User Booking Trek
```
1. Login as john_trekker
2. Go to "Browse Treks"
3. Filter by difficulty or location
4. Click on trek (e.g., Annapurna)
5. Click "Book Now"
6. Agree to terms
7. Confirm booking
8. Check "My Bookings"
9. See newly booked trek
```

### Testing Overbooking Prevention
```
1. As different users, try to book same trek
2. After slots are full, "Book" button becomes disabled
3. Cannot exceed total slot count
4. Error message shows: "No slots available"
```

---

## 📊 Database Contents After Running Script

```
Users:        4 users
Staff:        3 staff members
Admin:        1 (default)
Treks:        5 treks
Bookings:     6 bookings
```

---

## 🧹 Clearing Test Data

### Option 1: Delete Database File
```bash
# Stop the application first
# Then delete the database
rm trekking_app.db
# or on Windows: del trekking_app.db

# Restart the application
python app.py
```

This recreates a fresh database with only the default admin.

### Option 2: Modify Script
To change test data, edit `populate_test_data.py` before running:
```python
# Change trek names, locations, etc.
# Modify staff details
# Adjust booking dates
```

---

## 💡 Tips for Testing

### For Admin Testing
- Create multiple treks with different statuses
- Test approval workflow with pending staff
- Try blacklisting users
- View comprehensive bookings report

### For Staff Testing
- Update trek slots multiple times
- Change trek status (Open → Closed → Open)
- Verify slot count accuracy
- Print participant list

### For User Testing
- Browse treks with various filters
- Try booking when slots are limited
- Test cancellation workflow
- View complete booking history

### Performance Testing
- Create large number of treks
- Test filtering with many records
- Check search functionality
- Monitor database response time

---

## 🔍 Verifying Test Data

### Login as Admin
1. Check "Total Treks" shows 5
2. Check "Total Users" shows 4
3. Check "Total Staff" shows 3
4. Check "Total Bookings" shows 6

### Login as Staff (rahul_guide)
1. Dashboard shows 2 assigned treks
2. Can view participants for each
3. Can update trek details

### Login as User (john_trekker)
1. Dashboard shows 1 active booking
2. "My Bookings" shows 2 total (1 completed)
3. Can browse 4 available treks

---

## ⚙️ Customizing Test Data

Edit `populate_test_data.py` to:
- Change trek names and locations
- Modify staff details
- Adjust difficulty levels
- Change start/end dates
- Modify slot counts
- Add more users/staff/treks
- Change booking statuses

Example:
```python
trek1 = Trek(
    name='YOUR_TREK_NAME',
    location='YOUR_LOCATION',
    difficulty='Hard',
    # ... other fields
)
```

---

## 🐛 Troubleshooting

### Error: "Database is locked"
```
Solution: Delete trekking_app.db and restart
```

### Script doesn't create data
```
Solution: Make sure app.py has been run once first
Solution: Check Python and dependencies installed
```

### Users can't login with test credentials
```
Solution: Verify exact username and password spelling
Solution: Run populate_test_data.py again
```

### Test treks don't appear in admin panel
```
Solution: Refresh browser (Ctrl+F5)
Solution: Logout and login again
```

---

## 📈 What You Can Test

✅ User registration and login
✅ Admin approval workflows
✅ Trek creation and modification
✅ Booking management
✅ Slot availability tracking
✅ Status workflows
✅ Role-based access control
✅ Search and filtering
✅ Blacklisting functionality
✅ Cancellation logic
✅ Complete booking history
✅ Responsive UI on different devices

---

## 🎉 You're Ready!

With test data populated, you can:
- Explore all features
- Test different user roles
- Verify workflows
- Check edge cases
- Develop new features
- Practice as a user

**Start testing now!** 🚀

---

**Last Updated**: 2026
**Test Data Version**: 1.0
