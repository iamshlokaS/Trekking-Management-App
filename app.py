# ============================================
# TREKKING MANAGEMENT APPLICATION - MAIN APP
# ============================================
# This is the main Flask application file
# All routes and configurations are defined here

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from functools import wraps
import os

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_change_this'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///trekking_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Redirect to login if not authenticated

# ============================================
# DATABASE MODELS
# ============================================

class User(db.Model):
    """User model for trekkers (participants)"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    full_name = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    address = db.Column(db.String(200))
    is_blacklisted = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    # Relationships
    bookings = db.relationship('Booking', backref='user', lazy=True, cascade='all, delete-orphan')
    
    # For Flask-Login
    @property
    def is_active(self):
        return not self.is_blacklisted
    
    @property
    def is_authenticated(self):
        return True
    
    @property
    def is_anonymous(self):
        return False
    
    def get_id(self):
        return str(self.id)


class Staff(db.Model):
    """Staff model for trek coordinators/guides"""
    __tablename__ = 'staff'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    full_name = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    experience_years = db.Column(db.Integer)
    is_approved = db.Column(db.Boolean, default=False)  # Admin approval needed
    is_blacklisted = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    # Relationships
    treks = db.relationship('Trek', backref='assigned_staff', lazy=True)
    
    # For Flask-Login
    @property
    def is_active(self):
        return self.is_approved and not self.is_blacklisted
    
    @property
    def is_authenticated(self):
        return True
    
    @property
    def is_anonymous(self):
        return False
    
    def get_id(self):
        return f"staff_{self.id}"


class Admin(db.Model):
    """Admin model - superuser"""
    __tablename__ = 'admin'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    full_name = db.Column(db.String(120))
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    # For Flask-Login
    @property
    def is_active(self):
        return True
    
    @property
    def is_authenticated(self):
        return True
    
    @property
    def is_anonymous(self):
        return False
    
    def get_id(self):
        return f"admin_{self.id}"


class Trek(db.Model):
    """Trek model - trekking events"""
    __tablename__ = 'treks'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    location = db.Column(db.String(120), nullable=False)
    difficulty = db.Column(db.String(20), nullable=False)  # Easy, Moderate, Hard
    duration_days = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text)
    total_slots = db.Column(db.Integer, nullable=False)
    available_slots = db.Column(db.Integer, nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='Pending')  # Pending, Approved, Open, Closed, Completed
    assigned_staff_id = db.Column(db.Integer, db.ForeignKey('staff.id'))
    created_by = db.Column(db.Integer, db.ForeignKey('admin.id'))  # Admin who created it
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    # Relationships
    bookings = db.relationship('Booking', backref='trek', lazy=True, cascade='all, delete-orphan')
    
    def get_available_slots(self):
        """Calculate available slots based on bookings"""
        booked = Booking.query.filter_by(trek_id=self.id, status='Booked').count()
        return self.total_slots - booked


class Booking(db.Model):
    """Booking model - user trek bookings"""
    __tablename__ = 'bookings'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    trek_id = db.Column(db.Integer, db.ForeignKey('treks.id'), nullable=False)
    booking_date = db.Column(db.DateTime, default=datetime.now)
    status = db.Column(db.String(20), default='Booked')  # Booked, Cancelled, Completed
    notes = db.Column(db.Text)


# ============================================
# USER LOADER FOR FLASK-LOGIN
# ============================================

@login_manager.user_loader
def load_user(user_id):
    """Load user from session - checks all user types"""
    try:
        if user_id.startswith('admin_'):
            admin_id = int(user_id.replace('admin_', ''))
            return Admin.query.get(admin_id)
        elif user_id.startswith('staff_'):
            staff_id = int(user_id.replace('staff_', ''))
            return Staff.query.get(staff_id)
        else:
            return User.query.get(int(user_id))
    except (ValueError, IndexError):
        return None


# ============================================
# HELPER FUNCTIONS
# ============================================

def init_db():
    """Initialize database with admin user"""
    with app.app_context():
        db.create_all()
        
        # Check if admin exists, if not create default admin
        admin = Admin.query.first()
        if not admin:
            admin = Admin(
                username='admin',
                email='admin@trekking.com',
                password='admin123',  # In production, hash this!
                full_name='System Administrator'
            )
            db.session.add(admin)
            db.session.commit()
            print("Default admin created: username=admin, password=admin123")


def role_required(role):
    """Decorator to check user role"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash('Please log in first', 'danger')
                return redirect(url_for('login'))
            
            # Check user type
            try:
                user_type = type(current_user).__name__
                print(f"Access check - Expected: {role}, Got: {user_type}")
                
                if user_type == role:
                    return f(*args, **kwargs)
                else:
                    print(f"Access denied: {user_type} trying to access {role} area")
                    flash('Unauthorized access', 'danger')
                    return redirect(url_for('home'))
            except Exception as e:
                print(f"Role check error: {e}")
                flash('An error occurred', 'danger')
                return redirect(url_for('home'))
        return decorated_function
    return decorator


