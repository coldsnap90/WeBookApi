from flask import current_app,url_for
from app.extensions import login_manager,mail,db,Message
from flask_login import UserMixin
import jwt
from datetime import datetime, timezone, timedelta



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key = True)
    email = db.Column(db.String(100),unique=True)
    password = db.Column(db.String(100))
  

    def __repr__(self):
        return f"{self.id}, {self.email},{self.password}"
    
    def send_link(self,user):
        token = self.generate_confirmation_token()
        msg = Message('Campsite booking Notifier',
                    recipients=[user.email])
        confirmation_link = url_for('auth.booking_info',token=token,_external=True)
        msg.body = f'''Your site has been booked, follow the link for details:
    {confirmation_link}
    If you did not make this request then simply ignore this email and no changes will be made.
     '''
        mail.send(msg)

    def generate_confirmation_token(self,expiration=1000000):
        data = {'confirm': self.id,'exp': datetime.now(timezone.utc) + timedelta(seconds=expiration)}
        return jwt.encode(data, current_app.config['SECRET_KEY'], algorithm="HS256")
   
    
    def token_confirm(self, token, leeway=10):
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], leeway=leeway, algorithms=["HS256"])
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        return True
    
    @staticmethod
    def verify_auth_token(token, leeway=10):
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], leeway=leeway, algorithms=["HS256"])
        except:
            return None
        return User.query.get(data['user_id'])
    