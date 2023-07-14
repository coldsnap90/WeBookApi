from app.auth import auth
from flask_login import login_user, current_user, logout_user, login_required
import psycopg2
from psycopg2.extras import RealDictCursor
from app.main.forms import LoginForm,apiRequestUserForm,parkForm,siteForm
from app.models import *
from flask import render_template,redirect,url_for,jsonify,flash
import time
import os

from app.extensions import bcrypt

#connect to databse
def get_db_connect():
    while True:
        try:
            print('db')
            conn = psycopg2.connect(dbname=os.environ.get('DBNAME'), user=os.environ.get('USER'), host=os.environ.get('LOCALHOST'), password=os.environ.get('PASSWORD'), port=os.environ.get('PORT'),cursor_factory = RealDictCursor)
            cur = conn.cursor()
            print('db1')
            return conn,cur
        except Exception as error:
            print('Connecting to DB failed')
        time.sleep(2)
 
    

#login route
@auth.route('/login',methods =['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        print('val on sub')
        email_found = User.query.filter_by(email=form.email.data).first()
        print(email_found)
        if email_found and bcrypt.check_password_hash(email_found.password,form.email_password.data):
            login_user(email_found,remember=form.remember_me.data)
            return redirect(url_for('auth.api_call'))
        else:
            error = True
            print('Email doesnt exist')
    return render_template('login.html',login_form=form)

#logout route
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


#confirm email jwt token
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

#api call link
@auth.route('/api-call')
@login_required
def api_call():
    return render_template('api_call.html')

#get user data
@auth.route('/get-users',methods =['GET'])
@login_required
def get_users():
    conn,cur = get_db_connect()
    cur.execute('SELECT * FROM users;')
    users = cur.fetchall() 
    return jsonify(users),201

#get park data
@auth.route('/get-parks',methods =['GET'])
@login_required
def get_parks():
    conn,cur = get_db_connect()
    cur.execute('SELECT * FROM parks;')
    parks = cur.fetchall()
    return jsonify(parks),201

#get site data
@auth.route('/get-sites',methods =['GET'])
@login_required
def get_sites():
    conn,cur = get_db_connect()
    cur.execute('SELECT * FROM sites;')
    sites = cur.fetchall()
    return jsonify(sites),201

#add user
@auth.route('/add-user',methods=['GET','POST'])
@login_required
def add_user():
    form = apiRequestUserForm()
    if form.is_submitted():
        if form.scan.data == '':
            form.scan.data = '0'

        conn,cur = get_db_connect()
        cur.execute("""INSERT INTO users(id,email,password,first_name,last_name,confirmed,billing_address,postal_code,city,province,country,subscription,
                    c_id,s_id,scan,sub_day,active,phone_num,is_admin) Values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING *""",(form.id.data,form.email.data,
                    form.password.data,form.first_name.data,form.last_name.data,form.confirmed.data,form.address.data,form.postal_code.data,form.city.data,form.province.data,
                        form.country.data,form.subscription.data,form.customer_id.data,form.subscription_id.data,form.scan.data,form.sub_day.data,form.active.data,
                            form.phone_number.data,form.is_admin.data,))
        new_post = cur.fetchone()
        conn.commit()
        return jsonify(new_post),202

    return render_template('user_submit.html',form=form)

#add site
@auth.route('/add-site',methods=['GET','POST'])
@login_required
def add_site():
    form = siteForm()
    if form.is_submitted() and current_user.is_admin:
        if not form.id.data and not form.campground.data and not\
                    form.inner_campground.data and not form.names.data and not form.park_id.data:
            conn,cur = get_db_connect()
            cur.execute("""INSERT INTO users(id,campground,inner_campground,names,park_id) Values(%s,%s,%s,%s,%s) RETURNING *""",(form.id.data,form.campground.data,
                        form.inner_campground.data,form.names.data,form.park_id.data,))
            new_post = cur.fetchone()
            conn.commit()
            return jsonify(new_post),202

    return render_template('site.html',form=form)

#add park
def add_park():
    form = parkForm()
    if form.is_submitted() and current_user.is_admin:
        if not form.id.data and not form.park.data:
            conn,cur = get_db_connect()
            cur.execute("""INSERT INTO users(id,park_site) Values(%s,%s) RETURNING *""",(form.id.data,form.park_site.data,))
            new_post = cur.fetchone()
            conn.commit()
            return jsonify(new_post),202

    return render_template('park.html',form=form)

#delete user
@auth.route('delete-user',methods=['GET','POST'])
@login_required
def delete_user():
    form = apiRequestUserForm()
    if form.is_submitted():
        conn,cur = get_db_connect()
        cur.execute("""DELETE FROM users WHERE id = %s OR email = %s OR first_name = %s AND last_name = %s OR
                        c_id = %s  RETURNING *""",(form.id.data,form.email.data,
                        form.first_name.data,form.last_name.data,form.customer_id.data,))
        new_post = cur.fetchone()
        conn.commit()
        return 202
    return render_template('user_submit.html',form=form)

#delete park
@auth.route('delete-park',methods=['GET','POST'])
@login_required
def delete_park():
        form = parkForm()
        if form.is_submitted() and current_user.is_admin:
       
            conn,cur = get_db_connect()
            cur.execute("""DELETE FROM park WHERE id = %s OR park_site = %s  RETURNING *""",(form.id.data,form.park_site.data,
                            ))
            cur.execute("""DELETE FROM sites WHERE park_id = %s  RETURNING *""",(form.id.data,
                            ))
            conn.commit()
        return 202
#delete site
@auth.route('delete-site',methods=['GET','POST'])
@login_required
def delete_site():
        form = siteForm()
        if form.is_submitted() and current_user.is_admin:
            conn,cur = get_db_connect()
            cur.execute("""DELETE FROM sites WHERE id = %s OR campground = %s AND names = %s  RETURNING *""",(form.id.data,form.campground.data,
                            form.sites.data,))
            conn.commit()
            return 202
        return render_template('site.html',form=form)
     
#route to communicate with front end
@auth.route('/sited/<park>',methods=['GET'])
def sited(park):
    conn,cur = get_db_connect()
    cur.execute("""SELECT * FROM parks WHERE park_site = %s""",(park,))
    park_data = cur.fetchone()
    campSites = park_data
    campArray = []
    camp_temp = ''
    inner_temp =''
    sitesObj = {}
    sitesObj['names'] = 'any site'
    sitesObj['campground'] = camp_temp
    sitesObj['inner_campground'] = inner_temp
    campArray.append(sitesObj)
    for sites in campSites.sites:
            sitesObj = {}
            sitesObj['names'] = sites.names
            if camp_temp != sites.campground:
                camp_temp = sites.campground
                sitesObj['campground'] = camp_temp
            if inner_temp != sites.inner_campground:
                inner_temp = sites.inner_campground
                sitesObj['inner_campground'] = inner_temp
            campArray.append(sitesObj)

    return jsonify({'sites' : campArray})
