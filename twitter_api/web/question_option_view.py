from __future__ import annotations
from ntpath import join
from flask import Flask
from flask import request, send_file, send_from_directory,current_app
from flask import json, jsonify, Response, blueprints
from configparser import ConfigParser
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# from twitter_api.models.question import QuestionModel
# from twitter_api.models.question_option import QuestionOptionModel
from twitter_api.twitter_database.config_database import config
import psycopg2
from twitter_api.web.common_view import twitter_bp
import random
import csv as csv_lib
import os
from werkzeug.utils import secure_filename
import io
from datetime import datetime
from collections import OrderedDict
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:admin@127.0.0.1:5432/twitter_data"

db = SQLAlchemy(app)

migrate = Migrate(app, db)


class QuestionModel(db.Model):
    __tablename__ = 'question'

    id = db.Column(db.Integer, primary_key=True)
    active = db.Column(db.Boolean)
    question_type = db.Column(db.Integer)
    text = db.Column(db.Text)
    question_number = db.Column(db.Integer)
    version_number = db.Column(db.Integer)
    deleted = db.Column(db.Boolean)
    other = db.Column(db.Boolean)

    def __init__(self, active, question_type, text, question_number, version_number, deleted, other):
        self.active = active
        self.question_type = question_type
        self.text = text
        self.question_number = question_number
        self.version_number = version_number
        self.deleted = deleted
        self.other = other

    def __init__(self, item):
        # BaseModel.__init__(self, item)
        self.id = item.get('id')
        self.active = item.get('active')
        self.question_type = item.get('question_type')
        self.text = item.get('text')
        self.question_number = item.get('question_number')
        self.version_number = item.get('version_number')
        self.deleted = item.get('deleted')
        self.other = item.get('other')

    def __repr__(self):
        return f"<Question {self.text}>"


class QuestionOptionModel(db.Model):
    __tablename__ = 'question_option'

    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer)
    text = db.Column(db.Text)
    version_number = db.Column(db.Integer)

    def __init__(self, question_id, text, version_number):
        self.question_id = question_id
        self.text = text
        self.version_number = version_number

    def __init__(self, item):
        # BaseModel.__init__(self, item)
        self.id = item.get('id')
        self.text = item.get('text')
        self.question_id = item.get('question_id')
        self.version_number = item.get('version_number')

    def __repr__(self):
        return f"<Question {self.text}>"


class TweetModel(db.Model):
    __tablename__ = 'tweet'

    id_unique = db.Column(db.Integer, primary_key=True)
    tweet_id = db.Column(db.Text)
    original_tweet_id = db.Column(db.Text)
    text  = db.Column(db.Text)
    date = db.Column(db.Date)
    time = db.Column(db.Time)
    source = db.Column(db.Text)
    lang = db.Column(db.Text)
    author_username = db.Column(db.Text)
    author_name = db.Column(db.Text)
    author_profile_url = db.Column(db.Text)
    author_description = db.Column(db.Text)
    verified_author = db.Column(db.Boolean)
    media_keys = db.Column(db.Text)
    
    def __init__(self, tweet_id, original_tweet_id,text, date, time, source, lang, author_username, author_name,
                 author_profile_url, author_description, verified_author, media_keys):
        self.tweet_id = tweet_id
        self.original_tweet_id = original_tweet_id
        self.text = text
        self.date = date
        self.source = source
        self.lang = lang
        self.author_username = author_username
        self.author_name = author_name
        self.author_profile_url = author_profile_url
        self.author_description = author_description
        self.verified_author = verified_author
        self.media_keys = media_keys
        self.time = time
        
        
    def __init__(self,item):

        self.tweet_id = item.get('tweet_id')
        self.original_tweet_id = item.get('original_tweet_id')
        self.text = item.get('text')
        self.date = item.get('date')
        self.time = item.get('time')
        self.source = item.get('source')
        self.lang = item.get('lang')
        self.author_username = item.get('author_username')
        self.author_name = item.get('author_name')
        self.author_profile_url = item.get('author_profile_url')
        self.author_description = item.get('author_description')
        self.verified_author = item.get('verified_author')
        self.media_keys = item.get('media_keys')
        

    def __repr__(self):
        return f"<Tweet {self.tweet}>"


class AnnotatedTweetModel(db.Model):
    __tablename__ = 'annotated_tweet'

    id_unique = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Text)
    hashtags = db.Column(db.Text)
    name = db.Column(db.Text)
    tweet = db.Column(db.Text)
    user_id = db.Column(db.Text)

    def __init__(self, id_unique, date, hashtags, name, tweet, user_id):
        self.id_unique = id_unique
        self.date = date
        self.hashtags = hashtags
        self.name = name
        self.tweet = tweet
        self.user_id = user_id

    def __init__(self, item):
        # BaseModel.__init__(self, item)
        self.id_unique = item.get('id_unique')
        self.date = item.get('date')
        self.hashtags = item.get('hashtags')
        self.name = item.get('name')
        self.tweet = item.get('tweet')
        self.user_id = item.get('user_id')

    def __repr__(self):
        return f"<Question {self.tweet}>"


class AnnotationModel(db.Model):
    __tablename__ = 'annotation'

    id = db.Column(db.Integer, primary_key=True)
    tweet_id = db.Column(db.Integer)
    user_id = db.Column(db.Text)
    question_id = db.Column(db.Integer)
    question_option_id = db.Column(db.Integer)
    text_answer = db.Column(db.Text)
    annotation_id = db.Column(db.Integer)

    def __init__(self, id, tweet_id, user_id, question_id, question_option_id, text_answer, annotation_id):
        self.id = id
        self.tweet_id = tweet_id
        self.user_id = user_id
        self.question_id = question_id
        self.question_option_id = question_option_id
        self.text_answer = text_answer
        self.annotation_id = annotation_id

    def __init__(self, item):
        # BaseModel.__init__(self, item)
        self.id = item.get('id')
        self.tweet_id = item.get('tweet_id')
        self.user_id = item.get('user_id')
        self.question_id = item.get('question_id')
        self.question_option_id = item.get('question_option_id')
        self.text_answer = item.get('text_answer')
        self.annotation_id = item.get('annotation_id')

    def __repr__(self):
        return f"<Annotation {self.id}>"
