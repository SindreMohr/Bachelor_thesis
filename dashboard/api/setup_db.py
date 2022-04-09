import imp
import sqlite3
from datetime import date, timedelta
from sqlite3 import Error
from time import pthread_getcpuclockid
# Most of this stuff is re-used from lectures

#hack for sd
import pandas as pd
from sklearn.model_selection import train_test_split
from zmq import NULL

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
sql_create_models_table = """CREATE TABLE IF NOT EXISTS models(
     mid INTEGER PRIMARY KEY AUTOINCREMENT,
     mtype TEXT NOT NULL,
     lag INTEGER ,
     batches INTEGER,
     epochs INTEGER,
     train_test_split REAL
);"""

 #layer_depth INTEGER,
 #    layers INTEGER,
 # these are derivable from a saved modell

#remember to clean fs of model as well on delete
sql_create_projects_table = """ CREATE TABLE IF NOT EXISTS projects
    pid INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT
    mid INTEGER,

    FOREIGN KEY (mid) references models (mid) ON DELETE CASCADE
    );"""

sql_create_project_houses_table = """ CREATE TABLE IF NOT EXISTS project_houses
    pid INTEGER,
    lclid TEXT,

    PRIMARY KEY (pid,lclid)
    FOREIGN KEY (pid) references projects (pid) ON DELETE CASCADE
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

def drop_table(conn, table_name):
    try:
        c = conn.cursor()
        c.execute("DROP TABLE ?",(table_name,))
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
def add_project_db(conn):

    #no params kinda odd
    sql = ''' INSERT INTO projects()
              VALUES() '''
    try:
        cur = conn.cursor()
        cur.execute(sql, ())
        conn.commit()
        return True
    except Error as e:
        print(e)
        return False

def add_model_db(conn, mtype, lag, batches, epochs, train_test_split):
    sql = ''' INSERT INTO models(mtype,lag,batches,epochs,train_test_split)
              VALUES(?,?,?,?,?) '''
    try:
        cur = conn.cursor()
        cur.execute(sql, (mtype, lag, batches,epochs,train_test_split))
        conn.commit()
        return True
    except Error as e:
        print(e)
        return False

##### INITS #####

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

#### UPDATE #####

def update_project(conn,pid,mid):
    try:
        cur = conn.cursor()
        cur.execute("UPDATE projects SET mid=? WHERE pid = ?",(mid, pid))
        conn.commit()
    except Error as e:
        print(e)

def update_model(conn, mid,mtype,lag,batches,epochs,train_test_split):
    try:
        cur = conn.cursor()
        cur.execute("UPDATE projects SET mtype=?, lag=?, batches=?, epochs=?, train_test_split=? WHERE mid = ?",(mtype, lag, batches, epochs, train_test_split, mid))
        conn.commit()
    except Error as e:
        print(e)
#### DELETE #####

def delete_project(conn,pid):
    try:
        cur = conn.cursor()
        
        #deleting model should cascade delete project, but i dont think the opposite applies 
        cur.execute("SELECT mid FROM projects WHERE pid = ?",(pid,))
        for (mid) in cur:
            if mid is not None:
                delete_model(mid)
            else:
                cur.execute("DELETE FROM projects WHERE pid = ?",(pid,))
                conn.commit()
    except Error as e:
        print(e)

def delete_model(conn,mid):
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM models WHERE mid = ?",(mid,))
        conn.commit()
    except Error as e:
        print(e)

##### SELECTS #####

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

    # Frequency of data, these two queries should return the same result
    cur.execute(f"SELECT COUNT(tstp) FROM dataset WHERE lclid='{lclid}'") 
    result['count_tstp'] = cur.fetchone()
    cur.execute(f"SELECT COUNT(energy) FROM dataset WHERE lclid='{lclid}'")
    result['count_energy'] = cur.fetchone()

    #data average/mean
    # is time mean/sd necessary? at least in this format
    cur.execute(f"SELECT AVG(energy) FROM dataset WHERE lclid='{lclid}'")
    result['avg_energy'] = cur.fetchone()
    cur.execute(f"SELECT AVG(tstp) FROM dataset WHERE lclid='{lclid}'")
    result['avg_tstp'] = cur.fetchone()
    
    #energy sd
    #consider making less queries and let pandas do the work
    query = (f"SELECT energy FROM dataset WHERE lclid='{lclid}'")
    df = pd.read_sql(query,conn)
    sd = df["energy"].std()
    result['std_energy'] = sd



    #energy min max
    cur.execute(f"SELECT MIN(energy) FROM dataset WHERE lclid='{lclid}'")
    result['min_energy'] = cur.fetchone()
    cur.execute(f"SELECT  MAX(energy) FROM dataset WHERE lclid='{lclid}'")
    result['max_energy'] = cur.fetchone()
    
    
     

    #timestamp min max sd
    cur.execute(f"SELECT AVG(tstp) FROM dataset WHERE lclid='{lclid}'")
    result['std_tstp'] = cur.fetchone()
    cur.execute(f"SELECT MIN(tstp) FROM dataset WHERE lclid='{lclid}'")
    result['min_tstp'] = cur.fetchone()
    cur.execute(f"SELECT MAX(tstp) FROM dataset WHERE lclid='{lclid}'")
    result['max_tstp'] = cur.fetchone()

    #Getting dataset head
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

def select_projects(conn):
    cur = conn.cursor()
    cur.execute(f"SELECT pid FROM projects") 
    result = {}
    projects = []
    for row in cur:
        projects.append(row)
    result['projects'] = projects
    return result

def select_project(conn,pid):
    cur = conn.cursor()
    cur.execute("SELECT * FROM projects WHERE pid = ?",(pid,))
    res = {}
    project = {}
    
    for (pid,name,mid) in cur:
       project["id"] = pid
       project["name"] = name
       project["mid"] = mid
    
    print(project["mid"])
    if project["mid"] is not None:
        cur.execute("SELECT * FROM models WHERE mid = ?",(project["mid"],))
        for (mid,mtype,lag,batches,epochs,train_test_split) in cur:
            project["mtype"] = mtype
            project["lag"] = lag
            project["mid"] = mid
            project["batches"] = batches
            project["epochs"] = epochs
            project["train_test_split"] = train_test_split
    cur.execute("SELECT lclid FROM project_houses WHERE pid = ?",(pid,))
    house_list = []
    for (lclid) in cur:
        house_list.append(lclid)
    project["houses"] = house_list
    return project


#### SETUP ####

def setup():
    conn = create_connection(database)
    if conn is not None:
        #create_table(conn, sql_create_house_table)
        #create_table(conn, sql_create_dataset_table)
        #init_database(conn)
        #init_house_info(conn)

        create_table(conn, sql_create_models_table)
        create_table(conn, sql_create_projects_table)
        create_table(conn, sql_create_project_houses_table)



        conn.close()

if __name__ == '__main__':
    setup()