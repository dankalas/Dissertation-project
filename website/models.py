from . import db
from flask_login import UserMixin

class Route(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    navigation_id = db.Column(db.Integer, db.ForeignKey('navigation.id'))
    time = db.Column(db.Double(10, 2))
    distance = db.Column(db.Double(10, 2))
    calories=db.Column(db.Integer)
    carbon_emissions=db.Column(db.Integer)
    noise_pollution=db.Column(db.Integer)
    scenic_score=db.Column(db.Integer)
    aqi_value=db.Column(db.Integer)
    safety_score=db.Column(db.Integer)
    route_label=db.Column(db.Integer)
    rmse = db.Column(db.Double(10, 2))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    navigation_history = db.relationship('Navigation')
    
class Navigation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    start_location = db.Column(db.String(255))  
    end_location = db.Column(db.String(255))
    mode = db.Column(db.String(255))
    routes = db.relationship('Route')