class AssignationModel(db.Model):
    __tablename__ = 'assignation'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Text)
    tweet_id = db.Column(db.Integer)
    answer = db.Column(db.Integer)
    annotate_date = db.Column(db.Date)
    
    def __init__(self, id, user_id, tweet_id, answer, annotate_date):
        self.id = id
        self.tweet_id = tweet_id
        self.user_id = user_id
        self.answer = answer
        self.annotate_date = annotate_date
    def __init__(self, item):
        # BaseModel.__init__(self, item)
        self.id = item.get('id')
        self.tweet_id = item.get('tweet_id')
        self.user_id = item.get('user_id')
        self.answer = item.get('answer')
        self.annotate_date = item.get('annotate_date')

    def __repr__(self):
        return f"<Assignation of tweet {self.tweet_id} to {self.user_id}>"


class RoleModel(db.Model):
    __tablename__ = 'role'

    username = db.Column(db.Text, primary_key=True)
    role = db.Column(db.Text)
    
    def __init__(self, username, role):
        self.username = username
        self.role = role
    def __init__(self, item):
        # BaseModel.__init__(self, item)
        self.username = item.get('username')
        self.role = item.get('role')
        
    def __repr__(self):
        return f"<User {self.username} has role {self.role}>"

@app.route('/api/hello')
def favi():
    return 'Hello', 200


'''
@app.route('/api/load_data', methods=['GET'])
def load_data():
    try:
        id = 1
        content = "Is this the political equivalent of an incel? Where if you don't engage it's a you problem even though the person you're not engaging."
        result = {}
        result["id"] = id
        result["content"] = content
        response = jsonify(result)
    except Exception as e:
        error = {"exception": str(e), "message": "Exception has occurred. Check the format of the request."}
        response = Response(json.dumps(error), 500, mimetype="application/json")
    return response

'''


@app.route('/api/highlight_2', methods=['POST'])
def highlight_2():
    try:
        data = request.get_json()
        # get questions and answers, annotate the tweet based on the user's response
        # answer = data["values"]["Please choose hashtag(s) for this tweet"]
        answer = data["values"]["Please enter hashtag(s) for this tweet, separated by comma "]
        #print(data)
        #print(answer)
        answer_list = answer.split(",")
        answer_list_without_empty_space = []
        for ans in answer_list:
            answer_list_without_empty_space.append(ans.replace(" ", ""))
        #print(answer_list_without_empty_space)
        tweets = TweetModel.query.limit(100).all()
        tweet_results = [
            {
                "id": single_tweet.id_unique,
                "date": single_tweet.date,
                "hashtags": single_tweet.hashtags,
                "name": single_tweet.name,
                "tweet": single_tweet.tweet,
                "user_id": single_tweet.user_id.split('.')[0],
            } for single_tweet in tweets]

        for tweet_result in tweet_results:
            check = any(item in tweet_result["hashtags"] for item in answer_list_without_empty_space)
            if check:
                #print("here")
                max_id = 0
                annotated_tweets = AnnotatedTweetModel.query.all()
                for annotated_tweet in annotated_tweets:
                    if annotated_tweet.id_unique > max_id:
                        max_id = annotated_tweet.id_unique
                annotated_tweet_to_add = {}

                annotated_tweet_to_add["id_unique"] = max_id + 1

                annotated_tweet_to_add["date"] = tweet_result["date"]
                annotated_tweet_to_add["hashtags"] = tweet_result["hashtags"]
                annotated_tweet_to_add["name"] = tweet_result["name"]
                annotated_tweet_to_add["tweet"] = tweet_result["tweet"]
                annotated_tweet_to_add["user_id"] = tweet_result["user_id"]
                tweet_to_add = AnnotatedTweetModel(annotated_tweet_to_add)
                db.session.add(tweet_to_add)
                db.session.commit()

        response = "success", 200

    except Exception as e:
        error = {"exception": str(e), "message": "Exception has occurred. Check the format of the request."}
        response = Response(json.dumps(error), 500, mimetype="application/json")

    return response

def create_annotation_record(record_id, tweet_id, user_id, question_id, answer_db_id, answer, annotation_id):
    annotation = {}
    annotation["id"] = record_id
    annotation["tweet_id"] = tweet_id
    annotation["user_id"] = user_id
    annotation["question_id"] = question_id
    annotation["text_answer"] = ""
    if answer_db_id == None:
        annotation["text_answer"] = answer
    elif answer_db_id == -1:
        annotation["text_answer"] = answer
        annotation["question_option_id"] = answer_db_id
    else:
        annotation["question_option_id"] = answer_db_id
    annotation["annotation_id"] = annotation_id
    return annotation


