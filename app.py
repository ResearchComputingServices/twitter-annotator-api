import os
#from flask_cors import CORS
#from api import app
from twitter_api.web.question_option_view import app
from flask_sqlalchemy import SQLAlchemy

#CORS(app)

#from twitter_api.web.views import *
#from twitter_api import twitter_factory


if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)