from flask import Flask
from app.config import Config
from .extensions import db,csrf,login_manager,bcrypt,migrate,mail


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    with app.app_context():
        csrf.init_app(app)
        db.init_app(app)
        bcrypt.init_app(app)
        login_manager.init_app(app)
        mail.init_app(app)


       
        #makes these two blueprints
        
        
        from app.auth import auth as auth_blueprint
        from app.main import main as main_blueprint
    
        app.register_blueprint(auth_blueprint,url_prefix='/auth',templates_folder='templates')
        app.register_blueprint(main_blueprint,url_prefix='/',templates_folder='templates')
        db.create_all()
        
        #app.cli.add_command('create_tables')
    return app
