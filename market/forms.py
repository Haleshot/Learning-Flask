from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from market.models import User


class Register_Form(FlaskForm):

    def validate_username(self, username_to_check): # Checking whether duplicate username doesn't exist and raising error accordingly. We have a field called as username and hence we named the function as validate_username so Flaskform understands that we are checking/validating for the Username field.
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError("Username already exists! Please try a different username")


    def validate_email_address(self, email_address_to_check): # Checking whether duplicate username doesn't exist and raising error accordingly. We have a field called as username and hence we named the function as validate_username so Flaskform understands that we are checking/validating for the Username field.
        email_address = User.query.filter_by(email_address=email_address_to_check.data).first()
        if email_address:
            raise ValidationError("Email Address already exists! Please try a different username")


    username = StringField(label='User Name:', validators=[Length(min=2, max=30), DataRequired()]) # Constricting the username field to minimumn of 2 and maximum of 30 characters and ensuring some data has been entered..
    email_address = StringField(label='Email Address:', validators=[Email(), DataRequired()]) # Checking whether Email is entered correctly in the field and ensuring some data has been entered.
    password1 = PasswordField(label='Password:', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirm Password', validators=[EqualTo('password1'), DataRequired()]) # Ensuring the Confirm password field matches with the password entered in the first place and ensuring some data has been entered..
    submit = SubmitField(label='Create Account')


class Login_Form(FlaskForm):

    username = StringField(label='User Name:', validators=[DataRequired()]) # Constricting the username field to minimumn of 2 and maximum of 30 characters and ensuring some data has been entered..
    password = PasswordField(label='Password:', validators=[DataRequired()]) # Constricting the username field to minimumn of 2 and maximum of 30 characters and ensuring some data has been entered..
    submit = SubmitField(label='Sign In')

class PurchaseItemForm(FlaskForm):
    submit = SubmitField(label='Purchase Item!')

class SellItemForm(FlaskForm):
    submit = SubmitField(label='Sell Item!')