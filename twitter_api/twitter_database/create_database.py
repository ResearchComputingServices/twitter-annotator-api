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
        CREATE TABLE tweet (
            id int PRIMARY KEY
        )
        """,
        """ CREATE TABLE users (
            id int PRIMARY KEY
                )
        """,
        """ CREATE TABLE answer (
            id int PRIMARY KEY,
            question_id int,
            text_answer text,
            answer int
                )
        """,
        """ CREATE TABLE question (
            id int PRIMARY KEY,
            active boolean,
            question_type int,
            text text
                )
        """,
        """ CREATE TABLE annotation (
            id int PRIMARY KEY,
            tweet_id int,
            user_id int,
            question_id int,
            answer_id int,
            FOREIGN KEY (tweet_id) REFERENCES tweet (id),
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (answer_id) REFERENCES answer (id),
            FOREIGN KEY (question_id) REFERENCES question (id)
                )
        """,

        """ CREATE TABLE question_type (
            id int PRIMARY KEY,
            type text
                )
        """,
        """ CREATE TABLE answer_question_option (
            answer_id int PRIMARY KEY,
            question_option_id int
                )
        """,
        """ CREATE TABLE question_option (
            id int PRIMARY KEY,
            text text,
            question_id int
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

def create_tables_tweet():
    """ create tables in the PostgreSQL database"""
    commands = (
        """
        CREATE TABLE tweet (
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
        """ CREATE TABLE annotation (
            id int PRIMARY KEY,
            tweet_id int,
            user_id int,
            question_id int,
            answer_id int
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
    '''
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
    '''
    print("Table dropped... ")

    # Commit your changes in the database
    conn.commit()

    # Closing the connection
    conn.close()


if __name__ == '__main__':
    #connect()
    clear_tables()
    create_tables()
    create_tables_tweet()


