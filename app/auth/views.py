from app.auth import auth
from flask import jsonify,request,render_template,flash
from flask_login import login_user, current_user, logout_user, login_required
import psycopg2
from app.main.forms import LoginForm
from app.models import *
from flask import render_template,request,redirect,url_for,session,current_app
from app.extensions import bcrypt


def get_db_connect():
    conn = psycopg2.connect(dbname='users', user='postgres', host='localhost', password='Machine81', port=5432)
    cur = conn.cursor()
    return cur

@auth.route('/login',methods =['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email_found = User.query.filter_by(email=form.email.data).first()
        
        if email_found and bcrypt.check_password_hash(email_found.password,form.email_password.data):
            login_user(email_found,remember=form.remember_me.data)
            return redirect(url_for('auth.api_call'))
        else:
            error = True
            print('Email doesnt exist')
    return render_template('login.html',login_form=form)

@auth.route('/confirm/<token>',methods=['GET','POST'])
def confirm(token):
    user_id = User.get_id(current_user)
    if current_user.confirmed:
        return redirect(url_for('auth.login'))
    if current_user.confirm(token):
        db.session.commit()
    else:
        flash('link invalid')
        return redirect(url_for('auth.login'))
    return render_template('confirmation.html',token=token)

@auth.route('/api-call')
def api_call():
    return render_template('api_call.html')

@auth.route('/get-users',methods =['GET'])
def get_users():
  
    cur = get_db_connect()
    cur.execute('SELECT * FROM users;')
    users = cur.fetchall()
    user_data = []
    for row in users:
        user = {"id":row[0],'email':row[1], "password":row[2], "First Name":row[4],'Last Name ':row[5],'Confirmed ':row[6],'Billing Address ':row[7],'Postal Code ':row[8],
                'Postal Code ':row[8],'City':row[9],'Province':row[10],'Country':row[11],'Subscription':row[12],'Customer_id':row[13],'Subscription_id':row[14],
                'Scan':row[15],'Sub Day':row[16],'Active':row[17],'Phone Number':row[18]}
        user_data.append(user)
   
    return jsonify(user_data)

@auth.route('/get-parks',methods =['GET'])
@login_required
def get_parks():
    cur = get_db_connect()
    cur.execute('SELECT * FROM parks')
    parks = cur.fetchall()
    parks_data = []
    for row in parks:
        park = {"id":row[0],'park':row[1]}
        parks_data.append(park)

    return jsonify(parks_data)

@auth.route('/get-sites',methods =['GET'])
@login_required
def get_sites():
    cur = get_db_connect()
    cur.execute('SELECT * FROM sites')
    sites = cur.fetchall()
    sites_data = []
    for row in sites:
        site = {"id":row[0],'campground':row[1],'inner_campground':row[2],'names':row[3],'park_id':row[5]}
        sites_data.append(site)

    return jsonify(sites_data)