from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import enum

app = Flask("catalyzapp")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/test.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class User(db.Model):

  class RoleEnum(enum.Enum):
    mentor = "mentor"
    mentee = "mentee"

  class LanguageEnum(enum.Enum):
    english = "english"
    spanish = "spanish"

  facebook_id = db.Column(db.Integer, primary_key=True, nullable=False)
  first_name = db.Column(db.String(50), nullable=False)
  last_name = db.Column(db.String(50), nullable=False)
  email = db.Column(db.String(50), nullable=False)
  image_link = db.Column(db.String(100), nullable=False)
  language = db.Column(db.Enum(LanguageEnum), nullable=False)
  country_of_origin = db.Column(db.String(3), nullable=False)
  gender = db.Column(db.String(50), nullable=False)
  bio = db.Column(db.String(90), nullable=False)
  interest = db.Column(db.String(40), nullable=False)
  role = db.Column(db.Enum(RoleEnum), nullable=False)


class Conversation(db.Model):
  id = db.Column(db.Integer, primary_key=True, nullable=False)
  mentor = db.Column(db.Integer, db.ForeignKey('user.facebook_id'), nullable=False)
  mentee = db.Column(db.Integer, db.ForeignKey('user.facebook_id'), nullable=False)
  timestamp = db.Column(db.DateTime, nullable=False)


class Message(db.Model):
  conversation_id = db.Column(
    db.Integer, db.ForeignKey('conversation.id'), primary_key=True, nullable=False
  )
  sent_by = db.Column(
    db.Integer, db.ForeignKey('user.facebook_id'), primary_key=True, nullable=False
  )
  timestamp = db.Column(db.DateTime, primary_key=True, nullable=False)
  message = db.Column(db.Text, nullable=False)
  timestamp = db.Column(db.DateTime, nullable=False)
