from flask import request, jsonify, url_for, Blueprint
from flask import json, jsonify, Response, blueprints
from twitter_api.web.common_view import twitter_bp
import twitter_api.web.question_option_view


@twitter_bp.route("/", methods=['GET'])
def hello():
    return "Hello"

