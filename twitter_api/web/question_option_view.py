import time
from flask import Flask
from flask import request, send_file
from flask import json, jsonify, Response, blueprints
from configparser import ConfigParser
from flask_cors import cross_origin
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
#from twitter_api.models.question import QuestionModel
#from twitter_api.models.question_option import QuestionOptionModel
from twitter_api.models.tweet import TweetModel
from twitter_api.twitter_database.config_database import config
import psycopg2
from twitter_api.web.common_view import twitter_bp
from onlinedatabase_api.decorators.crossorigin import crossdomain

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

    def __init__(self, active, question_type, text, question_number, version_number, deleted):
        self.active = active
        self.question_type = question_type
        self.text = text
        self.question_number = question_number
        self.version_number = version_number
        self.deleted = deleted

    def __init__(self, item):
        # BaseModel.__init__(self, item)
        self.id = item.get('id')
        self.active = item.get('active')
        self.question_type = item.get('question_type')
        self.text = item.get('text')
        self.question_number = item.get('question_number')
        self.version_number = item.get('version_number')
        self.deleted = item.get('deleted')

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

@app.route('/api/highlight', methods=['POST'])
def highlight():
    try:
        data = request.get_json()
        # add data to database
        print(data)
        response = jsonify(data)

    except Exception as e:
        error = {"exception": str(e), "message": "Exception has occurred. Check the format of the request."}
        response = Response(json.dumps(error), 500, mimetype="application/json")

    return response



@app.route('/api/get_question_option', methods=['GET'])
def get_question_option():
    try:
        #print('get_question_option')
        questions = QuestionModel.query.all()
        questions = QuestionModel.query.filter_by(deleted=False).all()
        print(questions)
        Question_results = [
            {
                "id": question.id,
                "active": question.active,
                "question_type": question.question_type,
                "text": question.text,
                "question_number": question.question_number

            } for question in questions]
        #print(Question_results)
        Question_id_unsort = []
        for Question_result in Question_results:
            Question_id_unsort.append(Question_result.get("question_number"))

        Question_id_sorted = sorted(Question_id_unsort)
        Question_results_sorted = []
        for i in range(len(Question_id_sorted)):
            for Question_result in Question_results:
                if Question_result.get("question_number") == Question_id_sorted[i] and Question_result.get("active") == True:

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
        # tweets = TweetModel.query.all()
        tweet = TweetModel.query.filter_by(id_unique=2).first()
        full_link = tweet.link
        id_for_tweet = full_link.split("/")
        response = jsonify(id_for_tweet[-1])
    except Exception as e:
        error = {"exception": str(e), "message": "Exception has occurred. Check the format of the request."}
        response = Response(json.dumps(error), 500, mimetype="application/json")
    return response


@app.route('/api/get_all_question_option', methods=['GET'])

def get_all_question_option():
    try:
        #print('get_all_question_option')
        questions = QuestionModel.query.all()
        questions = QuestionModel.query.filter_by(deleted=False).all()
        Question_results = [
            {
                "id": question.id,
                "active": question.active,
                "question_type": question.question_type,
                "text": question.text,
                "deleted": question.deleted,
                "question_number": question.question_number
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
        #print("success")
        response = {"questions": Question_results_sorted, "options": Question_option_results_sorted}
    except Exception as e:
        error = {"exception": str(e), "message": "Exception has occurred. Check the format of the request."}
        response = Response(json.dumps(error), 500, mimetype="application/json")
    return response


@app.route('/api/get_single_question_option', methods=['GET'])
def get_single_question_option():
    try:
        print('get_single_question_option')
        specific_id = request.args.get('id')

        single_question = QuestionModel.query.filter_by(id=specific_id).first()
        single_specific_question = {
            "id": single_question.id,
            "active": single_question.active,
            "question_type": single_question.question_type,
            "text": single_question.text
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
        print("update here")
        print(data)
        print(data.get('id'))
        # question = QuestionModel.query.filter_by(id=data.get('id')).first()
        question = QuestionModel.query.filter_by(id=data.get('id')).first()
        print(question)
        print(question.question_number)
        print(question.version_number)
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


        print("reate_single_question_option")
        data = request.get_json()
        print(data)
        questions = QuestionModel.query.all()
        max_id = 0
        for s_question in questions:
            if s_question.id > max_id:
                max_id = s_question.id

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

        question_data["id"] = int(max_id + 1)
        question_data["active"] = question_active
        question_data["question_type"] = int_question_type
        question_data["text"] = data["text"]


        question_data["question_number"] = question.question_number
        question_data["version_number"] = question.version_number+1
        question_data["deleted"] = False

        questions_to_add = QuestionModel(question_data)
        db.session.add(questions_to_add)
        db.session.commit()

        question_options = QuestionOptionModel.query.all()
        print("start")
        print(question_options)
        for question_option in question_options:
            print(question_option.question_id)
            if question_option.question_id == data.get('id'):
                db.session.delete(question_option)
                db.session.commit()
        if int_question_type == 0 or int_question_type == 1:
            print("only if radio and checkbox")
            for option in data["options"]:

                max_option_id = 0
                question_options = QuestionOptionModel.query.all()
                for option_id in question_options:
                    if option_id.id > max_option_id:
                        max_option_id = option_id.id

                option_data_to_add = {}
                print("here", max_option_id)

                option_data_to_add["id"] = max_option_id + 1
                option_data_to_add["text"] = option

                option_data_to_add["question_id"] = int(max_id + 1)
                option_data_to_add["version_number"] = question.version_number+1
                #option_data_to_add["active"] = question_active
                option_to_add = QuestionOptionModel(option_data_to_add)
                db.session.add(option_to_add)
                db.session.commit()

        print("success")
        response = "success", 200

    except Exception as e:
        error = {"exception": str(e), "message": "Exception has occurred. Check the format of the request."}
        response = Response(json.dumps(error), 500)

    return response


@app.route('/api/update_single_question_option_active_only', methods=['PUT'])
def update_single_question_option_active_only():
    try:
        data = request.get_json()
        print("update active status")
        print(data)
        print(data.get('id'))
        question = QuestionModel.query.filter_by(id=data.get('id')).first()
        print(question)
        question.active = data.get('active')
        db.session.commit()

        print("success")
        response = "success", 200

    except Exception as e:
        error = {"exception": str(e), "message": "Exception has occurred. Check the format of the request."}
        response = Response(json.dumps(error), 500)

    return response


@app.route('/api/delete_single_question_option', methods=['DELETE'])
def delete_single_question_option():
    try:
        data = request.get_json()
        print("**update active status")
        print(data)
        print(data.get('id'))
        question = QuestionModel.query.filter_by(id=data.get('id')).first()
        print(question)
        question.active = False
        question.deleted = True
        #data = request.get_json()
        print('delete_single_question_option')
        specific_id = data["id"]
        corresponding_options = data["options"]

        #single_question_to_delete = QuestionModel.query.filter_by(id=specific_id).first()

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
                print(single_option_to_delete)
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
        print("reate_single_question_option")
        data = request.get_json()
        print(data)
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

        question_data["id"] = int(max_id + 1)
        question_data["active"] = question_active
        question_data["question_type"] = int_question_type
        question_data["text"] = data["text"]

        max_question_number = 0
        for question in questions:

            if question.question_number > max_question_number:
                max_question_number = question.question_number

        question_data["question_number"] = max_question_number+1
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
