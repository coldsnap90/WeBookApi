from flask_wtf import FlaskForm

from wtforms import StringField, PasswordField, BooleanField,SubmitField,validators,ValidationError,SelectField,DateField
from wtforms.validators import DataRequired, Length, Email,EqualTo,NumberRange,InputRequired
from app.models import UserMixin, User
from wtforms_validators import ActiveUrl, Alpha, AlphaDash, AlphaSpace,Integer,AlphaNumeric

class LoginForm(FlaskForm):
        email = StringField('Email',validators=[DataRequired(),Length(1,64),Email()])     
        email_password = PasswordField('Password',validators = [DataRequired()]) 
        remember_me = BooleanField('Keep me logged in.')
        account_submit = SubmitField('Log in')

class signupForm(FlaskForm):
        user_email = StringField('Email',validators=[DataRequired(),Length(1,64),Email()])
        email_password = PasswordField('Password',validators = [DataRequired(),Length(1,64)])
        create_account = SubmitField('Create account.')
        
        def validate_email(self,user_email):
                user_email = User.query.filter_by(user_email = user_email.data).first()
                if user_email:
                        raise ValidationError('email already registered.')

