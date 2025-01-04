from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Website(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255), nullable=False)
    start_time = db.Column(db.String(10), nullable=True)
    end_time = db.Column(db.String(10), nullable=True)
    slack_user_ids = db.Column(db.String(255), nullable=True)
    tag_here = db.Column(db.Boolean, default=False)  # New field
