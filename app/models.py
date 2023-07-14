from flask import current_app,url_for
from app.extensions import login_manager,db,Message
from flask_login import UserMixin
import jwt
from datetime import datetime, timezone, timedelta


#login manager
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#user class


class User(db.Model,UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key = True)
    email = db.Column(db.String(100),unique=True)
    password = db.Column(db.String(100))
    is_admin = db.Column(db.Boolean,default = False)
    
  

    def __repr__(self):
        return f"{self.id}, {self.email},{self.password}, {self.is_admin}"
    
    #generate jwt token
    def generate_confirmation_token(self,expiration=1000000):
        data = {'confirm': self.id,'exp': datetime.now(timezone.utc) + timedelta(seconds=expiration)}
        return jwt.encode(data, current_app.config['SECRET_KEY'], algorithm="HS256")
   
   #confirm token
    def token_confirm(self, token, leeway=10):
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], leeway=leeway, algorithms=["HS256"])
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        return True
    #verify token
    @staticmethod
    def verify_auth_token(token, leeway=10):
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], leeway=leeway, algorithms=["HS256"])
        except:
            return None
        return User.query.get(data['user_id'])
    