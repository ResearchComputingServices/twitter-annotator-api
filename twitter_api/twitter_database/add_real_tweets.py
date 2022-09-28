from configparser import ConfigParser
import psycopg2
import pickle

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# from twitter_api.models.question import QuestionModel
# from twitter_api.models.question_option import QuestionOptionModel

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:admin@127.0.0.1:5432/twitter_data"

db = SQLAlchemy(app)

migrate = Migrate(app, db)




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
        self.time = time
        self.source = source
        self.lang = lang
        self.author_username = author_username
        self.author_name = author_name
        self.author_profile_url = author_profile_url
        self.author_description = author_description
        self.verified_author = verified_author
        self.media_keys = media_keys
        
        
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

def config(filename='database.ini', section='postgresql'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db


def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        #print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        #print('PostgreSQL database version:')
        cur.execute('SELECT version()')

        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        #print(db_version)

        # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            #print('Database connection closed.')

def clear_tables():
    params = config()
    # connect to the PostgreSQL server
    conn = psycopg2.connect(**params)
    # Setting auto commit false
    conn.autocommit = True

    # Creating a cursor object using the cursor() method
    cursor = conn.cursor()

    # Doping EMPLOYEE table if already exists

    
    cursor.execute("DROP TABLE IF EXISTS {};".format("media"))
    cursor.execute("DROP TABLE IF EXISTS {};".format("annotation"))
    cursor.execute("DROP TABLE IF EXISTS {};".format("assignation"))
    cursor.execute("DROP TABLE IF EXISTS {};".format("question"))
    cursor.execute("DROP TABLE IF EXISTS {};".format("question_option"))
    cursor.execute("DROP TABLE IF EXISTS {};".format("question_type"))
    cursor.execute("DROP TABLE IF EXISTS {};".format("tweet"))
    cursor.execute("DROP TABLE IF EXISTS {};".format("role"))
    
    print("Tables dropped... ")

    # Commit your changes in the database
    conn.commit()

    # Closing the connection
    conn.close()
def create_tables():
    
    
    """ create tables in the PostgreSQL database"""
    commands = (
        """ CREATE TABLE tweet (
            id_unique SERIAL PRIMARY KEY,
            tweet_id TEXT,
            original_tweet_id TEXT,
            text TEXT,
            date DATE,
            time TIME,
            source TEXT,
            lang TEXT,
            author_username TEXT,
            author_name TEXT,
            author_profile_url TEXT,
            author_description TEXT,
            verified_author BOOLEAN,
            media_keys TEXT
                )
        """,
        """ CREATE TABLE media (
            id int PRIMARY KEY,
            media_key TEXT,
            type TEXT,
            url TEXT
            )
        """,
        """ CREATE TABLE question (
            id int PRIMARY KEY,
            active boolean,
            question_type int,
            text text,
            question_number int,
            version_number int,
            deleted boolean,
            other boolean
                )
        """,
        """ CREATE TABLE annotation (
                   id int PRIMARY KEY,
                   tweet_id int,
                   user_id text,
                   question_id int,
                   question_option_id int,
                   text_answer text,
                   annotation_id int
                       )
        """,
        """ CREATE TABLE question_type (
                  id int PRIMARY KEY,
                  type text
                      )
        """,
        """ CREATE TABLE question_option (
            id int PRIMARY KEY,
            text text,
            question_id int,
            version_number int
                )
        """,
        """ CREATE TABLE assignation (
                         id SERIAL PRIMARY KEY,
                         user_id text,
                         tweet_id int,
                         answer int,
                         annotate_date text
                             )
        """
    )
    conn = None
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # create table one by one
        for command in commands:
            cur.execute(command)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    print("Table created...")



def serializeObject(object_,file_name):
    file_object = open(file_name,'wb')
    pickle.dump(object_, file_object,protocol = 2)
    file_object.close()
    return
def deserializeObject(file_name):
    file_object = open(file_name,'rb')
    object_ = pickle.load(file_object)
    file_object.close() 
    return object_

def creat_role_table():
    """ create table in the PostgreSQL database"""
    commands = (
        """ CREATE TABLE role (
            username TEXT PRIMARY KEY,
            role TEXT
                )
        """
    )
    conn = None
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # create table one by one
        
        cur.execute(commands)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    print("Table created...")

def add_roles_in_table(dic):
    for username,role in dic.items():
        try:
            params = config()
            # connect to the PostgreSQL server
            conn = psycopg2.connect(**params)
            # Setting auto commit false
            conn.autocommit = True

            # Creating a cursor object using the cursor() method
            cursor = conn.cursor()

            postgres_insert_query = """INSERT INTO role (username, role) VALUES (%s,%s) """
            record_to_insert = (username,role)
            print(record_to_insert)
            cursor.execute(postgres_insert_query, record_to_insert)
            conn.commit()
            # count = cursor.rowcount
            print(username, " inserted successfully into role table")

        except (Exception, psycopg2.Error) as error:
            print("Failed to insert record into mobile freetext_trial_run", error)

        finally:
            # closing database connection.
            if conn:
                cursor.close()
                conn.close()
                print("PostgreSQL connection is closed")

def add_question_type_to_table(dic):
    for id, type in dic.items():
        try:
            params = config()
            # connect to the PostgreSQL server
            conn = psycopg2.connect(**params)
            # Setting auto commit false
            conn.autocommit = True

            # Creating a cursor object using the cursor() method
            cursor = conn.cursor()

            postgres_insert_query = """INSERT INTO question_type (id, type) VALUES (%s,%s) """
            record_to_insert = (id,type)
            print(record_to_insert)
            cursor.execute(postgres_insert_query, record_to_insert)
            conn.commit()
            # count = cursor.rowcount
            print(type, " inserted successfully into question type table")

        except (Exception, psycopg2.Error) as error:
            print("Failed to insert record into mobile freetext_trial_run", error)

        finally:
            # closing database connection.
            if conn:
                cursor.close()
                conn.close()
                print("PostgreSQL connection is closed")

def add_tweet(data_dic):
    
    try:
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        # Setting auto commit false
        conn.autocommit = True

        # Creating a cursor object using the cursor() method
        cursor = conn.cursor()

        postgres_insert_query = """INSERT INTO tweet (tweet_id, original_tweet_id, text, date, time, source,
        lang, author_username, author_name, author_profile_url, author_description, verified_author, 
        media_keys) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) """
        record_to_insert = (data_dic['tweet_id'], data_dic.get('original_tweet_id',''), data_dic['text'], data_dic['date'], 
                            data_dic['time'], data_dic['source'], data_dic['lang'], data_dic['author_username'],
                            data_dic['author_name'], data_dic['author_profile_url'], data_dic['author_description'],
                            data_dic['verified_author'], data_dic.get('media_keys',''))
        #print(record_to_insert)
        cursor.execute(postgres_insert_query, record_to_insert)
        conn.commit()
        # count = cursor.rowcount
        #print(data_dic['tweet_id'], "tweet inserted successfully into tweet table")

    except (Exception, psycopg2.Error) as error:
        print("Failed to insert record into mobile freetext_trial_run", error)

    finally:
        # closing database connection.
        if conn:
            cursor.close()
            conn.close()
            #print("PostgreSQL connection is closed")


def add_data(file_path):
    global all_responses
    global tw
    global row,header
    all_responses = deserializeObject(file_path)
    for tweet in all_responses['data']:
        data_dic = {}
        pass_flag = 0
        
        if tweet['lang'] == 'en':
            data_dic['lang'] = 'en'
            data_dic['tweet_id'] = tweet['id']
            data_dic['text'] = tweet['text']
            

            created_at = tweet['created_at']
            date_list = created_at.split('T')
            date,tim = date_list[0],date_list[1].split('.')[0]
            data_dic['time'] = tim
            data_dic['date'] = date
            data_dic['source'] = tweet['source']
            
            author_id = tweet['author_id']
            for user in all_responses['includes']['users']:
                if user['id'] == author_id:
                    data_dic['author_username'] = user['username']
                    data_dic['author_name'] = user['name']
                    data_dic['author_profile_url'] = user['profile_image_url']
                    data_dic['author_description'] = user['description']
                    data_dic['verified_author'] = user['verified']
                    break
            if 'attachments' in tweet.keys():
                if 'media_keys' in tweet['attachments'].keys():
                    media_keys = ''
                    for media_key in tweet['attachments']['media_keys']:
                        media_keys += (media_key + ',')
                    data_dic['media_keys'] = media_keys[:-1]
            
            if tweet['text'][0:3] == 'RT ':
                if 'referenced_tweets' in tweet.keys():
                    for referenced_tweet in tweet['referenced_tweets']:
                        if referenced_tweet['type'] == 'retweeted':
                            retweet_id = referenced_tweet['id']
                            break
                    for retweeted_tweet in all_responses['includes']['tweets']:
                        if retweeted_tweet['id'] == retweet_id:
                            if retweeted_tweet['lang'] == 'en':
                                data_dic['original_tweet_id'] = retweet_id
                                data_dic['text'] = retweeted_tweet['text']
                            else:
                                pass_flag = 1
                            break
        else:
            pass_flag = 1
        
        
        

        if pass_flag == 0:
            tweet = TweetModel.query.filter_by(tweet_id=data_dic['tweet_id']).first()
            if not tweet:
                original_tweet = data_dic.get('original_tweet_id','')
                if original_tweet:
                    tweet = TweetModel.query.filter_by(original_tweet_id=original_tweet).first()
                    if not tweet:
                        add_tweet(data_dic)
                else:
                    add_tweet(data_dic)
        
 

if __name__ == "__main__":
    date = '2022-01-'
    day = 1
    for day in range(1,3):
        if day < 10:
            date_ = date + '0' + str(day)
        else:
            date_ = date + str(day)
        address = date_ + '/' + date_ + '.p'
        add_data(address)