from . import db
from flask_login import UserMixin

class Route(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    navigation_id = db.Column(db.Integer, db.ForeignKey('navigation.id'))
    time = db.Column(db.Float)  # Float is more common for time-related data
    distance = db.Column(db.Float)  # Use Float for distances
    calories = db.Column(db.Integer)
    carbon_emissions = db.Column(db.Integer)
    noise_pollution = db.Column(db.Integer)
    scenic_score = db.Column(db.Integer)
    aqi_value = db.Column(db.Integer)
    safety_score = db.Column(db.Integer)
    route_label = db.Column(db.String(255))  # Changed to String, since labels are often text
    rmse = db.Column(db.Float)  # Float works well for most statistical measures

    # Establishing bidirectional relationship if needed
    navigation = db.relationship('Navigation', back_populates='routes')

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    
    # Relationship to navigation history
    navigation_history = db.relationship('Navigation', back_populates='user')

class Navigation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    start_location = db.Column(db.String(255))  
    end_location = db.Column(db.String(255))
    mode = db.Column(db.String(255))
    
    # Relationships
    routes = db.relationship('Route', back_populates='navigation', cascade="all, delete-orphan")
    user = db.relationship('User', back_populates='navigation_history')
