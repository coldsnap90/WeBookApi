import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.database'
    SECRET_KEY = os.environ.get('ENV_SECRET_KEY')
    CSRF_ENABLED = True