@app.route('/api/highlight', methods=['POST'])
def highlight():
    try:
        params = request.get_json()
        data = [params['values']]
        tweet_id= params['tweet_id'] #It should come from the front-end (data)
        user_id= params['username'] #It should come from the front-end (data)

        record_count = db.session.query(AnnotationModel.id).count()
        if record_count>0:
            last_record = db.session.query(AnnotationModel).order_by(AnnotationModel.id.desc()).first()
            record_id = last_record.id + 1
            annotation_id = last_record.annotation_id + 1
        else:
            annotation_id = 1
            record_id = 1
        #if record_count>0:
        #    last_record = db.session.query(AnnotationModel).order_by(AnnotationModel.id.desc()).first()
        #    annotation_id = last_record.annotation_id + 1
        #else:
        #    annotation_id = 1

        #Get list of questions
        questions_answers = data

        for q_a in questions_answers: #questions_answers has one element
            questions = q_a.keys()

            other_options_dic = {} #map question id to text of the "other option"
            new_questions_ids = []
            for question in questions:
                if len(question)>=6 and question[:6] == 'other_':
                    id_ = question.split('_')[1]
                    other_options_dic[id_] = q_a[question]
                else:
                    new_questions_ids.append(question)
            for question_id, answer in other_options_dic.items():  #save other options as rows with question_option_id = -1
                answer_db_id = -1
                annotation = create_annotation_record(record_id, tweet_id, user_id, question_id, answer_db_id, answer,
                                                 annotation_id)
                annotation = AnnotationModel(annotation)
                db.session.add(annotation)

                record_id = record_id+1

            for question_id in new_questions_ids:
                # Look for question id in database
                
                answers = q_a[question_id]
                if type(answers)!=list:
                    a = answers
                    answers = []
                    answers.append(a)

                for answer in answers:
                    answer_db = QuestionOptionModel.query.filter_by(text=answer, question_id=question_id).first()
                    if answer_db == None:
                        answer_db_id = None
                    else:
                        answer_db_id = answer_db.id
                    annotation = create_annotation_record(record_id, tweet_id, user_id, question_id, answer_db_id, answer,
                                                 annotation_id)
                    annotation = AnnotationModel(annotation)
                    db.session.add(annotation)

                    record_id = record_id+1

        db.session.commit()
        response = "success", 200

    except Exception as e:
        error = {"exception": str(e), "message": "Exception has occurred. Check the format of the request."}
        response = Response(json.dumps(error), 500, mimetype="application/json")

    return response

@app.route('/api/get_assigned_tweets', methods=['GET'])
def get_assigned_tweets():   #return the id of assigned tweets
    try:
        #data = request.get_json()
        #print(data)
        user_id = request.args.get('username')
        assignations = AssignationModel.query.filter(AssignationModel.user_id==user_id, AssignationModel.answer == 0).all()
        tweet_ids = []
        for assignation in assignations:
            tweet_ids.append(assignation.tweet_id)
    except Exception as e:
        error = {"exception": str(e), "message": "Exception has occurred. Check the format of the request."}
        response = Response(json.dumps(error), 500, mimetype="application/json")

    return {"tweet_ids":tweet_ids}
@app.route('/api/get_tweet_by_id', methods=['GET'])
def get_tweet_by_id(): #get tweet by its dataset id
    try:
        id = request.args.get('id')
        tweet = TweetModel.query.filter_by(id_unique=id).first()
        response = {"tweet_id":tweet.tweet_id,"text":tweet.text}
    except Exception as e:
        error = {"exception": str(e), "message": "Exception has occurred. Check the format of the request."}
        response = Response(json.dumps(error), 500, mimetype="application/json")
    return response

@app.route('/api/update_single_assignation', methods=['PUT'])
def update_single_assignation():
    try:
        data = request.get_json()
        user_id = data['username']
        tweet_id = data['tweet_id']
        assignation = AssignationModel.query.filter(AssignationModel.user_id==user_id, AssignationModel.tweet_id == tweet_id).first()
        assignation.answer = 1
        assignation.annotate_date = datetime.today().strftime('%Y-%m-%d')
        db.session.commit()
        response = "success", 200
    except Exception as e:
        error = {"exception": str(e), "message": "Exception has occurred. Check the format of the request."}
        response = Response(json.dumps(error), 500, mimetype="application/json")
    return response
    
@app.route('/api/skip_irrelevant_tweet', methods=['PUT'])
def skip_irrelevant_tweet():
    try:
        data = request.get_json()
        user_id = data['username']
        tweet_id = data['tweet_id']
        assignation = AssignationModel.query.filter(AssignationModel.user_id==user_id, AssignationModel.tweet_id == tweet_id).first()
        assignation.answer = 2
        assignation.annotate_date = datetime.today().strftime('%Y-%m-%d')
        db.session.commit()
        response = "success", 200
    except Exception as e:
        error = {"exception": str(e), "message": "Exception has occurred. Check the format of the request."}
        response = Response(json.dumps(error), 500, mimetype="application/json")
    return response


@app.route('/api/get_question_option', methods=['GET'])
def get_question_option():
    try:
        # print('get_question_option')
        questions = QuestionModel.query.all()
        questions = QuestionModel.query.filter_by(deleted=False).all()
        #print(questions)
        Question_results = [
            {
                "id": question.id,
                "active": question.active,
                "question_type": question.question_type,
                "text": question.text,
                "question_number": question.question_number,
                "other": question.other

            } for question in questions]
        # print(Question_results)
        Question_id_unsort = []
        for Question_result in Question_results:
            Question_id_unsort.append(Question_result.get("question_number"))

        Question_id_sorted = sorted(Question_id_unsort)
        Question_results_sorted = []
        for i in range(len(Question_id_sorted)):
            for Question_result in Question_results:
                if Question_result.get("question_number") == Question_id_sorted[i] and Question_result.get(
                        "active") == True:
                    Question_results_sorted.append(Question_result)

        questions_options = QuestionOptionModel.query.all()
        Question_options_results = [
            {
                "id": question_option.id,
                "question_id": question_option.question_id,
                "text": question_option.text
            } for question_option in questions_options]

        Question_option_id_unsort = []
        for Question_option_result in Question_options_results:
            Question_option_id_unsort.append(Question_option_result.get("id"))

        Question_option_id_sorted = sorted(Question_option_id_unsort)
        Question_option_results_sorted = []
        for i in range(len(Question_option_id_sorted)):
            for Question_option_result in Question_options_results:
                if Question_option_result.get("id") == Question_option_id_sorted[i]:
                    Question_option_results_sorted.append(Question_option_result)

        response = {"questions": Question_results_sorted, "options": Question_option_results_sorted}
    except Exception as e:
        error = {"exception": str(e), "message": "Exception has occurred. Check the format of the request."}
        response = Response(json.dumps(error), 500, mimetype="application/json")
    return response


