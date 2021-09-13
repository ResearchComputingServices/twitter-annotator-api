import time
from flask import Flask
from flask import request, send_file
from flask import json, jsonify, Response, blueprints
from configparser import ConfigParser
from flask_cors import cross_origin
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

import psycopg2

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:admin@127.0.0.1:5432/twitter_data"

db = SQLAlchemy(app)

migrate = Migrate(app, db)
class QuestionOptionModel(db.Model):
    __tablename__ = 'question_option'

    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer)
    text = db.Column(db.Text)

    def __init__(self, question_id, text):
        self.question_id = question_id
        self.text = text

    def __init__(self, item):
        # BaseModel.__init__(self, item)
        self.id = item.get('id')
        self.text = item.get('text')
        self.question_id = item.get('question_id')

    def __repr__(self):
        return f"<Question {self.text}>"