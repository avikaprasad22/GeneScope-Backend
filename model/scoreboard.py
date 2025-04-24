from __init__ import db, app
from model.user import User
from sqlalchemy.exc import IntegrityError
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the Scoreboard model
class Scoreboard(db.Model):
    __tablename__ = 'scoreboard'

    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String, db.ForeignKey('users._uid'), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref='scoreboard', lazy=True)

    def __repr__(self):
        return f"<Scoreboard(id={self.id}, uid={self.uid}, score={self.score}, timestamp={self.timestamp})>"

    def read(self):
        return {
            "username": self.user.name,
            "score": self.score,
            "timestamp": self.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        }

# Function to submit a score
def submit_score(uid, score):
    with app.app_context():
        try:
            new_score = Scoreboard(uid=uid, score=score)
            db.session.add(new_score)
            db.session.commit()
            return f"Score submitted successfully for user: {uid}"
        except IntegrityError:
            db.session.rollback()
            return "Failed to submit score: IntegrityError"
        except Exception as e:
            db.session.rollback()
            return f"An error occurred: {str(e)}"

# Function to get top 10 scores
def get_top_scores():
    with app.app_context():
        top_scores = Scoreboard.query.order_by(Scoreboard.score.desc()).limit(10).all()
        return [score.read() for score in top_scores]

# Function to initialize the Scoreboard table
def init_scoreboard():
    with app.app_context():
        db.create_all()
