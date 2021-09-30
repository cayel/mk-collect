import sqlite3
from typing import Any
import config
import pandas as pd

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn

def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        Error : Any
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def drop_table(conn, drop_table_sql):
    """ drop a table from the drop_table_sql statement
    :param conn: Connection object
    :param drop_table_sql: a DROP TABLE statement
    :return:
    """   
    try:
        Error : Any
        c = conn.cursor()
        c.execute(drop_table_sql)
    except Error as e:
        print(e)    

played = pd.read_excel('data/spotify_recently_played.xlsx', sheet_name='Feuille 1', header=None)
played.drop(played.columns[4], axis=1, inplace=True)
played.columns =['playedDate', 'title', 'artist', 'spotifyId']

sql_create_played_table = """ CREATE TABLE IF NOT EXISTS played (
                                            playedId integer PRIMARY KEY,
                                            title text NOT NULL,
                                            artist text,
                                            spotifyId text,
                                            playedDate date
                                        ); """    
    
sql_drop_played_table = """ DROP TABLE played """    

# create a database connection
conn = create_connection(config.db_file)
# drop tables
if conn is not None:
    # drop played table
    drop_table(conn, sql_drop_played_table)
else:
    print("Error! cannot create the database connection.")

# create tables
if conn is not None:
    # create projects table
    create_table(conn, sql_create_played_table)
else:
    print("Error! cannot create the database connection.")

# populate database
played.to_sql('played', conn, if_exists='append', index=False)

# load database
played =  pd.read_sql('SELECT * FROM played', conn)

print("Played : ", len(played.index))
