from configparser import ConfigParser
import psycopg2
import csv
import pandas as pd


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
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')

        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print(db_version)

        # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


def create_tables():
    """ create tables in the PostgreSQL database"""
    commands = (
        """
        CREATE TABLE freetext_trial_run (
            id_unique SERIAL PRIMARY KEY,
            mturk_id TEXT,
            tweet_id TEXT,
            tweet TEXT,
            text TEXT,
            answer TEXT,
            id text
        )
        """,
        """ CREATE TABLE likert_trial_run (
            id_unique SERIAL PRIMARY KEY,
            mturk_id TEXT,
            tweet_id TEXT,
            tweet TEXT,
            text TEXT,
            answer TEXT,
            id text
                )
        """,
        """ CREATE TABLE tweet (
            id_unique SERIAL PRIMARY KEY,
            conversation_id TEXT,
            created_at TEXT,
            date TEXT,
            hashtags TEXT,
            id TEXT,
            likes_count text,
            link TEXT,
            location TEXT,
            mentions TEXT,
            name TEXT,
            photos TEXT,
            place text,
            replies_count TEXT,
            retweet TEXT,
            retweets_count TEXT,
            time TEXT,
            Relevance TEXT,
            tweet text,
            urls text,
            user_id text,
            username text,
            video text
                )
        """,
        """ CREATE TABLE question (
            id int PRIMARY KEY,
            active boolean,
            question_type int,
            text text,
            question_number int,
            version_number int,
            deleted boolean
                )
        """,
        """ CREATE TABLE annotation (
                   id int PRIMARY KEY,
                   tweet_id int,
                   user_id int,
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
                         id int PRIMARY KEY,
                         user_id int,
                         tweet_id int,
                         answer int
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

#Deprecated
def create_tables_van():
    """ create tables in the PostgreSQL database"""
    commands = (
        """ CREATE TABLE Toronto_Van_Attach_Twitter (
            id_unique SERIAL PRIMARY KEY,
            conversation_id TEXT,
            created_at TEXT,
            date TEXT,
            hashtags TEXT,
            id TEXT,
            likes_count text,
            link TEXT,
            location TEXT,
            mentions TEXT,
            name TEXT,
            photos TEXT,
            place text,
            replies_count TEXT,
            retweet TEXT,
            retweets_count TEXT,
            time TEXT,
            Relevance TEXT,
            tweet text,
            urls text,
            user_id text,
            username text,
            video text
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

#Deprecated
def create_table_test():
    """ create tables in the PostgreSQL database"""
    commands = (
        """ CREATE TABLE Annotation_table (
            id_unique SERIAL PRIMARY KEY,
            conversation_id TEXT,
            created_at TEXT,
            date TEXT,
            hashtags TEXT,
            id TEXT,
            likes_count text,
            link TEXT,
            location TEXT,
            mentions TEXT,
            name TEXT,
            photos TEXT,
            place text,
            replies_count TEXT,
            retweet TEXT,
            retweets_count TEXT,
            time TEXT,
            Relevance TEXT,
            tweet text,
            urls text,
            user_id text,
            username text,
            video text
                )
        """)
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

#Deprecated
def clear_tables_original():
    params = config()
    # connect to the PostgreSQL server
    conn = psycopg2.connect(**params)
    # Setting auto commit false
    conn.autocommit = True

    # Creating a cursor object using the cursor() method
    cursor = conn.cursor()

    # Doping EMPLOYEE table if already exists
    #cursor.execute("DROP TABLE IF EXISTS {};".format("vendor_parts"))
    #cursor.execute("DROP TABLE IF EXISTS {};".format("part_drawings"))
    #cursor.execute("DROP TABLE IF EXISTS {};".format("likert_trial_run"))
    cursor.execute("DROP TABLE IF EXISTS {};".format("Toronto_Van_Attach_Twitter"))
    #cursor.execute("DROP TABLE IF EXISTS {};".format("Annotation_table"))
    print("Table dropped... ")

    # Commit your changes in the database
    conn.commit()

    # Closing the connection
    conn.close()

def clear_tables():
    params = config()
    # connect to the PostgreSQL server
    conn = psycopg2.connect(**params)
    # Setting auto commit false
    conn.autocommit = True

    # Creating a cursor object using the cursor() method
    cursor = conn.cursor()

    # Doping EMPLOYEE table if already exists


    cursor.execute("DROP TABLE IF EXISTS {};".format("annotation"))
    cursor.execute("DROP TABLE IF EXISTS {};".format("tweet"))
    cursor.execute("DROP TABLE IF EXISTS {};".format("assignation"))
    cursor.execute("DROP TABLE IF EXISTS {};".format("users"))
    cursor.execute("DROP TABLE IF EXISTS {};".format("answer"))
    cursor.execute("DROP TABLE IF EXISTS {};".format("question"))
    cursor.execute("DROP TABLE IF EXISTS {};".format("question_type"))
    cursor.execute("DROP TABLE IF EXISTS {};".format("question_option"))
    cursor.execute("DROP TABLE IF EXISTS {};".format("answer_question_option"))

    cursor.execute("DROP TABLE IF EXISTS {};".format("vendor_parts"))
    cursor.execute("DROP TABLE IF EXISTS {};".format("part_drawings"))
    cursor.execute("DROP TABLE IF EXISTS {};".format("freetext_trial_run"))
    cursor.execute("DROP TABLE IF EXISTS {};".format("likert_trial_run"))
    cursor.execute("DROP TABLE IF EXISTS {};".format("Toronto_Van_Attach_Twitter"))
    cursor.execute("DROP TABLE IF EXISTS {};".format("Annotation_table"))

    print("Tables dropped... ")

    # Commit your changes in the database
    conn.commit()

    # Closing the connection
    conn.close()


def add_data():
    try:
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        # Setting auto commit false
        conn.autocommit = True

        # Creating a cursor object using the cursor() method
        cursor = conn.cursor()

        postgres_insert_query = """ INSERT INTO freetext_trial_run (mturk_id, tweet_id, tweet) VALUES (%s,%s,%s)"""
        record_to_insert = (5, 'One Plus 6', 950)
        cursor.execute(postgres_insert_query, record_to_insert)

        conn.commit()
        count = cursor.rowcount
        print(count, "Record inserted successfully into mobile table")

    except (Exception, psycopg2.Error) as error:
        print("Failed to insert record into mobile table", error)

    finally:
        # closing database connection.
        if conn:
            cursor.close()
            conn.close()
            print("PostgreSQL connection is closed")


def add_data_freetext_trial_run(mturk_id, tweet_id, tweet, text, answer, id):
    try:
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        # Setting auto commit false
        conn.autocommit = True

        # Creating a cursor object using the cursor() method
        cursor = conn.cursor()

        postgres_insert_query = """INSERT INTO freetext_trial_run (mturk_id, tweet_id, tweet, text, answer, 
        id) VALUES (%s,%s,%s,%s,%s,%s) """
        record_to_insert = (mturk_id, tweet_id, tweet, text, answer, id)
        cursor.execute(postgres_insert_query, record_to_insert)

        conn.commit()
        # count = cursor.rowcount
        print(mturk_id, "tweet inserted successfully into freetext_trial_run table")

    except (Exception, psycopg2.Error) as error:
        print("Failed to insert record into mobile freetext_trial_run", error)

    finally:
        # closing database connection.
        if conn:
            cursor.close()
            conn.close()
            print("PostgreSQL connection is closed")


def add_data_likert_trial_run(mturk_id, tweet_id, tweet, text, answer, id):
    try:
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        # Setting auto commit false
        conn.autocommit = True

        # Creating a cursor object using the cursor() method
        cursor = conn.cursor()

        postgres_insert_query = """INSERT INTO likert_trial_run (mturk_id, tweet_id, tweet, text, answer, 
        id) VALUES (%s,%s,%s,%s,%s,%s) """
        record_to_insert = (mturk_id, tweet_id, tweet, text, answer, id)
        cursor.execute(postgres_insert_query, record_to_insert)

        conn.commit()
        # count = cursor.rowcount
        print(mturk_id, "tweet inserted successfully into likert_trial_run table")

    except (Exception, psycopg2.Error) as error:
        print("Failed to insert record into mobile freetext_trial_run", error)

    finally:
        # closing database connection.
        if conn:
            cursor.close()
            conn.close()
            print("PostgreSQL connection is closed")


def add_data_Toronto_Van_Attach_Twitter(conversation_id, created_at, date, hashtags, id, likes_count, link,
                                        location, mentions, name, photos, place, replies_count, retweet,
                                        retweets_count, time, relevance, tweet, urls, user_id, username, video):
    try:
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        # Setting auto commit false
        conn.autocommit = True

        # Creating a cursor object using the cursor() method
        cursor = conn.cursor()

        postgres_insert_query = """INSERT INTO tweet (conversation_id, created_at, date, 
        hashtags, id, likes_count, link, location, mentions, name, photos, place, replies_count, retweet, 
        retweets_count, time, Relevance, tweet, urls, user_id, username, video) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,
        %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) """
        record_to_insert = (conversation_id, created_at, date, hashtags, id, likes_count, link,
                            location, mentions, name, photos, place, replies_count, retweet,
                            retweets_count, time, relevance, tweet, urls, user_id, username, video)

        cursor.execute(postgres_insert_query, record_to_insert)
        print("here")
        conn.commit()
        # count = cursor.rowcount
        print(conversation_id, "tweet inserted successfully into tweet table")

    except (Exception, psycopg2.Error) as error:
        print("Failed to insert record into mobile freetext_trial_run", error)

    finally:
        # closing database connection.
        if conn:
            cursor.close()
            conn.close()
            print("PostgreSQL connection is closed")


def read_data_freetext_trial_run():
    with open('freetext-trial-run.csv', newline='', encoding="utf8") as csvfile:
        data = pd.read_csv(csvfile)
        for _, row in data.iterrows():
            d = dict(row)
            mturk_id = d["mturk_id"]
            tweet_id = d["tweet_id"]
            tweet = d["tweet"]
            text = d["text"]
            answer = d["answer"]
            id = d["id"]
            add_data_freetext_trial_run(mturk_id, tweet_id, tweet, text, answer, id)


def read_data_likert_trial_run():
    with open('likert-trial-run.csv', newline='', encoding="utf8") as csvfile:
        data = pd.read_csv(csvfile)
        for _, row in data.iterrows():
            d = dict(row)
            mturk_id = d["mturk_id"]
            tweet_id = d["tweet_id"]
            tweet = d["tweet"]
            text = d["text"]
            answer = d["answer"]
            id = d["id"]
            add_data_likert_trial_run(mturk_id, tweet_id, tweet, text, answer, id)


def read_data_Toronto_Van_Attach_Twitter_1_15000():
    with open('Toronto_Van_Attach_Twitter.csv', newline='') as csvfile:
        data = pd.read_csv(csvfile, nrows=15000)
        for _, row in data.iterrows():
            d = dict(row)
            conversation_id = d["conversation_id"]
            created_at = d["created_at"]
            date = d["date"]
            hashtags = d["hashtags"]
            id = d["id"]
            likes_count = "" if str(d["likes_count"]) == ("nan" or "NaN") else int(d["likes_count"])
            link = d["link"]
            location = d["location"]
            mentions = d["mentions"]
            name = d["name"]
            photos = d["photos"]
            place = d["place"]
            replies_count = "" if str(d["replies_count"]) == ("nan" or "NaN") else int(d["replies_count"])
            retweet = d["retweet"]
            retweets_count = "" if str(d["retweets_count"]) == ("nan" or "NaN") else int(d["retweets_count"])
            time = d["time"]
            Relevance = "" if str(d["Relevance"]) == ("nan" or "NaN") else int(d["Relevance"])
            tweet = d["tweet"]
            urls = d["urls"]
            user_id = d["user_id"]
            username = d["username"]
            video = "" if str(d["video"]) == ("nan" or "NaN") else int(d["video"])
            # print(type(conversation_id))
            add_data_Toronto_Van_Attach_Twitter(conversation_id, created_at, date, hashtags, id, likes_count, link,
                                                location, mentions, name, photos, place, replies_count, retweet,
                                                retweets_count, time, Relevance, tweet, urls, user_id, username, video)

def read_data_Toronto_Van_Attach_Twitter_15001_30000():
    with open('Toronto_Van_Attach_Twitter.csv', newline='') as csvfile:
        data = pd.read_csv(csvfile, skiprows=(1, 15000), nrows=15000)
        for _, row in data.iterrows():
            d = dict(row)
            conversation_id = d["conversation_id"]
            created_at = d["created_at"]
            date = d["date"]
            hashtags = d["hashtags"]
            id = d["id"]
            likes_count = "" if str(d["likes_count"]) == ("nan" or "NaN") else int(d["likes_count"])
            link = d["link"]
            location = d["location"]
            mentions = d["mentions"]
            name = d["name"]
            photos = d["photos"]
            place = d["place"]
            replies_count = "" if str(d["replies_count"]) == ("nan" or "NaN") else int(d["replies_count"])
            retweet = d["retweet"]
            retweets_count = "" if str(d["retweets_count"]) == ("nan" or "NaN") else int(d["retweets_count"])
            time = d["time"]
            Relevance = "" if str(d["Relevance"]) == ("nan" or "NaN") else int(d["Relevance"])
            tweet = d["tweet"]
            urls = d["urls"]
            user_id = d["user_id"]
            username = d["username"]
            video = "" if str(d["video"]) == ("nan" or "NaN") else int(d["video"])
            # print(type(conversation_id))
            add_data_Toronto_Van_Attach_Twitter(conversation_id, created_at, date, hashtags, id, likes_count, link,
                                                location, mentions, name, photos, place, replies_count, retweet,
                                                retweets_count, time, Relevance, tweet, urls, user_id, username, video)

def read_data_Toronto_Van_Attach_Twitter_30001_45000():
    with open('Toronto_Van_Attach_Twitter.csv', newline='') as csvfile:
        data = pd.read_csv(csvfile, skiprows=(1, 30000), nrows=15000)
        for _, row in data.iterrows():
            d = dict(row)
            conversation_id = d["conversation_id"]
            created_at = d["created_at"]
            date = d["date"]
            hashtags = d["hashtags"]
            id = d["id"]
            likes_count = "" if str(d["likes_count"]) == ("nan" or "NaN") else int(d["likes_count"])
            link = d["link"]
            location = d["location"]
            mentions = d["mentions"]
            name = d["name"]
            photos = d["photos"]
            place = d["place"]
            replies_count = "" if str(d["replies_count"]) == ("nan" or "NaN") else int(d["replies_count"])
            retweet = d["retweet"]
            retweets_count = "" if str(d["retweets_count"]) == ("nan" or "NaN") else int(d["retweets_count"])
            time = d["time"]
            Relevance = "" if str(d["Relevance"]) == ("nan" or "NaN") else int(d["Relevance"])
            tweet = d["tweet"]
            urls = d["urls"]
            user_id = d["user_id"]
            username = d["username"]
            video = "" if str(d["video"]) == ("nan" or "NaN") else int(d["video"])
            # print(type(conversation_id))
            add_data_Toronto_Van_Attach_Twitter(conversation_id, created_at, date, hashtags, id, likes_count, link,
                                                location, mentions, name, photos, place, replies_count, retweet,
                                                retweets_count, time, Relevance, tweet, urls, user_id, username, video)

def read_data_Toronto_Van_Attach_Twitter_45001_60000():
    with open('Toronto_Van_Attach_Twitter.csv', newline='') as csvfile:
        data = pd.read_csv(csvfile, skiprows=(1, 45000), nrows=15000)
        for _, row in data.iterrows():
            d = dict(row)
            conversation_id = d["conversation_id"]
            created_at = d["created_at"]
            date = d["date"]
            hashtags = d["hashtags"]
            id = d["id"]
            likes_count = "" if str(d["likes_count"]) == ("nan" or "NaN") else int(d["likes_count"])
            link = d["link"]
            location = d["location"]
            mentions = d["mentions"]
            name = d["name"]
            photos = d["photos"]
            place = d["place"]
            replies_count = "" if str(d["replies_count"]) == ("nan" or "NaN") else int(d["replies_count"])
            retweet = d["retweet"]
            retweets_count = "" if str(d["retweets_count"]) == ("nan" or "NaN") else int(d["retweets_count"])
            time = d["time"]
            Relevance = "" if str(d["Relevance"]) == ("nan" or "NaN") else int(d["Relevance"])
            tweet = d["tweet"]
            urls = d["urls"]
            user_id = d["user_id"]
            username = d["username"]
            video = "" if str(d["video"]) == ("nan" or "NaN") else int(d["video"])
            # print(type(conversation_id))
            add_data_Toronto_Van_Attach_Twitter(conversation_id, created_at, date, hashtags, id, likes_count, link,
                                                location, mentions, name, photos, place, replies_count, retweet,
                                                retweets_count, time, Relevance, tweet, urls, user_id, username, video)




if __name__ == '__main__':
    #connect()
    clear_tables()
    create_tables()

    #create_table_test()
    #create_tables_van()
    # add_data()
    #read_data_freetext_trial_run()
    #read_data_likert_trial_run()
    read_data_Toronto_Van_Attach_Twitter_1_15000()
    read_data_Toronto_Van_Attach_Twitter_15001_30000()
    read_data_Toronto_Van_Attach_Twitter_30001_45000()
    read_data_Toronto_Van_Attach_Twitter_45001_60000()


