from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, ValidationError, TextAreaField,IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from fsp.models import User
from wtforms.fields.html5 import DateField
from wtforms.widgets import TextArea



class RegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=20)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone=StringField('Phone', validators=[DataRequired(), Length(min=6,max=15)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError("This email already exists! Please choose a different one")

    def validate_phone(self, phone):
        if User.query.filter_by(phone=phone.data).first():
            raise ValidationError("This phone number already exists! Please choose a different one")

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')



class RequestResetForm (FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_username(self, email):
        user = User.query.filter_by(email=email.data).first()
        if not user:
            raise ValidationError('There is no account with that email. You must register first.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')


class ContactForm(FlaskForm):
  name = StringField('Name',validators=[DataRequired()])
  email = StringField('Email',validators=[DataRequired()])
  subject = StringField('Subject')
  message = TextAreaField(u'Message', widget=TextArea(),validators=[DataRequired()])
  submit = SubmitField('Send')

class CompleteOrderForm(FlaskForm):
    number=IntegerField('Unit')
    order_date = DateField('Pick up Date',validators=[DataRequired()])
    submit = SubmitField('Complete order')

class ConfirmOrderForm(FlaskForm):
    order_date = DateField('Pick up Date',validators=[DataRequired()])
    submit = SubmitField('Confirm order')

class VolunteerForm(FlaskForm):
  submit = SubmitField('Send request')

class AddFood(FlaskForm):
    type = StringField('Name',validators=[DataRequired()])
    exp_data = DateField('Expired Data')
    pointfds = StringField('Point')
    quantity = IntegerField('Unit',validators=[DataRequired()])
    submit = SubmitField('Add')

class RemoveFood(FlaskForm):
    type = StringField('Name',validators=[DataRequired()])
    exp_data = DateField('Expired Data')
    pointfds = StringField('Point')
    quantity = IntegerField('Unit',validators=[DataRequired()])
    submit = SubmitField('Remove')

class GiveBonusForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=20)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    bonus=IntegerField('Bonus',validators=[DataRequired()])
    submit = SubmitField('Assign Bonus/Vouchers')

    def validate_bonus(self, bonus):
        if bonus.data > 800:
            raise ValidationError('You are giving a too high bonus! Plese do a double-check or contact Food Sharing Point team!')


