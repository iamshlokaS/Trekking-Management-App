"""
Test Data Population Script
===========================
This script populates the database with sample data for testing.
Run this AFTER the main application has been run once (to create the database).

Usage: python populate_test_data.py
"""

from app import app, db, User, Staff, Trek, Booking, Admin
from datetime import datetime, timedelta

def populate_test_data():
    """Populate database with sample test data"""
    
    with app.app_context():
        print("🔄 Populating test data...")
        
        # Clear existing data (except admin)
        Booking.query.delete()
        Trek.query.delete()
        Staff.query.delete()
        User.query.delete()
        
        # ============================================
        # CREATE TEST STAFF MEMBERS
        # ============================================
        print("👤 Creating staff members...")
        
        staff1 = Staff(
            username='rahul_guide',
            email='rahul@trekking.com',
            password='staff123',
            full_name='Rahul Kumar',
            phone='9876543210',
            experience_years=5,
            is_approved=True,
            is_blacklisted=False
        )
        
        staff2 = Staff(
            username='priya_guide',
            email='priya@trekking.com',
            password='staff123',
            full_name='Priya Singh',
            phone='9876543211',
            experience_years=3,
            is_approved=True,
            is_blacklisted=False
        )
        
        staff3 = Staff(
            username='rajesh_newstaff',
            email='rajesh@trekking.com',
            password='staff123',
            full_name='Rajesh Patel',
            phone='9876543212',
            experience_years=1,
            is_approved=False,  # Pending approval
            is_blacklisted=False
        )
        
        db.session.add_all([staff1, staff2, staff3])
        db.session.commit()
        print("✅ Staff created: 3 members (2 approved, 1 pending)")
        
        # ============================================
        # CREATE TEST TREKS
        # ============================================
        print("🏔️  Creating treks...")
        
        admin = Admin.query.first()
        
        trek1 = Trek(
            name='Everest Base Camp',
            location='Nepal',
            difficulty='Hard',
            duration_days=14,
            description='Challenge yourself with the most iconic trek in the world. Reach the base camp of Mount Everest.',
            total_slots=15,
            available_slots=8,
            start_date=datetime.now() + timedelta(days=30),
            end_date=datetime.now() + timedelta(days=44),
            status='Open',
            assigned_staff_id=staff1.id,
            created_by=admin.id
        )
        
        trek2 = Trek(
            name='Annapurna Circuit',
            location='Nepal',
            difficulty='Moderate',
            duration_days=21,
            description='A spectacular journey around Annapurna massif with diverse landscapes and culture.',
            total_slots=20,
            available_slots=12,
            start_date=datetime.now() + timedelta(days=45),
            end_date=datetime.now() + timedelta(days=66),
            status='Open',
            assigned_staff_id=staff2.id,
            created_by=admin.id
        )
        
        trek3 = Trek(
            name='Manali to Leh Highway Trek',
            location='Himachal Pradesh',
            difficulty='Moderate',
            duration_days=7,
            description='Experience the thrilling mountain roads and high altitude passes.',
            total_slots=25,
            available_slots=18,
            start_date=datetime.now() + timedelta(days=60),
            end_date=datetime.now() + timedelta(days=67),
            status='Open',
            assigned_staff_id=staff1.id,
            created_by=admin.id
        )
        
        trek4 = Trek(
            name='Kedarkantha Trek',
            location='Uttarakhand',
            difficulty='Easy',
            duration_days=4,
            description='Perfect beginner trek with stunning Himalayan views and snow-capped peaks.',
            total_slots=30,
            available_slots=20,
            start_date=datetime.now() + timedelta(days=20),
            end_date=datetime.now() + timedelta(days=24),
            status='Open',
            assigned_staff_id=staff2.id,
            created_by=admin.id
        )
        
        trek5 = Trek(
            name='Roopkund Trek',
            location='Uttarakhand',
            difficulty='Hard',
            duration_days=6,
            description='Trek to the mysterious glacial lake surrounded by mysterious skeletal remains.',
            total_slots=20,
            available_slots=15,
            start_date=datetime.now() + timedelta(days=50),
            end_date=datetime.now() + timedelta(days=56),
            status='Approved',  # Not yet open for booking
            assigned_staff_id=None,  # Not assigned yet
            created_by=admin.id
        )
        
        db.session.add_all([trek1, trek2, trek3, trek4, trek5])
        db.session.commit()
        print("✅ Treks created: 5 treks (4 open, 1 approved)")
        
        # ============================================
        # CREATE TEST USERS
        # ============================================
        print("👥 Creating users...")
        
        user1 = User(
            username='john_trekker',
            email='john@example.com',
            password='user123',
            full_name='John Doe',
            phone='8765432109',
            address='New Delhi'
        )
        
        user2 = User(
            username='sarah_adventurer',
            email='sarah@example.com',
            password='user123',
            full_name='Sarah Johnson',
            phone='8765432108',
            address='Mumbai'
        )
        
        user3 = User(
            username='mike_explorer',
            email='mike@example.com',
            password='user123',
            full_name='Mike Chen',
            phone='8765432107',
            address='Bangalore'
        )
        
        user4 = User(
            username='emma_hiker',
            email='emma@example.com',
            password='user123',
            full_name='Emma Wilson',
            phone='8765432106',
            address='Pune'
        )
        
        db.session.add_all([user1, user2, user3, user4])
        db.session.commit()
        print("✅ Users created: 4 users")
        
        # ============================================
        # CREATE TEST BOOKINGS
        # ============================================
        print("📋 Creating bookings...")
        
        booking1 = Booking(
            user_id=user1.id,
            trek_id=trek1.id,
            booking_date=datetime.now() - timedelta(days=5),
            status='Booked'
        )
        
        booking2 = Booking(
            user_id=user2.id,
            trek_id=trek1.id,
            booking_date=datetime.now() - timedelta(days=3),
            status='Booked'
        )
        
        booking3 = Booking(
            user_id=user3.id,
            trek_id=trek2.id,
            booking_date=datetime.now() - timedelta(days=2),
            status='Booked'
        )
        
        booking4 = Booking(
            user_id=user4.id,
            trek_id=trek4.id,
            booking_date=datetime.now() - timedelta(days=1),
            status='Booked'
        )
        
        booking5 = Booking(
            user_id=user1.id,
            trek_id=trek4.id,
            booking_date=datetime.now() - timedelta(days=10),
            status='Completed'
        )
        
        booking6 = Booking(
            user_id=user2.id,
            trek_id=trek3.id,
            booking_date=datetime.now(),
            status='Booked'
        )
        
        db.session.add_all([booking1, booking2, booking3, booking4, booking5, booking6])
        db.session.commit()
        print("✅ Bookings created: 6 bookings (5 active, 1 completed)")
        
        # ============================================
        # SUMMARY
        # ============================================
        print("\n" + "="*50)
        print("✅ TEST DATA POPULATED SUCCESSFULLY!")
        print("="*50)
        print("\n📊 Summary:")
        print(f"  • Admins: {Admin.query.count()}")
        print(f"  • Staff: {Staff.query.count()} (Approved: {Staff.query.filter_by(is_approved=True).count()}, Pending: {Staff.query.filter_by(is_approved=False).count()})")
        print(f"  • Treks: {Trek.query.count()}")
        print(f"  • Users: {User.query.count()}")
        print(f"  • Bookings: {Booking.query.count()}")
        
        print("\n🔐 Test Credentials:")
        print("\n  Admin:")
        print("    Username: admin")
        print("    Password: admin123")
        
        print("\n  Staff (Approved):")
        print("    Username: rahul_guide")
        print("    Password: staff123")
        
        print("\n  Users:")
        print("    Username: john_trekker")
        print("    Password: user123")
        
        print("\n💡 Tips:")
        print("  • Login with different accounts to test different roles")
        print("  • Admin can approve pending staff (Rajesh Patel)")
        print("  • Admin can assign staff to unassigned trek (Roopkund)")
        print("  • Users can browse, book, and cancel treks")
        print("  • Staff can update trek details and view participants")
        
        print("\n" + "="*50)
        print("Happy Testing! 🏔️")
        print("="*50 + "\n")

if __name__ == '__main__':
    populate_test_data()