@app.route('/api/get_tweet_id', methods=['GET'])
def get_tweet_id():
    try:
        tweets_count =  db.session.query(TweetModel.id_unique).count()
        id_random = random.randint(0, tweets_count)
        tweet = TweetModel.query.filter_by(id_unique=id_random).first()
        full_link = tweet.link
        link_list = full_link.split("/")
        id_for_tweet = link_list[len(link_list)-1]
        response = jsonify(id_for_tweet)
    except Exception as e:
        error = {"exception": str(e), "message": "Exception has occurred. Check the format of the request."}
        response = Response(json.dumps(error), 500, mimetype="application/json")
    return response


@app.route('/api/get_all_question_option', methods=['GET'])
def get_all_question_option():
    try:
        # print('get_all_question_option')
        questions = QuestionModel.query.all()
        questions = QuestionModel.query.filter_by(deleted=False).all()
        Question_results = [
            {
                "id": question.id,
                "active": question.active,
                "question_type": question.question_type,
                "text": question.text,
                "deleted": question.deleted,
                "question_number": question.question_number,
                "other": question.other
            } for question in questions]
        Question_id_unsort = []
        for Question_result in Question_results:
            Question_id_unsort.append(Question_result.get("question_number"))
        Question_id_sorted = sorted(Question_id_unsort)
        Question_results_sorted = []
        for i in range(len(Question_id_sorted)):
            for Question_result in Question_results:
                if Question_result.get("question_number") == Question_id_sorted[i]:

                    if Question_result["deleted"] is False:
                        Question_results_sorted.append(Question_result)
        questions_options = QuestionOptionModel.query.all()
        Question_options_results = [
            {
                "id": question_option.id,
                "question_id": question_option.question_id,
                "text": question_option.text
            } for question_option in questions_options]
        Question_option_id_unsort = []
        for Question_option_result in Question_options_results:
            Question_option_id_unsort.append(Question_option_result.get("id"))
        Question_option_id_sorted = sorted(Question_option_id_unsort)
        Question_option_results_sorted = []
        for i in range(len(Question_option_id_sorted)):
            for Question_option_result in Question_options_results:
                if Question_option_result.get("id") == Question_option_id_sorted[i]:
                    Question_option_results_sorted.append(Question_option_result)
        # print("success")
        response = {"questions": Question_results_sorted, "options": Question_option_results_sorted}
    except Exception as e:
        error = {"exception": str(e), "message": "Exception has occurred. Check the format of the request."}
        response = Response(json.dumps(error), 500, mimetype="application/json")
    return response


@app.route('/api/get_single_question_option', methods=['GET'])
def get_single_question_option():
    try:
        #print('get_single_question_option')
        specific_id = request.args.get('id')

        single_question = QuestionModel.query.filter_by(id=int(specific_id)).first()
        single_specific_question = {
            "id": single_question.id,
            "active": single_question.active,
            "question_type": single_question.question_type,
            "text": single_question.text,
            "other": single_question.other
        }

        single_question_text = single_question.text

        questions_options = QuestionOptionModel.query.all()
        Question_options_results = [
            {
                "id": question_option.id,
                "question_id": question_option.question_id,
                "text": question_option.text
            } for question_option in questions_options]
        specific_options = []
        for Question_options_result in Question_options_results:

            if Question_options_result["question_id"] == int(specific_id):
                specific_options.append(Question_options_result)

        response = {"question": single_specific_question, "options": specific_options}
    except Exception as e:
        error = {"exception": str(e), "message": "Exception has occurred. Check the format of the request."}
        response = Response(json.dumps(error), 500, mimetype="application/json")
    return response


@app.route('/api/update_single_question_option', methods=['PUT'])
def update_single_question_option():
    try:
        data = request.get_json()
        #print("update here")
        #print(data)
        #print(data.get('id'))
        # question = QuestionModel.query.filter_by(id=data.get('id')).first()
        question = QuestionModel.query.filter_by(id=data.get('id')).first()
        #print(question)
        #print(question.question_number)
        #print(question.version_number)
        q_n = question.question_number
        # provider.update(data, article)
        # question.question_type = data.get('question_type')
        # db.session.commit()
        
        if data["type"] == "radio":
            int_question_type = 0
        elif data["type"] == "checkbox":
            int_question_type = 1
        else:
            int_question_type = 2
        if data["active"] == "true":
            question_active = True
        else:
            question_active = False
        
        
        question.active = False
        question.question_type = int_question_type
        question.text = data.get('text')
        question.question_number = q_n
        question.deleted = True
        db.session.commit()

        #print("reate_single_question_option")
        data = request.get_json()
        #print(data)
        questions = QuestionModel.query.all()
        max_id = 0
        for s_question in questions:
            if s_question.id > max_id:
                max_id = s_question.id

        question_other_option = False
        question_data = {}
        if data["type"] == "radio":
            int_question_type = 0
            if data["other"] == "true":
                question_other_option = True
        elif data["type"] == "checkbox":
            int_question_type = 1
            if data["other"] == "true":
                question_other_option = True
        else:
            int_question_type = 2
        if data["active"] == "true":
            question_active = True
        else:
            question_active = False

        question_data["id"] = int(max_id + 1)
        question_data["active"] = question_active
        question_data["question_type"] = int_question_type
        question_data["text"] = data["text"]

        question_data["other"] = question_other_option

        question_data["question_number"] = question.question_number
        question_data["version_number"] = question.version_number + 1
        question_data["deleted"] = False

        questions_to_add = QuestionModel(question_data)
        db.session.add(questions_to_add)
        db.session.commit()

        # question_options = QuestionOptionModel.query.all()
        # print("start")
        # print(question_options)
        # for question_option in question_options:
        #     print(question_option.question_id)
        #     if question_option.question_id == data.get('id'):
        #         db.session.delete(question_option)
        #         db.session.commit()
        if int_question_type == 0 or int_question_type == 1:
            #print("only if radio and checkbox")
            for option in data["options"]:

                max_option_id = 0
                question_options = QuestionOptionModel.query.all()
                for option_id in question_options:
                    if option_id.id > max_option_id:
                        max_option_id = option_id.id

                option_data_to_add = {}
                #print("here", max_option_id)

                option_data_to_add["id"] = max_option_id + 1
                option_data_to_add["text"] = option

                option_data_to_add["question_id"] = int(max_id + 1)
                option_data_to_add["version_number"] = question.version_number + 1
                # option_data_to_add["active"] = question_active
                option_to_add = QuestionOptionModel(option_data_to_add)
                db.session.add(option_to_add)
                db.session.commit()

        #print("success")
        response = "success", 200

    except Exception as e:
        error = {"exception": str(e), "message": "Exception has occurred. Check the format of the request."}
        response = Response(json.dumps(error), 500)

    return response


