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

#not entirely sure all fields of this maybe split into tables for each modeltype instead of single one with potentially unused fields
sql_create_model_info_table = """CREATE TABLE IF NOT EXISTS model_info(
     mid INTEGER PRIMARY KEY AUTOINCREMENT,
     mtype TEXT NOT NULL,
     lag INTEGER,
     layer_depth INTEGER,
     batches INTEGER,
     epochs INTEGER,
     train_test_split REAL
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


def add_house_info_db(conn, lclid, acorn, affluency):
    sql = ''' INSERT INTO houses(lclid,acorn_class,affluency)
              VALUES(?,?,?) '''
    try:
        cur = conn.cursor()
        cur.execute(sql, (lclid, acorn, affluency))
        conn.commit()
        return True
    except Error as e:
        print(e)
        return False

def init_database(conn):
    with open("ouput.csv", "r") as rf:
        rf.readline()
        for line in rf:
            line = line.split(",")
            lclid = line[0]
            tstp = line[1]
            energy = line[2]
            add_data_db(conn, lclid, tstp, energy)

def init_house_info(conn):
     with open("informations_households.csv", "r") as rf:
        rf.readline()
        for line in rf:
            line = line.split(",")
            lclid = line[0]
            acorn = line[2]
            affluency = line[3]
            print(f"lclid: {lclid}, acorn: {acorn}, affluiency: {affluency} ")
            #idk where get rest info perse only 10 houses so far could hardcode.
            add_house_info_db(conn, lclid, acorn, affluency)


def select_interactions_db(conn, post_id):
    cur = conn.cursor()
    cur.execute(f"SELECT id, comment, username FROM interactions WHERE post_id={post_id} and interaction_type='comment'") 

def select_housedata_curve_db(conn, lclid):
    cur = conn.cursor()
    cur.execute(f"SELECT tstp, energy FROM dataset WHERE lclid='{lclid}' ORDER BY id ASC") 
    result = {}
    time = []
    values = []
    for row in cur:
        tstp, val = row
        time.append(tstp)
        values.append(val)
    result['time'] = time
    result['values'] = values
    return result

def select_housedata_count_db(conn, lclid):
    cur = conn.cursor()
    result = {}
    cur.execute(f"SELECT COUNT(tstp) FROM dataset WHERE lclid='{lclid}'") 
    result['count_tstp'] = cur.fetchone()
    cur.execute(f"SELECT COUNT(energy) FROM dataset WHERE lclid='{lclid}'")
    result['count_energy'] = cur.fetchone()

    cur.execute(f"SELECT AVG(energy) FROM dataset WHERE lclid='{lclid}'")
    result['avg_energy'] = cur.fetchone()
    cur.execute(f"SELECT AVG(tstp) FROM dataset WHERE lclid='{lclid}'")
    result['avg_tstp'] = cur.fetchone()

    cur.execute(f"SELECT AVG(energy) FROM dataset WHERE lclid='{lclid}'")
    result['std_energy'] = cur.fetchone()
    cur.execute(f"SELECT MIN(energy) FROM dataset WHERE lclid='{lclid}'")
    result['min_energy'] = cur.fetchone()
    cur.execute(f"SELECT MAX(energy) FROM dataset WHERE lclid='{lclid}'")
    result['max_energy'] = cur.fetchone()

    cur.execute(f"SELECT AVG(tstp) FROM dataset WHERE lclid='{lclid}'")
    result['std_tstp'] = cur.fetchone()
    cur.execute(f"SELECT MIN(tstp) FROM dataset WHERE lclid='{lclid}'")
    result['min_tstp'] = cur.fetchone()
    cur.execute(f"SELECT MAX(tstp) FROM dataset WHERE lclid='{lclid}'")
    result['max_tstp'] = cur.fetchone()
    cur.execute(f"SELECT * FROM dataset WHERE lclid='{lclid}' LIMIT 10")
    id = []
    lcl = []
    tstp = []
    energy = []
    for row in cur:
        i, l, t, e = row
        id.append(i)
        lcl.append(l)
        tstp.append(t)
        energy.append(e)
    head = {}
    head['id'] = id
    head['lclid'] = lcl
    head['tstp'] = tstp
    head['energy'] = energy
    result['head'] = head
    print("THIS IS RESULTS")
    print(result)
    return result

def select_lclids(conn):
    cur = conn.cursor()
    cur.execute(f"SELECT DISTINCT lclid FROM dataset ORDER BY lclid") 
    result = {}
    lclid = []
    for row in cur:
        lclid.append(row)
    result['lclid'] = lclid
    return result

#### SETUP ####

def setup():
    conn = create_connection(database)
    if conn is not None:
        #create_table(conn, sql_create_house_table)
        #create_table(conn, sql_create_dataset_table)
        #init_database(conn)
        init_house_info(conn)
        conn.close()

if __name__ == '__main__':
    setup()