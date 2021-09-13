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
class TweetModel(db.Model):
    __tablename__ = 'tweet'

    id_unique = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(db.Text)
    created_at = db.Column(db.Text)
    date = db.Column(db.Text)
    hashtags = db.Column(db.Text)
    id = db.Column(db.Text)
    likes_count = db.Column(db.Text)
    link = db.Column(db.Text)
    location = db.Column(db.Text)
    mentions = db.Column(db.Text)
    name = db.Column(db.Text)
    photos = db.Column(db.Text)
    place = db.Column(db.Text)
    replies_count = db.Column(db.Text)
    retweet = db.Column(db.Text)
    retweets_count = db.Column(db.Text)
    time = db.Column(db.Text)
    relevance = db.Column(db.Text)
    tweet = db.Column(db.Text)
    urls = db.Column(db.Text)
    user_id = db.Column(db.Text)
    username = db.Column(db.Text)
    video = db.Column(db.Text)

    def __init__(self, conversation_id, created_at, date, hashtags, id, likes_count, link, location, mentions, name,
                 photos, place, replies_count, retweet, retweets_count, time, relevance, tweet, urls, user_id, username,
                 video):
        self.conversation_id = conversation_id
        self.created_at = created_at
        self.date = date
        self.hashtags = hashtags
        self.id = id
        self.likes_count = likes_count
        self.link = link
        self.location = location
        self.mentions = mentions
        self.name = name
        self.photos = photos
        self.place = place
        self.replies_count = replies_count
        self.retweet = retweet
        self.retweets_count = retweets_count
        self.time = time
        self.relevance = relevance
        self.tweet = tweet
        self.urls = urls
        self.user_id = user_id
        self.username = username
        self.video = video

    def __repr__(self):
        return f"<Tweet {self.tweet}>"