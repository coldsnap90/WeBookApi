from flask import Blueprint


#blueprint instantiation
main = Blueprint('main',__name__)
from app.main import views