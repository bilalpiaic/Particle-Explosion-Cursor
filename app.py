import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
app = Flask(__name__)

# Database configuration
database_url = os.environ.get("DATABASE_URL")
logger.debug(f"Database URL found: {'Yes' if database_url else 'No'}")

app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
app.secret_key = os.environ.get("SESSION_SECRET")

# Initialize database
db.init_app(app)

with app.app_context():
    import models
    db.create_all()