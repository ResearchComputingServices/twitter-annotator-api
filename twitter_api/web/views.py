from flask import request, jsonify, url_for, Blueprint
from flask import json, jsonify, Response, blueprints
from twitter_api.web.common_view import twitter_bp
from onlinedatabase_api.decorators.crossorigin import crossdomain
import twitter_api.web.question_option_view


@twitter_bp.route("/", methods=['GET'])
@crossdomain(origin='*')
def hello():
    return "Hello"

