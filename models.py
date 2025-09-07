from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from extensions import db, login_manager

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(120), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    user_type = db.Column(db.String(20))  # 'donor', 'delivery', 'admin'
    phone = db.Column(db.String(20))
    address = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    donations = db.relationship('Donation', backref='donor', lazy='dynamic', foreign_keys='Donation.donor_id')
    deliveries = db.relationship('Delivery', backref='delivery_person', lazy='dynamic', foreign_keys='Delivery.delivery_person_id')
    
    def __repr__(self):
        return f'<User {self.username}> ({self.user_type})'
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

class Donation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    donor_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    food_type = db.Column(db.String(100))
    quantity = db.Column(db.String(100))
    freshness = db.Column(db.String(50))  # e.g., 'Fresh', 'Day old', etc.
    pickup_location = db.Column(db.String(200))
    status = db.Column(db.String(20), default='pending')  # pending, assigned, in_transit, delivered
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship with delivery
    delivery = db.relationship('Delivery', backref='donation', uselist=False)
    
    def __repr__(self):
        return f'<Donation {self.id}: {self.food_type} ({self.status})>'

class Recipient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    contact_person = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    address = db.Column(db.String(200))
    recipient_type = db.Column(db.String(50))  # e.g., 'NGO', 'Old Age Home', etc.
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship with deliveries
    deliveries = db.relationship('Delivery', backref='recipient', lazy='dynamic')
    
    def __repr__(self):
        return f'<Recipient {self.name} ({self.recipient_type})>'

class Delivery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    donation_id = db.Column(db.Integer, db.ForeignKey('donation.id'))
    delivery_person_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    recipient_id = db.Column(db.Integer, db.ForeignKey('recipient.id'))
    status = db.Column(db.String(20), default='assigned')  # assigned, on_the_way, picked_up, delivered
    pickup_time = db.Column(db.DateTime)
    delivery_time = db.Column(db.DateTime)
    confirmation_type = db.Column(db.String(50))  # e.g., 'signature', 'photo', 'feedback'
    confirmation_data = db.Column(db.Text)  # Could store a file path, feedback text, etc.
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Delivery {self.id} for Donation {self.donation_id} ({self.status})>'