@app.route('/api/update_single_question_option_active_only', methods=['PUT']) #change just the active status of question
def update_single_question_option_active_only():
    try:
        data = request.get_json()
        #print("update active status")
        #print(data)
        #print(data.get('id'))
        question = QuestionModel.query.filter_by(id=data.get('id')).first()
        #print(question)
        question.active = data.get('active')
        db.session.commit()

        #print("success")
        response = "success", 200

    except Exception as e:
        error = {"exception": str(e), "message": "Exception has occurred. Check the format of the request."}
        response = Response(json.dumps(error), 500)

    return response


@app.route('/api/delete_single_question_option', methods=['DELETE'])
def delete_single_question_option():
    try:
        data = request.get_json()
        #print("**update active status")
        #print(data)
        #print(data.get('id'))
        question = QuestionModel.query.filter_by(id=data.get('id')).first()
        
        annotations = AnnotationModel.query.filter(AnnotationModel.question_id == question.id).first()
        if annotations:
            question.active = False
            question.deleted = True
            db.session.commit()
        else:
            db.session.delete(question)
            # data = request.get_json()
            #print('delete_single_question_option')
            specific_id = data["id"]
            corresponding_options = data["options"]

            # single_question_to_delete = QuestionModel.query.filter_by(id=specific_id).first()

            if corresponding_options == []:
                max_option_id = 0
                question_options = QuestionOptionModel.query.all()
                for option in question_options:
                    if option.id > max_option_id:
                        max_option_id = option.id
                option_data_to_add = {}

                option_data_to_add["id"] = max_option_id + 1
                option_data_to_add["text"] = "a"

                option_data_to_add["question_id"] = data.get('id')
                option_data_to_add["version_number"] = 1
                option_to_add = QuestionOptionModel(option_data_to_add)
                db.session.add(option_to_add)
                db.session.commit()
                single_option_to_delete = QuestionOptionModel.query.filter_by(id=option_data_to_add["id"]).first()
                db.session.delete(single_option_to_delete)
                db.session.commit()
            for corresponding_option in corresponding_options:
                single_option_to_delete = QuestionOptionModel.query.filter_by(id=corresponding_option["id"]).first()
                if single_option_to_delete:
                    db.session.delete(single_option_to_delete)
                    db.session.commit()
                    #print(single_option_to_delete)
        
        '''
        if single_question_to_delete:
            db.session.delete(single_question_to_delete)
            db.session.commit()
            response = "success", 200
        else:
            response = "Failed", 404
        '''
        response = "success", 200
    except Exception as e:
        error = {"exception": str(e), "message": "Exception has occurred. Check the format of the request."}
        response = Response(json.dumps(error), 500, mimetype="application/json")
    return response


'''
@app.route('/api/delete_single_question_option', methods=['DELETE'])
def delete_single_question_option():
    try:
        data = request.get_json()
        print("update active status")
        print(data)
        print(data.get('id'))
        question = QuestionModel.query.filter_by(id=data.get('id')).first()
        print(question)

        # provider.update(data, article)
        question.deleted = True
        question.active = False
        db.session.delete()
        db.session.commit()

        print("success")
        response = "success", 200

    except Exception as e:
        error = {"exception": str(e), "message": "Exception has occurred. Check the format of the request."}
        response = Response(json.dumps(error), 500, mimetype="application/json")
    return response
'''


@app.route('/api/create_single_question_option', methods=['POST'])
def create_single_question_option():
    try:
        #print("reate_single_question_option")
        data = request.get_json()
        #print(data)
        questions = QuestionModel.query.all()
        max_id = 0
        for question in questions:
            if question.id > max_id:
                max_id = question.id

        question_data = {}
        if data["type"] == "radio":
            int_question_type = 0
        elif data["type"] == "checkbox":
            int_question_type = 1
        else:
            int_question_type = 2
        if data["active"] == "true":
            question_active = True
        else:
            question_active = False

        question_other_option = False
        if int_question_type !=2:
            if data["other"] == "true":
                question_other_option = True
        
        question_data["id"] = int(max_id + 1)
        question_data["active"] = question_active
        question_data["question_type"] = int_question_type
        question_data["text"] = data["text"]
        question_data['other'] = question_other_option

        max_question_number = 0
        for question in questions:

            if question.question_number > max_question_number:
                max_question_number = question.question_number

        question_data["question_number"] = max_question_number + 1
        question_data["version_number"] = 1
        question_data["deleted"] = False

        questions_to_add = QuestionModel(question_data)
        db.session.add(questions_to_add)
        db.session.commit()

        if int_question_type == 0 or int_question_type == 1:
            for option_data in data["options"]:
                max_option_id = 0
                question_options = QuestionOptionModel.query.all()
                for option in question_options:
                    if option.id > max_option_id:
                        max_option_id = option.id
                option_data_to_add = {}

                option_data_to_add["id"] = max_option_id + 1
                option_data_to_add["text"] = option_data

                option_data_to_add["question_id"] = max_id + 1
                option_data_to_add["version_number"] = 1
                option_to_add = QuestionOptionModel(option_data_to_add)
                db.session.add(option_to_add)
                db.session.commit()

        response = "success", 200

    except Exception as e:
        error = {"exception": str(e), "message": "Exception has occurred. Check the format of the request."}
        response = Response(json.dumps(error), 500)

    return response


