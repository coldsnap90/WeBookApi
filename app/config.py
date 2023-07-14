import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.database'
    SECRET_KEY = os.environ.get('ENV_SECRET_KEY')
    CSRF_ENABLED = True
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAMES')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORDS')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDERS')
    MAIL_MAX_EMAILS = 1