from . import db
from flask_login import UserMixin

class Route(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    time_w = db.Column(db.String(150))
    calories_w=db.Column(db.String(150))
    carbon_emissions_w=db.Column(db.String(150))
    noise_pollution_w=db.Column(db.String(150))
    scenic_score_w=db.Column(db.String(150))
    aqi_value_w=db.Column(db.String(150))
    accident_rate_w=db.Column(db.String(150))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    Route = db.relationship('Route')