@app.route('/api/get_all_tweets', methods=['GET'])
def get_all_tweets():
    try:
        tweets = TweetModel.query.limit(1000).all()
        tweet_results = [
            {
                "id": single_tweet.id_unique,
                "date": single_tweet.date,
                "hashtags": single_tweet.hashtags,
                "name": single_tweet.name,
                "tweet": single_tweet.tweet,
                "user_id": single_tweet.user_id.split('.')[0],
                "annotated": "No"
            } for single_tweet in tweets]

        # tweet = TweetModel.query.filter_by(id_unique=2).first()
        # full_link = tweet.link
        # id_for_tweet = full_link.split("/")
        # response = jsonify()

        response = {"tweets": tweet_results}

    except Exception as e:
        error = {"exception": str(e), "message": "Exception has occurred. Check the format of the request."}
        response = Response(json.dumps(error), 500, mimetype="application/json")
    return response


@app.route('/api/get_all_tweets_annotated', methods=['GET'])
def get_all_tweets_annotated():
    try:
        tweets = AnnotatedTweetModel.query.limit(1000).all()
        tweet_results = [
            {
                "id": single_tweet.id_unique,
                "date": single_tweet.date,
                "hashtags": single_tweet.hashtags,
                "name": single_tweet.name,
                "tweet": single_tweet.tweet,
                "user_id": single_tweet.user_id.split('.')[0],
                "annotated": "Yes"
            } for single_tweet in tweets]

        # tweet = TweetModel.query.filter_by(id_unique=2).first()
        # full_link = tweet.link
        # id_for_tweet = full_link.split("/")
        # response = jsonify()

        response = {"tweets": tweet_results}

    except Exception as e:
        error = {"exception": str(e), "message": "Exception has occurred. Check the format of the request."}
        response = Response(json.dumps(error), 500, mimetype="application/json")
    return response


@app.route('/api/get_single_tweet', methods=['GET'])
def get_single_tweets():
    try:

        response = "success", 200

    except Exception as e:
        error = {"exception": str(e), "message": "Exception has occurred. Check the format of the request."}
        response = Response(json.dumps(error), 500, mimetype="application/json")
    return response


#-------------------------------------Tweet Admin Panel--------------------------------------------------------------------

    
def save_tweets(tweets,path):
    rows = tweets
    columns_to_exclude = set(['_sa_instance_state'])
    
    #create list of column names  
    column_names = [i for i in rows[0].__dict__]
    for column_name in columns_to_exclude:
        column_names.pop(column_names.index(column_name))
    
    f = open(path, 'w', encoding='UTF8',newline= '')
    writer = csv_lib.writer(f,delimiter = ',')
    writer.writerow(column_names)
    for row in rows:
        lst = []
        for column_name in column_names:
            if column_name not in columns_to_exclude:
                data = str(row.__dict__[column_name])
                lst.append(data)
        writer.writerow(lst)
    f.close()
    return




@app.route('/api/download', methods=['GET'])
def download_file():
    filename = request.args.get('filename')
    path = os.path.join(current_app.root_path, 'downloads')
    return send_from_directory(path, filename, as_attachment=True)

@app.route('/api/get_tweets_by_date', methods=['GET'])
def get_tweets_by_date():
    try:
        date1 = request.args.get('date1')
        date2 = request.args.get('date2')
        unassigned = request.args.get('unassigned')
        if unassigned == 'true':
            tweets = TweetModel.query.filter(TweetModel.date>=date1).filter(TweetModel.date<=date2).filter(~db.exists().where(AssignationModel.tweet_id == TweetModel.id_unique)).all()
        else:
            tweets = TweetModel.query.filter(TweetModel.date>=date1).filter(TweetModel.date<=date2).all()
        if not tweets:
            return "No tweet to download",200

        path = os.path.join(current_app.root_path, 'downloads')
        if not os.path.isdir(path):
            os.makedirs(path)
        path = os.path.join(path, 'tweets.csv')

        save_tweets(tweets,path)
        response = "success", 200
        return response
    except Exception as e:
        error = {"exception": str(e), "message": "Exception has occurred. Check the format of the request."}
        response = Response(json.dumps(error), 500, mimetype="application/json")
    return response

@app.route('/api/get_random_tweets', methods=['GET'])
def get_random_tweets():
    try:
        num = request.args.get('num')
        tweets = TweetModel.query.filter(~db.exists().where(AssignationModel.tweet_id == TweetModel.id_unique)).order_by(db.func.random()).limit(num)
        if not tweets:
            return "No tweet to download",200
        
        path = os.path.join(current_app.root_path, 'downloads')
        if not os.path.isdir(path):
            os.makedirs(path)
        path = os.path.join(path, 'tweets.csv')
        save_tweets(tweets,path)
        response = "success", 200
        return response
    except Exception as e:
        error = {"exception": str(e), "message": "Exception has occurred. Check the format of the request."}
        response = Response(json.dumps(error), 500, mimetype="application/json")
    return response


def save_assignation_from_csv(file,annotator_username):
    stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
    csv_input = csv_lib.reader(stream)

    row_counter = 0
    for row in csv_input:
        if row_counter == 0:
            id_index = row.index('id_unique')
            row_counter += 1
        else:
            tweet_id = row[id_index]
            if tweet_id:
                assigned_tweet = AssignationModel.query.filter(AssignationModel.tweet_id == tweet_id, AssignationModel.user_id == annotator_username).first()
                if not assigned_tweet: #prevent an already assigned tweet to assign to the same user again
                    assignation = {'user_id':annotator_username, 'tweet_id': tweet_id, 'answer': 0} 
                    assignation = AssignationModel(assignation)
                    db.session.add(assignation)

    db.session.commit()
    
    return

