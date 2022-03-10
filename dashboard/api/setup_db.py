import sqlite3
from datetime import date, timedelta
from sqlite3 import Error
# Most of this stuff is re-used from lectures

database = "./database.db"

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn

##### CREATE TABLES ######## 
sql_create_dataset_table = """CREATE TABLE IF NOT EXISTS dataset (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                lclid TEXT NOT NULL,
                                tstp TEXT NOT NULL,
                                energy REAL NOT NULL
                            );"""
# FOREIGN KEY (lclid) REFERENCES houses (lclid)

sql_create_house_table = """ CREATE TABLE IF NOT EXISTS houses
    lclid TEXT PRIMARY KEY,
    acorn_class TEXT NOT NULL,
    affluency TEXT NOT NULL,
    start_date TEXT NOT NULL,
    stop_date TEXT NOT NULL
    );"""


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

#### INSERT #########
def add_data_db(conn, lclid, tstp, energy):
    """
    Add a new user into the users table
    :param conn:
    :param lclid:
    :param tstp:
    :param energy:
    """
    sql = ''' INSERT INTO dataset(lclid,tstp,energy)
              VALUES(?,?,?) '''
    try:
        cur = conn.cursor()
        cur.execute(sql, (lclid, tstp, energy))
        conn.commit()
        return True
    except Error as e:
        print(e)
        return False

def init_database(conn):
    with open("ouput.csv", "r") as rf:
        for line in rf:
            line = line.split(",")
            lclid = line[0]
            tstp = line[1]
            energy = line[2]
            add_data_db(conn, lclid, tstp, energy)


def select_interactions_db(conn, post_id):
    cur = conn.cursor()
    cur.execute(f"SELECT id, comment, username FROM interactions WHERE post_id={post_id} and interaction_type='comment'") 

def select_housedata_db(conn, lclid):
    cur = conn.cursor()
    cur.execute(f"SELECT lclid, tstp, energy FROM dataset WHERE lclid={lclid}") 
    result = []
    for row in cur:
        content = {}
        id, time, val = row
        content["id"] = id
        content["time"] = time
        content["val"] = val
        result.append(content)
    return result

#### SETUP ####

def setup():
    conn = create_connection(database)
    if conn is not None:
        #create_table(conn, sql_create_house_table)
        create_table(conn, sql_create_dataset_table)
        init_database(conn)
        conn.close()

if __name__ == '__main__':
    setup()