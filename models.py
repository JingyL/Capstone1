from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

class CollabBoard(db.Model):
    """Board."""

    __tablename__ = 'boards'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    name = db.Column(db.Text, nullable=False, unique=True)

    boardID = db.Column(db.String, nullable=False, unique=True)