@app.route('/api/assign_tweets', methods=['POST'])
def assign_tweets():
    try:

        annotator_username = request.form.get('annotator')
        file = request.files['file'] 
        save_assignation_from_csv(file,annotator_username)
        response = "success", 200

    except Exception as e:
        error = {"exception": str(e), "message": "Exception has occurred. Check the format of the request."}
        response = Response(json.dumps(error), 500)

    return response


@app.route('/api/assign_random_tweets', methods=['POST'])
def assign_random_tweets():
    try:
        params = request.get_json()
        annotator_username = params['username']
        tweets = TweetModel.query.filter(~db.exists().where(AssignationModel.tweet_id == TweetModel.id_unique)).order_by(db.func.random()).limit(100)
        for tweet in tweets:
            assignation = {'user_id':annotator_username, 'tweet_id': tweet.id_unique, 'answer': 0} 
            assignation = AssignationModel(assignation)
            db.session.add(assignation)
        db.session.commit()
        response = "success", 200

    except Exception as e:
        error = {"exception": str(e), "message": "Exception has occurred. Check the format of the request."}
        response = Response(json.dumps(error), 500)

    return response


def save_annotations(annotations_dic,path):
    column_names = ['Annotator', 'Date of Annotation','Annotation id','Tweet id in database', 'Tweet text', 'Question', 'Answer', 'Question', 'Answer', '...' ]
    f = open(path, 'w', encoding='UTF8',newline= '')
    writer = csv_lib.writer(f,delimiter = ',')
    writer.writerow(column_names)
    for annotation_id, annot in annotations_dic.items():
        lst = []
        lst.append(annot['annotator'])
        lst.append(annot['annotate_date'])
        lst.append(str(annotation_id))
        lst.append(str(annot['tweet_id']))
        lst.append(annot['tweet_text'])
        questions = annot['questions']
        for question_id,question_details in questions.items():
            lst.append(question_details[0])
            answers = ""
            for answer in question_details[1]:
                answers += ("\"" + answer + "\",")
            lst.append(answers[:-1])
        writer.writerow(lst)
    f.close()
    return
def prepare_annotations(annotations,annotations2,annotations3):
    annotations_dic = OrderedDict()
    for record in annotations:
        annotation_id = record[0]
        tweet_id = record[1]
        tweet_text = record[2]
        question_id = record[3]
        question_type = record[4]
        question_text = record[5]
        annotation_text_answer = record[6]  #Not null if question type is 2 or question has other option
        annotate_date = record[7]
        annotator_id = record[8]
        option_text = record[9]
        
        annotation = annotations_dic.get(annotation_id)
        
        if not annotation:
            annotation = OrderedDict()
            annotation['tweet_id'] = tweet_id
            annotation['tweet_text'] = tweet_text
            annotation['annotate_date'] = annotate_date
            annotation['annotator'] = annotator_id
        questions = annotation.get('questions')
        if not questions:
            questions = OrderedDict()
        question = questions.get(question_id) #[text,[answers]]
        if question:
            question[1].append(option_text)
        else:
            if question_type == 2:
                question = [question_text,[annotation_text_answer]]
            else:
                question = [question_text,[option_text]]
            questions[question_id] = question
        annotation['questions'] = questions

        annotations_dic[annotation_id] = annotation

    for record in annotations3:  # records related to other options
        annotation_id = record[0]
        tweet_id = record[1]
        tweet_text = record[2]
        question_id = record[3]
        question_type = record[4]
        question_text = record[5]
        annotation_text_answer = record[6]  #Not null if question type is 2 or question has other option
        annotate_date = record[7]
        annotator_id = record[8]

        annotation = annotations_dic.get(annotation_id)
        
        if not annotation:
            annotation = OrderedDict()
            annotation['tweet_id'] = tweet_id
            annotation['tweet_text'] = tweet_text
            annotation['annotate_date'] = annotate_date
            annotation['annotator'] = annotator_id
        questions = annotation.get('questions')
        if not questions:
            questions = OrderedDict()
        question = questions.get(question_id) #[text,[answers]]
        if question:
            question[1].append(annotation_text_answer)
        else:
            if question_type == 2:
                question = [question_text,[annotation_text_answer]]
            else:
                if annotation_text_answer:
                    question = [question_text,[annotation_text_answer]]
                else:
                    print('error')
            questions[question_id] = question
        annotation['questions'] = questions

        annotations_dic[annotation_id] = annotation
    for record in annotations2: #records related to text questions
        annotation_id = record[0]
        tweet_id = record[1]
        tweet_text = record[2]
        question_id = record[3]
        question_type = record[4]
        question_text = record[5]
        annotation_text_answer = record[6] #Not null if question type is 2 or question has other option
        annotate_date = record[7]
        annotator_id = record[8]

        annotation = annotations_dic.get(annotation_id)
        
        if not annotation:
            annotation = OrderedDict()
            annotation['tweet_id'] = tweet_id
            annotation['tweet_text'] = tweet_text
            annotation['annotate_date'] = annotate_date
            annotation['annotator'] = annotator_id
        questions = annotation.get('questions')
        if not questions:
            questions = OrderedDict()
        question = questions.get(question_id) #[text,[answers]]
        if question:
            print('error')
        else:
            if question_type == 2:
                question = [question_text,[annotation_text_answer]]
            else:
                print('error')
            questions[question_id] = question
        annotation['questions'] = questions

        annotations_dic[annotation_id] = annotation
    


    return annotations_dic

