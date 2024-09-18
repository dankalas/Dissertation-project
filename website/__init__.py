from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from .celery_config import make_celery
from celery.schedules import crontab
import os;

db = SQLAlchemy()
DB_NAME = "database.db"
DATABASE_URI="postgresql:///postgres:password@localhost:5432/optimizer_app"
db_uri = os.getenv("DATABASE_URI", "sqlite:///database.db")
print(db_uri)

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    
    # Configuring Celery
    app.config['CELERY_BROKER_URL'] =  "redis://localhost:6379/0"
    app.config['CELERY_RESULT_BACKEND'] = "redis://localhost:6379/0"
    

    # Registering Blueprints
    from .views import views
    from .auth import auth
    from .optimizer import optimizer

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(optimizer, url_prefix="/")

    # Celery Beat schedule (without user_id)
    app.config['CELERYBEAT_SCHEDULE'] = {
        'calculate-weekly-summary-every-monday': {
            'task': 'calculate_weekly_summary_task',
            'schedule': crontab(day_of_week=1, hour=0, minute=0),  # Every Monday at midnight
        },
    }
    
    # Configuring Celery
    celery = make_celery(app)
    
    # Initializing the database
    db.init_app(app)
    
    from .models import User, Route, Navigation, WeeklySummary  # Ensure all models are imported
    

    # Create database tables if they don't exist
    with app.app_context():
        db.create_all()

    # Set up the LoginManager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app, celery



def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
        
