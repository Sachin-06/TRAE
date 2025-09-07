from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.urls import url_parse
from models import User, Donation, Delivery, Recipient
from forms import LoginForm, RegistrationForm, DonationForm, DeliveryUpdateForm, RecipientForm
from extensions import db
from datetime import datetime

def register_routes(app):
    # Authentication routes
    @app.route('/')
    def index():
        return render_template('index.html')
    
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user is None or not user.check_password(form.password.data):
                flash('Invalid email or password')
                return redirect(url_for('login'))
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('dashboard')
            return redirect(next_page)
        return render_template('login.html', title='Sign In', form=form)
    
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))
        form = RegistrationForm()
        if form.validate_on_submit():
            user = User(username=form.username.data, email=form.email.data, 
                       user_type=form.user_type.data, phone=form.phone.data, 
                       address=form.address.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Congratulations, you are now a registered user!')
            return redirect(url_for('login'))
        return render_template('register.html', title='Register', form=form)
    
    @app.route('/logout')
    def logout():
        logout_user()
        return redirect(url_for('index'))
    
    # Dashboard route - redirects based on user type
    @app.route('/dashboard')
    @login_required
    def dashboard():
        if current_user.user_type == 'donor':
            return redirect(url_for('donor_dashboard'))
        elif current_user.user_type == 'delivery':
            return redirect(url_for('delivery_dashboard'))
        elif current_user.user_type == 'admin':
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid user type')
            return redirect(url_for('index'))
    
    # Donor routes
    @app.route('/donor/dashboard')
    @login_required
    def donor_dashboard():
        if current_user.user_type != 'donor':
            flash('Access denied')
            return redirect(url_for('dashboard'))
        donations = Donation.query.filter_by(donor_id=current_user.id).order_by(Donation.created_at.desc()).all()
        return render_template('donor/dashboard.html', title='Donor Dashboard', donations=donations)
    
    @app.route('/donor/add_donation', methods=['GET', 'POST'])
    @login_required
    def add_donation():
        if current_user.user_type != 'donor':
            flash('Access denied')
            return redirect(url_for('dashboard'))
        form = DonationForm()
        if form.validate_on_submit():
            donation = Donation(
                donor_id=current_user.id,
                food_type=form.food_type.data,
                quantity=form.quantity.data,
                freshness=form.freshness.data,
                pickup_location=form.pickup_location.data or current_user.address,
                status='pending'
            )
            db.session.add(donation)
            db.session.commit()
            flash('Donation added successfully!')
            return redirect(url_for('donor_dashboard'))
        return render_template('donor/add_donation.html', title='Add Donation', form=form)
    
    @app.route('/donor/donation/<int:id>')
    @login_required
    def view_donation(id):
        if current_user.user_type != 'donor' and current_user.user_type != 'admin':
            flash('Access denied')
            return redirect(url_for('dashboard'))
        donation = Donation.query.get_or_404(id)
        if current_user.user_type == 'donor' and donation.donor_id != current_user.id:
            flash('Access denied')
            return redirect(url_for('donor_dashboard'))
        return render_template('donor/view_donation.html', title='View Donation', donation=donation)
    
    # Delivery person routes
    @app.route('/delivery/dashboard')
    @login_required
    def delivery_dashboard():
        if current_user.user_type != 'delivery':
            flash('Access denied')
            return redirect(url_for('dashboard'))
        deliveries = Delivery.query.filter_by(delivery_person_id=current_user.id).order_by(Delivery.created_at.desc()).all()
        return render_template('delivery/dashboard.html', title='Delivery Dashboard', deliveries=deliveries)
    
    @app.route('/delivery/update/<int:id>', methods=['GET', 'POST'])
    @login_required
    def update_delivery(id):
        if current_user.user_type != 'delivery':
            flash('Access denied')
            return redirect(url_for('dashboard'))
        delivery = Delivery.query.get_or_404(id)
        if delivery.delivery_person_id != current_user.id:
            flash('Access denied')
            return redirect(url_for('delivery_dashboard'))
        form = DeliveryUpdateForm()
        if form.validate_on_submit():
            delivery.status = form.status.data
            if form.status.data == 'picked_up':
                delivery.pickup_time = datetime.utcnow()
                delivery.donation.status = 'in_transit'
            elif form.status.data == 'delivered':
                delivery.delivery_time = datetime.utcnow()
                delivery.confirmation_type = form.confirmation_type.data
                delivery.confirmation_data = form.confirmation_data.data
                delivery.donation.status = 'delivered'
            db.session.commit()
            flash('Delivery status updated successfully!')
            return redirect(url_for('delivery_dashboard'))
        form.status.data = delivery.status
        return render_template('delivery/update_delivery.html', title='Update Delivery', form=form, delivery=delivery)
    
    # Admin routes
    @app.route('/admin/dashboard')
    @login_required
    def admin_dashboard():
        if current_user.user_type != 'admin':
            flash('Access denied')
            return redirect(url_for('dashboard'))
        pending_donations = Donation.query.filter_by(status='pending').order_by(Donation.created_at).all()
        active_deliveries = Delivery.query.filter(Delivery.status != 'delivered').order_by(Delivery.created_at).all()
        delivery_persons = User.query.filter_by(user_type='delivery').all()
        recipients = Recipient.query.all()
        
        # Stats
        total_donations = Donation.query.count()
        delivered_donations = Donation.query.filter_by(status='delivered').count()
        active_delivery_persons = User.query.filter_by(user_type='delivery').count()
        
        return render_template('admin/dashboard.html', title='Admin Dashboard',
                              pending_donations=pending_donations,
                              active_deliveries=active_deliveries,
                              delivery_persons=delivery_persons,
                              recipients=recipients,
                              total_donations=total_donations,
                              delivered_donations=delivered_donations,
                              active_delivery_persons=active_delivery_persons)
    
    @app.route('/admin/assign_delivery/<int:donation_id>', methods=['GET', 'POST'])
    @login_required
    def assign_delivery(donation_id):
        if current_user.user_type != 'admin':
            flash('Access denied')
            return redirect(url_for('dashboard'))
        donation = Donation.query.get_or_404(donation_id)
        if donation.status != 'pending':
            flash('This donation is already assigned')
            return redirect(url_for('admin_dashboard'))
        
        if request.method == 'POST':
            delivery_person_id = request.form.get('delivery_person_id')
            recipient_id = request.form.get('recipient_id')
            
            if not delivery_person_id or not recipient_id:
                flash('Please select both delivery person and recipient')
                return redirect(url_for('assign_delivery', donation_id=donation_id))
            
            delivery = Delivery(
                donation_id=donation_id,
                delivery_person_id=delivery_person_id,
                recipient_id=recipient_id,
                status='assigned'
            )
            donation.status = 'assigned'
            
            db.session.add(delivery)
            db.session.commit()
            flash('Delivery assigned successfully!')
            return redirect(url_for('admin_dashboard'))
        
        delivery_persons = User.query.filter_by(user_type='delivery').all()
        recipients = Recipient.query.all()
        return render_template('admin/assign_delivery.html', title='Assign Delivery',
                              donation=donation,
                              delivery_persons=delivery_persons,
                              recipients=recipients)
    
    @app.route('/admin/recipients')
    @login_required
    def list_recipients():
        if current_user.user_type != 'admin':
            flash('Access denied')
            return redirect(url_for('dashboard'))
        recipients = Recipient.query.all()
        return render_template('admin/recipients.html', title='Recipients', recipients=recipients)
    
    @app.route('/admin/add_recipient', methods=['GET', 'POST'])
    @login_required
    def add_recipient():
        if current_user.user_type != 'admin':
            flash('Access denied')
            return redirect(url_for('dashboard'))
        form = RecipientForm()
        if form.validate_on_submit():
            recipient = Recipient(
                name=form.name.data,
                contact_person=form.contact_person.data,
                phone=form.phone.data,
                address=form.address.data,
                recipient_type=form.recipient_type.data
            )
            db.session.add(recipient)
            db.session.commit()
            flash('Recipient added successfully!')
            return redirect(url_for('list_recipients'))
        return render_template('admin/add_recipient.html', title='Add Recipient', form=form)