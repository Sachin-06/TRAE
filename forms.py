from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length
from models import User

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    user_type = SelectField('Register as', choices=[
        ('donor', 'Donor - I have food to donate'),
        ('delivery', 'Delivery Person - I can deliver food'),
        ('admin', 'Admin - I manage the system')
    ])
    phone = StringField('Phone Number', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class DonationForm(FlaskForm):
    food_type = StringField('Type of Food', validators=[DataRequired()])
    quantity = StringField('Quantity', validators=[DataRequired()])
    freshness = SelectField('Freshness', choices=[
        ('Fresh', 'Fresh - Prepared today'),
        ('Day old', 'Day old - Prepared yesterday'),
        ('Packaged', 'Packaged - Has longer shelf life')
    ])
    pickup_location = StringField('Pickup Location (leave blank to use your address)')
    submit = SubmitField('Submit Donation')

class DeliveryUpdateForm(FlaskForm):
    status = SelectField('Update Status', choices=[
        ('assigned', 'Assigned - Waiting to start'),
        ('on_the_way', 'On the way - Going to pickup'),
        ('picked_up', 'Picked up - Food collected'),
        ('delivered', 'Delivered - Food delivered to recipient')
    ])
    confirmation_type = SelectField('Confirmation Type', choices=[
        ('signature', 'Digital Signature'),
        ('photo', 'Photo'),
        ('feedback', 'Feedback')
    ])
    confirmation_data = TextAreaField('Confirmation Details')
    submit = SubmitField('Update Status')

class RecipientForm(FlaskForm):
    name = StringField('Organization Name', validators=[DataRequired()])
    contact_person = StringField('Contact Person', validators=[DataRequired()])
    phone = StringField('Phone Number', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    recipient_type = SelectField('Type of Organization', choices=[
        ('NGO', 'Non-Governmental Organization'),
        ('Old Age Home', 'Old Age Home'),
        ('Shelter', 'Shelter'),
        ('Orphanage', 'Orphanage'),
        ('Other', 'Other')
    ])
    submit = SubmitField('Add Recipient')