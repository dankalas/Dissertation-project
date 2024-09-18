from . import db
from flask_login import UserMixin
from datetime import datetime, timedelta

class Route(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    navigation_id = db.Column(db.Integer, db.ForeignKey('navigation.id'))
    time = db.Column(db.Float)  # Time of the journey in hours
    distance = db.Column(db.Float)  # Distance in kilometers
    calories = db.Column(db.Integer)  # Calories burned during the journey
    carbon_emissions = db.Column(db.Integer)  # Carbon emissions in grams or kilograms
    noise_pollution = db.Column(db.Integer)  # Noise pollution score
    scenic_score = db.Column(db.Integer)  # Scenic score for the journey
    aqi_value = db.Column(db.Integer)  # Air quality index value
    safety_score = db.Column(db.Integer)  # Safety score
    route_label = db.Column(db.String(255))  # Label for the route
    rmse = db.Column(db.Float)  # Root Mean Square Error, for evaluation purposes
    
    # Bidirectional relationship
    navigation = db.relationship('Navigation', back_populates='routes')

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    
    # Relationship to navigation history
    navigation_history = db.relationship('Navigation', back_populates='user')

    # Relationship to weekly summaries
    weekly_summaries = db.relationship('WeeklySummary', back_populates='user')

class Navigation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    start_location = db.Column(db.String(255))  
    end_location = db.Column(db.String(255))
    mode = db.Column(db.String(255))  # Travel mode (e.g., cycling, driving, walking)
    
    # Relationships
    routes = db.relationship('Route', back_populates='navigation', cascade="all, delete-orphan")
    user = db.relationship('User', back_populates='navigation_history')

# New Model: WeeklySummary for tracking carbon emissions and calories
class WeeklySummary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    week_start = db.Column(db.Date)  # Start date of the week
    total_carbon_emissions = db.Column(db.Float)  # Total carbon emissions for the week
    total_calories_burned = db.Column(db.Float)  # Total calories burned for the week
    carbon_diff = db.Column(db.Float)  # Percentage difference in carbon emissions compared to the previous week
    calories_diff = db.Column(db.Float)  # Percentage difference in calories burned compared to the previous week

    # Relationship back to the user
    user = db.relationship('User', back_populates='weekly_summaries')