# ============================================
# AUTHENTICATION ROUTES
# ============================================

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login route for all user types"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user_type = request.form.get('user_type')  # admin, staff, or user
        
        user = None
        
        # Check based on user type
        if user_type == 'admin':
            user = Admin.query.filter_by(username=username, password=password).first()
        elif user_type == 'staff':
            user = Staff.query.filter_by(username=username, password=password).first()
            if user and not user.is_approved:
                flash('Your account is pending admin approval', 'warning')
                return redirect(url_for('login'))
        elif user_type == 'user':
            user = User.query.filter_by(username=username, password=password).first()
            if user and user.is_blacklisted:
                flash('Your account has been blacklisted', 'danger')
                return redirect(url_for('login'))
        
        if user:
            try:
                login_user(user)
                flash(f'Welcome {username}!', 'success')
                print(f"User logged in: {user_type} - ID: {user.get_id()}")
                return redirect(url_for('dashboard'))
            except Exception as e:
                print(f"Login error: {e}")
                flash('Login error occurred', 'danger')
        else:
            flash('Invalid username or password', 'danger')
    
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Registration route for staff and users"""
    if request.method == 'POST':
        user_type = request.form.get('user_type')  # staff or user
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        full_name = request.form.get('full_name')
        phone = request.form.get('phone')
        
        # Check if user already exists
        if user_type == 'staff':
            existing = Staff.query.filter_by(username=username).first()
            if existing:
                flash('Staff username already exists', 'danger')
                return redirect(url_for('register'))
            
            staff = Staff(
                username=username,
                email=email,
                password=password,  # In production, hash this!
                full_name=full_name,
                phone=phone
            )
            db.session.add(staff)
            db.session.commit()
            flash('Staff registration successful! Please wait for admin approval.', 'success')
        
        elif user_type == 'user':
            existing = User.query.filter_by(username=username).first()
            if existing:
                flash('Username already exists', 'danger')
                return redirect(url_for('register'))
            
            user = User(
                username=username,
                email=email,
                password=password,  # In production, hash this!
                full_name=full_name,
                phone=phone
            )
            db.session.add(user)
            db.session.commit()
            flash('Registration successful! You can now log in.', 'success')
        
        return redirect(url_for('login'))
    
    return render_template('register.html')


@app.route('/logout')
@login_required
def logout():
    """Logout route"""
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))


# ============================================
# DASHBOARD ROUTES
# ============================================

@app.route('/dashboard')
@login_required
def dashboard():
    """Main dashboard - routes to appropriate dashboard based on user type"""
    try:
        user_type = type(current_user).__name__
        print(f"Dashboard route: User type = {user_type}, User ID = {current_user.get_id()}")
        
        if user_type == 'Admin':
            print("Redirecting to admin_dashboard")
            return redirect(url_for('admin_dashboard'))
        elif user_type == 'Staff':
            print("Redirecting to staff_dashboard")
            return redirect(url_for('staff_dashboard'))
        elif user_type == 'User':
            print("Redirecting to user_dashboard")
            return redirect(url_for('user_dashboard'))
        else:
            print(f"Unknown user type: {user_type}")
            flash('Unable to determine user type', 'danger')
            return redirect(url_for('home'))
    except Exception as e:
        print(f"Dashboard error: {e}")
        flash('An error occurred', 'danger')
        return redirect(url_for('home'))


@app.route('/admin/dashboard')
@login_required
@role_required('Admin')
def admin_dashboard():
    """Admin dashboard"""
    total_treks = Trek.query.count()
    total_users = User.query.count()
    total_staff = Staff.query.count()
    total_bookings = Booking.query.count()
    
    pending_staff = Staff.query.filter_by(is_approved=False, is_blacklisted=False).count()
    pending_treks = Trek.query.filter_by(status='Pending').count()
    
    return render_template('admin/dashboard.html',
                         total_treks=total_treks,
                         total_users=total_users,
                         total_staff=total_staff,
                         total_bookings=total_bookings,
                         pending_staff=pending_staff,
                         pending_treks=pending_treks)


@app.route('/staff/dashboard')
@login_required
@role_required('Staff')
def staff_dashboard():
    """Staff dashboard"""
    staff = current_user
    assigned_treks = Trek.query.filter_by(assigned_staff_id=staff.id).all()
    
    trek_stats = []
    for trek in assigned_treks:
        bookings = Booking.query.filter_by(trek_id=trek.id, status='Booked').count()
        trek_stats.append({
            'trek': trek,
            'booked_count': bookings,
            'available_slots': trek.get_available_slots()
        })
    
    return render_template('staff/dashboard.html', trek_stats=trek_stats)


@app.route('/user/dashboard')
@login_required
@role_required('User')
def user_dashboard():
    """User (trekker) dashboard"""
    user = current_user
    
    # Get available treks
    available_treks = Trek.query.filter_by(status='Open').all()
    
    # Get user's bookings
    bookings = Booking.query.filter_by(user_id=user.id).all()
    
    return render_template('user/dashboard.html',
                         available_treks=available_treks,
                         bookings=bookings)


# ============================================
# ADMIN ROUTES - TREK MANAGEMENT
# ============================================

@app.route('/admin/treks')
@login_required
@role_required('Admin')
def admin_treks():
    """View all treks"""
    search_query = request.args.get('search', '')
    
    if search_query:
        treks = Trek.query.filter(
            (Trek.name.contains(search_query)) |
            (Trek.location.contains(search_query))
        ).all()
    else:
        treks = Trek.query.all()
    
    return render_template('admin/treks.html', treks=treks, search_query=search_query)


@app.route('/admin/trek/create', methods=['GET', 'POST'])
@login_required
@role_required('Admin')
def create_trek():
    """Create new trek"""
    if request.method == 'POST':
        name = request.form.get('name')
        location = request.form.get('location')
        difficulty = request.form.get('difficulty')
        duration_days = int(request.form.get('duration_days'))
        description = request.form.get('description')
        total_slots = int(request.form.get('total_slots'))
        start_date_str = request.form.get('start_date')
        end_date_str = request.form.get('end_date')
        
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
            
            trek = Trek(
                name=name,
                location=location,
                difficulty=difficulty,
                duration_days=duration_days,
                description=description,
                total_slots=total_slots,
                available_slots=total_slots,
                start_date=start_date,
                end_date=end_date,
                status='Pending',
                created_by=current_user.id
            )
            db.session.add(trek)
            db.session.commit()
            flash(f'Trek "{name}" created successfully!', 'success')
            return redirect(url_for('admin_treks'))
        except Exception as e:
            flash(f'Error creating trek: {str(e)}', 'danger')
    
    return render_template('admin/create_trek.html')


@app.route('/admin/trek/<int:trek_id>/edit', methods=['GET', 'POST'])
@login_required
@role_required('Admin')
def edit_trek(trek_id):
    """Edit trek details"""
    trek = Trek.query.get_or_404(trek_id)
    
    if request.method == 'POST':
        trek.name = request.form.get('name')
        trek.location = request.form.get('location')
        trek.difficulty = request.form.get('difficulty')
        trek.duration_days = int(request.form.get('duration_days'))
        trek.description = request.form.get('description')
        trek.total_slots = int(request.form.get('total_slots'))
        trek.status = request.form.get('status')
        
        try:
            start_date_str = request.form.get('start_date')
            end_date_str = request.form.get('end_date')
            trek.start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
            trek.end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
        except:
            pass
        
        db.session.commit()
        flash('Trek updated successfully!', 'success')
        return redirect(url_for('admin_treks'))
    
    return render_template('admin/edit_trek.html', trek=trek)


@app.route('/admin/trek/<int:trek_id>/delete', methods=['POST'])
@login_required
@role_required('Admin')
def delete_trek(trek_id):
    """Delete trek"""
    trek = Trek.query.get_or_404(trek_id)
    name = trek.name
    
    # Delete associated bookings first
    Booking.query.filter_by(trek_id=trek_id).delete()
    db.session.delete(trek)
    db.session.commit()
    
    flash(f'Trek "{name}" deleted successfully!', 'success')
    return redirect(url_for('admin_treks'))


# ============================================
# ADMIN ROUTES - STAFF MANAGEMENT
# ============================================

@app.route('/admin/staff')
@login_required
@role_required('Admin')
def admin_staff():
    """View all staff"""
    search_query = request.args.get('search', '')
    
    if search_query:
        staff = Staff.query.filter(
            (Staff.full_name.contains(search_query)) |
            (Staff.username.contains(search_query))
        ).all()
    else:
        staff = Staff.query.all()
    
    return render_template('admin/staff.html', staff=staff, search_query=search_query)


@app.route('/admin/staff/<int:staff_id>/approve', methods=['POST'])
@login_required
@role_required('Admin')
def approve_staff(staff_id):
    """Approve staff registration"""
    staff = Staff.query.get_or_404(staff_id)
    staff.is_approved = True
    db.session.commit()
    flash(f'Staff "{staff.full_name}" approved!', 'success')
    return redirect(url_for('admin_staff'))


@app.route('/admin/staff/<int:staff_id>/blacklist', methods=['POST'])
@login_required
@role_required('Admin')
def blacklist_staff(staff_id):
    """Blacklist staff"""
    staff = Staff.query.get_or_404(staff_id)
    staff.is_blacklisted = not staff.is_blacklisted
    db.session.commit()
    
    status = "blacklisted" if staff.is_blacklisted else "removed from blacklist"
    flash(f'Staff "{staff.full_name}" {status}!', 'success')
    return redirect(url_for('admin_staff'))


@app.route('/admin/trek/<int:trek_id>/assign-staff', methods=['GET', 'POST'])
@login_required
@role_required('Admin')
def assign_staff(trek_id):
    """Assign staff to trek"""
    trek = Trek.query.get_or_404(trek_id)
    approved_staff = Staff.query.filter_by(is_approved=True, is_blacklisted=False).all()
    
    if request.method == 'POST':
        staff_id = request.form.get('staff_id')
        if staff_id:
            trek.assigned_staff_id = int(staff_id)
            db.session.commit()
            flash('Staff assigned to trek successfully!', 'success')
            return redirect(url_for('admin_treks'))
    
    return render_template('admin/assign_staff.html', trek=trek, staff_list=approved_staff)


# ============================================
# ADMIN ROUTES - USER MANAGEMENT
# ============================================

@app.route('/admin/users')
@login_required
@role_required('Admin')
def admin_users():
    """View all users"""
    search_query = request.args.get('search', '')
    
    if search_query:
        users = User.query.filter(
            (User.full_name.contains(search_query)) |
            (User.username.contains(search_query))
        ).all()
    else:
        users = User.query.all()
    
    return render_template('admin/users.html', users=users, search_query=search_query)


@app.route('/admin/user/<int:user_id>/blacklist', methods=['POST'])
@login_required
@role_required('Admin')
def blacklist_user(user_id):
    """Blacklist user"""
    user = User.query.get_or_404(user_id)
    user.is_blacklisted = not user.is_blacklisted
    db.session.commit()
    
    status = "blacklisted" if user.is_blacklisted else "removed from blacklist"
    flash(f'User "{user.full_name}" {status}!', 'success')
    return redirect(url_for('admin_users'))


@app.route('/admin/bookings')
@login_required
@role_required('Admin')
def admin_bookings():
    """View all bookings"""
    bookings = Booking.query.all()
    return render_template('admin/bookings.html', bookings=bookings)


# ============================================
# STAFF ROUTES
# ============================================

@app.route('/staff/trek/<int:trek_id>/update-slots', methods=['GET', 'POST'])
@login_required
@role_required('Staff')
def update_slots(trek_id):
    """Update trek slots and status"""
    trek = Trek.query.get_or_404(trek_id)
    
    # Verify staff is assigned to this trek
    if trek.assigned_staff_id != current_user.id:
        flash('You are not assigned to this trek', 'danger')
        return redirect(url_for('staff_dashboard'))
    
    if request.method == 'POST':
        trek.total_slots = int(request.form.get('total_slots'))
        trek.status = request.form.get('status')
        db.session.commit()
        flash('Trek updated successfully!', 'success')
        return redirect(url_for('staff_dashboard'))
    
    return render_template('staff/update_slots.html', trek=trek)


@app.route('/staff/trek/<int:trek_id>/participants')
@login_required
@role_required('Staff')
def view_participants(trek_id):
    """View participants for assigned trek"""
    trek = Trek.query.get_or_404(trek_id)
    
    if trek.assigned_staff_id != current_user.id:
        flash('You are not assigned to this trek', 'danger')
        return redirect(url_for('staff_dashboard'))
    
    bookings = Booking.query.filter_by(trek_id=trek_id, status='Booked').all()
    return render_template('staff/participants.html', trek=trek, bookings=bookings)


# ============================================
# USER ROUTES
# ============================================

@app.route('/user/treks')
@login_required
@role_required('User')
def browse_treks():
    """Browse available treks"""
    difficulty_filter = request.args.get('difficulty', '')
    location_filter = request.args.get('location', '')
    
    query = Trek.query.filter_by(status='Open')
    
    if difficulty_filter and difficulty_filter != 'all':
        query = query.filter_by(difficulty=difficulty_filter)
    
    if location_filter:
        query = query.filter(Trek.location.contains(location_filter))
    
    treks = query.all()
    all_locations = db.session.query(Trek.location).distinct().filter_by(status='Open').all()
    all_locations = [loc[0] for loc in all_locations]
    
    return render_template('user/browse_treks.html',
                         treks=treks,
                         locations=all_locations,
                         selected_difficulty=difficulty_filter,
                         selected_location=location_filter)


@app.route('/user/trek/<int:trek_id>/book', methods=['GET', 'POST'])
@login_required
@role_required('User')
def book_trek(trek_id):
    """Book a trek"""
    trek = Trek.query.get_or_404(trek_id)
    user = current_user
    
    if request.method == 'POST':
        # Check if trek is open
        if trek.status != 'Open':
            flash('This trek is not open for bookings', 'danger')
            return redirect(url_for('browse_treks'))
        
        # Check if slots available
        if trek.get_available_slots() <= 0:
            flash('No slots available for this trek', 'danger')
            return redirect(url_for('browse_treks'))
        
        # Check if already booked
        existing_booking = Booking.query.filter_by(user_id=user.id, trek_id=trek_id).first()
        if existing_booking:
            flash('You have already booked this trek', 'warning')
            return redirect(url_for('user_dashboard'))
        
        # Create booking
        booking = Booking(
            user_id=user.id,
            trek_id=trek_id,
            status='Booked'
        )
        db.session.add(booking)
        db.session.commit()
        
        flash(f'Successfully booked trek "{trek.name}"!', 'success')
        return redirect(url_for('user_dashboard'))
    
    return render_template('user/book_trek.html', trek=trek)


@app.route('/user/booking/<int:booking_id>/cancel', methods=['POST'])
@login_required
@role_required('User')
def cancel_booking(booking_id):
    """Cancel a booking"""
    booking = Booking.query.get_or_404(booking_id)
    
    if booking.user_id != current_user.id:
        flash('Unauthorized action', 'danger')
        return redirect(url_for('user_dashboard'))
    
    booking.status = 'Cancelled'
    db.session.commit()
    flash('Booking cancelled successfully', 'success')
    return redirect(url_for('user_dashboard'))


@app.route('/user/bookings')
@login_required
@role_required('User')
def user_bookings():
    """View user's booking history"""
    user = current_user
    bookings = Booking.query.filter_by(user_id=user.id).all()
    return render_template('user/bookings.html', bookings=bookings)


@app.route('/user/profile', methods=['GET', 'POST'])
@login_required
@role_required('User')
def user_profile():
    """Edit user profile"""
    user = current_user
    
    if request.method == 'POST':
        user.full_name = request.form.get('full_name')
        user.phone = request.form.get('phone')
        user.address = request.form.get('address')
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('user_dashboard'))
    
    return render_template('user/profile.html', user=user)


# ============================================
# HOME AND ERROR ROUTES
# ============================================

@app.route('/')
def home():
    """Home page"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('home.html')


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return render_template('error.html', error='Page not found'), 404


@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    return render_template('error.html', error='Server error'), 500


# ============================================
# APPLICATION ENTRY POINT
# ============================================

if __name__ == '__main__':
    # Initialize database on first run
    init_db()
    
    # Run Flask server for Railway
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
