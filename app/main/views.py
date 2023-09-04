
from app.main import main
from flask import render_template,request,redirect,url_for
from app.main.forms import signupForm
from app.models import *
from flask_login import current_user
from app.extensions import bcrypt,mail
from flask_mail import Message


#create user
@main.route('/',methods =['GET','POST'])
def create_user():
    form = signupForm()
    if current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    signUpForm = signupForm()
    if signUpForm.validate_on_submit():
        salted_password = bcrypt.generate_password_hash(signUpForm.email_password.data).decode('utf-8')
        new_user = User(email = signUpForm.user_email.data,password = salted_password)   
        db.session.add(new_user)
        db.session.commit()
        send_link(new_user,'confirm')
        return redirect(url_for('auth.login'))  
    return render_template('base.html',signup_form=signUpForm)

#send me func
def send_link(*args):
    new_user = args[0]
    token = new_user.generate_confirmation_token()
    if args[1]=='reset':
        msg = Message('Account password reset link',
                    recipients=[new_user.email])
        confirmation_link = url_for('auth.reset_password',token=token,_external=True)
        msg.body = f'''To confirm your password reset, visit the following link:
    {confirmation_link}
    If you did not make this request then simply ignore this email and no changes will be made.'''
 
    else:

        msg = Message('Account confirmation link',
                    recipients=[new_user.email])
        confirmation_link = url_for('auth.confirm',token=token,_external=True)
        msg.body = f'''To confirm your account registration, visit the following link:
    {confirmation_link}
    If you did not make this request then simply ignore this email and no changes will be made.
    '''
    mail.send(msg)
  