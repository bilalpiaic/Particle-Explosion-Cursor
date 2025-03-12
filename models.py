from app import db
from datetime import datetime

class ParticleSettings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    max_particles = db.Column(db.Integer, default=1000)
    fade_speed = db.Column(db.Float, default=5.0)
    min_size = db.Column(db.Float, default=5.0)
    max_size = db.Column(db.Float, default=20.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class UserPreference(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    theme = db.Column(db.String(50), default='dark')
    particle_color = db.Column(db.String(50), default='white')
    background_color = db.Column(db.String(50), default='black')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
