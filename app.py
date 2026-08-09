# ============================================
# TREKKING MANAGEMENT APPLICATION - MAIN APP
# ============================================
# SQLite-Only Version (Compliant with Requirements)

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from functools import wraps
import os

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# ============================================
# DATABASE CONFIGURATION - SQLITE ONLY
# ============================================
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///trekking_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# ============================================
# DATABASE MODELS
# ============================================

class User(db.Model, UserMixin):
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
    
    def is_active(self):
        return not self.is_blacklisted
    
    def is_authenticated(self):
        return True
    
    def is_anonymous(self):
        return False
    
    def get_id(self):
        return str(self.id)


class Staff(db.Model, UserMixin):
    """Staff model for trek coordinators/guides"""
    __tablename__ = 'staff'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    full_name = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    experience_years = db.Column(db.Integer)
    is_approved = db.Column(db.Boolean, default=False)
    is_blacklisted = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    # Relationships
    treks = db.relationship('Trek', backref='assigned_staff', lazy=True)
    
    def is_active(self):
        return self.is_approved and not self.is_blacklisted
    
    def is_authenticated(self):
        return True
    
    def is_anonymous(self):
        return False
    
    def get_id(self):
        return f"staff_{self.id}"


class Admin(db.Model, UserMixin):
    """Admin model - superuser"""
    __tablename__ = 'admin'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    full_name = db.Column(db.String(120))
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    def is_active(self):
        return True
    
    def is_authenticated(self):
        return True
    
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
    difficulty = db.Column(db.String(20), nullable=False)
    duration_days = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text)
    total_slots = db.Column(db.Integer, nullable=False)
    available_slots = db.Column(db.Integer, nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='Pending')
    assigned_staff_id = db.Column(db.Integer, db.ForeignKey('staff.id'))
    created_by = db.Column(db.Integer, db.ForeignKey('admin.id'))
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    # Relationships
    bookings = db.relationship('Booking', backref='trek', lazy=True, cascade='all, delete-orphan')
    
    def get_available_slots(self):
        """Calculate available slots based on bookings"""
        booked = Booking.query.filter_by(trek_id=self.id, status='Booked').count()
        return self.total_slots - booked


class Booking(db.Model):
    """Booking model - trek reservations"""
    __tablename__ = 'bookings'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    trek_id = db.Column(db.Integer, db.ForeignKey('treks.id'), nullable=False)
    booking_date = db.Column(db.DateTime, default=datetime.now)
    status = db.Column(db.String(20), default='Booked')
    notes = db.Column(db.Text)


# ============================================
# USER LOADER FOR FLASK-LOGIN
# ============================================

@login_manager.user_loader
def load_user(user_id):
    """Load user from session"""
    try:
        if user_id.startswith('admin_'):
            admin_id = int(user_id.replace('admin_', ''))
            return Admin.query.get(admin_id)
        elif user_id.startswith('staff_'):
            staff_id = int(user_id.replace('staff_', ''))
            return Staff.query.get(staff_id)
        else:
            return User.query.get(int(user_id))
    except (ValueError, IndexError, TypeError):
        return None


# ============================================
# DATABASE INITIALIZATION
# ============================================

def init_db():
    """Initialize database with tables and default admin user"""
    with app.app_context():
        db.create_all()
        print("✅ Database tables created successfully")
        
        admin = Admin.query.first()
        if not admin:
            admin = Admin(
                username='admin',
                email='admin@trekking.com',
                password='admin123',
                full_name='System Administrator'
            )
            db.session.add(admin)
            db.session.commit()
            print("✅ Default admin user created (username: admin, password: admin123)")
        else:
            print("✅ Admin user already exists")


# Initialize database on app startup
with app.app_context():
    db.create_all()
    if Admin.query.first() is None:
        admin = Admin(
            username='admin',
            email='admin@trekking.com',
            password='admin123',
            full_name='System Administrator'
        )
        db.session.add(admin)
        db.session.commit()


# ============================================
# HELPER FUNCTIONS
# ============================================

def role_required(role):
    """Decorator to check user role"""
    def decorator(f):
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash('Please log in first', 'danger')
                return redirect(url_for('login'))
            
            try:
                user_type = type(current_user).__name__
                if user_type == role:
                    return f(*args, **kwargs)
                else:
                    flash('Unauthorized access', 'danger')
                    return redirect(url_for('home'))
            except Exception as e:
                print(f"Role check error: {e}")
                flash('An error occurred', 'danger')
                return redirect(url_for('home'))
        
        decorated_function.__name__ = f.__name__
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
        user_type = request.form.get('user_type')
        
        user = None
        
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
                print(f"✅ User logged in: {user_type} - {username}")
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
        user_type = request.form.get('user_type')
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        full_name = request.form.get('full_name')
        phone = request.form.get('phone')
        
        if user_type == 'staff':
            existing = Staff.query.filter_by(username=username).first()
            if existing:
                flash('Staff username already exists', 'danger')
                return redirect(url_for('register'))
            
            staff = Staff(
                username=username,
                email=email,
                password=password,
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
                password=password,
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
        print(f"Dashboard access: {user_type}")
        
        if user_type == 'Admin':
            return redirect(url_for('admin_dashboard'))
        elif user_type == 'Staff':
            return redirect(url_for('staff_dashboard'))
        elif user_type == 'User':
            return redirect(url_for('user_dashboard'))
        else:
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
    available_treks = Trek.query.filter_by(status='Open').all()
    bookings = Booking.query.filter_by(user_id=user.id).all()
    
    return render_template('user/dashboard.html',
                         available_treks=available_treks,
                         bookings=bookings)


# ============================================
# HOME AND ERROR ROUTES
# ============================================

@app.route('/')
def home():
    """Home page"""
    try:
        if current_user and current_user.is_authenticated:
            return redirect(url_for('dashboard'))
    except:
        pass
    return render_template('home.html')


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return render_template('error.html', error='Page not found'), 404


@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    print(f"Server error: {error}")
    return render_template('error.html', error='Server error'), 500


@app.errorhandler(403)
def forbidden(error):
    """Handle 403 errors"""
    print(f"403 Forbidden error: {error}")
    return render_template('error.html', error='Access forbidden'), 403


# ============================================
# APPLICATION ENTRY POINT
# ============================================

if __name__ == '__main__':
    init_db()
    
    print("\n" + "="*60)
    print("🏔️  TREKKING MANAGEMENT APPLICATION")
    print("="*60)
    print("✅ Using SQLite Database (trekking_app.db)")
    print("✅ Database location: ./trekking_app.db")
    print("✅ Server running on: http://localhost:5000")
    print("✅ Login as: admin / admin123")
    print("="*60 + "\n")
    
    app.run(debug=True, host='localhost', port=5000)