@app.route('/api/get_annotations', methods=['GET'])
def get_annotations():
    
    try:
        annotator_username = request.args.get('annotator')
        if annotator_username != 'all':
            annotations = db.session.query(AnnotationModel,TweetModel,QuestionModel,QuestionOptionModel, AssignationModel).join(TweetModel,AnnotationModel.tweet_id==TweetModel.id_unique)\
            .join(QuestionModel,AnnotationModel.question_id == QuestionModel.id).join(QuestionOptionModel,AnnotationModel.question_option_id == QuestionOptionModel.id).join(AssignationModel, (AnnotationModel.user_id == AssignationModel.user_id) & (AnnotationModel.tweet_id == AssignationModel. tweet_id)).filter(AnnotationModel.user_id == annotator_username).with_entities(AnnotationModel.annotation_id, TweetModel.id_unique, TweetModel.text, AnnotationModel.question_id, QuestionModel.question_type, QuestionModel.text, AnnotationModel.text_answer, AssignationModel.annotate_date,  AnnotationModel.user_id, QuestionOptionModel.text).all()
            annotations2 = db.session.query(AnnotationModel,TweetModel,QuestionModel,AssignationModel).join(TweetModel,AnnotationModel.tweet_id==TweetModel.id_unique)\
            .join(QuestionModel,AnnotationModel.question_id == QuestionModel.id).join(AssignationModel, (AnnotationModel.user_id == AssignationModel.user_id) & (AnnotationModel.tweet_id == AssignationModel. tweet_id)).filter(AnnotationModel.user_id == annotator_username).filter(AnnotationModel.question_option_id == None).with_entities(AnnotationModel.annotation_id, TweetModel.id_unique, TweetModel.text, AnnotationModel.question_id, QuestionModel.question_type, QuestionModel.text, AnnotationModel.text_answer, AssignationModel.annotate_date, AnnotationModel.user_id).all()
            annotations3 = db.session.query(AnnotationModel,TweetModel,QuestionModel,AssignationModel).join(TweetModel,AnnotationModel.tweet_id==TweetModel.id_unique)\
            .join(QuestionModel,AnnotationModel.question_id == QuestionModel.id).join(AssignationModel, (AnnotationModel.user_id == AssignationModel.user_id) & (AnnotationModel.tweet_id == AssignationModel. tweet_id)).filter(AnnotationModel.user_id == annotator_username).filter(AnnotationModel.question_option_id == -1).with_entities(AnnotationModel.annotation_id, TweetModel.id_unique, TweetModel.text, AnnotationModel.question_id, QuestionModel.question_type, QuestionModel.text, AnnotationModel.text_answer, AssignationModel.annotate_date, AnnotationModel.user_id).all()
        else:
            annotations = db.session.query(AnnotationModel,TweetModel,QuestionModel,QuestionOptionModel,AssignationModel).join(TweetModel,AnnotationModel.tweet_id==TweetModel.id_unique)\
            .join(QuestionModel,AnnotationModel.question_id == QuestionModel.id).join(QuestionOptionModel,AnnotationModel.question_option_id == QuestionOptionModel.id).join(AssignationModel, (AnnotationModel.user_id == AssignationModel.user_id) & (AnnotationModel.tweet_id == AssignationModel. tweet_id)).with_entities(AnnotationModel.annotation_id, TweetModel.id_unique, TweetModel.text, AnnotationModel.question_id, QuestionModel.question_type, QuestionModel.text, AnnotationModel.text_answer, AssignationModel.annotate_date, AnnotationModel.user_id, QuestionOptionModel.text).all()
            annotations2 = db.session.query(AnnotationModel,TweetModel,QuestionModel,AssignationModel).join(TweetModel,AnnotationModel.tweet_id==TweetModel.id_unique)\
            .join(QuestionModel,AnnotationModel.question_id == QuestionModel.id).join(AssignationModel, (AnnotationModel.user_id == AssignationModel.user_id) & (AnnotationModel.tweet_id == AssignationModel. tweet_id)).filter(AnnotationModel.question_option_id == None).with_entities(AnnotationModel.annotation_id, TweetModel.id_unique, TweetModel.text, AnnotationModel.question_id, QuestionModel.question_type, QuestionModel.text, AnnotationModel.text_answer, AssignationModel.annotate_date, AnnotationModel.user_id).all()
            annotations3 = db.session.query(AnnotationModel,TweetModel,QuestionModel,AssignationModel).join(TweetModel,AnnotationModel.tweet_id==TweetModel.id_unique)\
            .join(QuestionModel,AnnotationModel.question_id == QuestionModel.id).join(AssignationModel, (AnnotationModel.user_id == AssignationModel.user_id) & (AnnotationModel.tweet_id == AssignationModel. tweet_id)).filter(AnnotationModel.question_option_id == -1).with_entities(AnnotationModel.annotation_id, TweetModel.id_unique, TweetModel.text, AnnotationModel.question_id, QuestionModel.question_type, QuestionModel.text, AnnotationModel.text_answer, AssignationModel.annotate_date, AnnotationModel.user_id).all()
        if not annotations:
            return "No annotation to download",200
        annotations_dic = prepare_annotations(annotations,annotations2,annotations3)

        path = os.path.join(current_app.root_path, 'downloads')
        if not os.path.isdir(path):
            os.makedirs(path)
        path = os.path.join(path, 'annotations.csv')
        save_annotations(annotations_dic,path)
        response = "success", 200
        return response
    except Exception as e:
        error = {"exception": str(e), "message": "Exception has occurred. Check the format of the request."}
        response = Response(json.dumps(error), 500, mimetype="application/json")
    return response

@app.route('/api/get_roles', methods=['GET'])
def get_roles():
    try:
        roles = RoleModel.query.all()
        roles_list = [
            {
                "username": role.username,
                "role": role.role,
            } for role in roles]
        response = {'roles':roles_list}
    except Exception as e:
        error = {"exception": str(e), "message": "Exception has occurred. Check the format of the request."}
        response = Response(json.dumps(error), 500)

    return response