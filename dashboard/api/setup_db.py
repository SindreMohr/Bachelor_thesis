import os
from pickle import FALSE
import shutil
import sqlite3
from datetime import date, datetime, timedelta
from sqlite3 import Error
# Most of this stuff is re-used from lectures

from datetime import datetime as dt
#hack for sd
import pandas as pd

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

sql_create_models_table = """CREATE TABLE IF NOT EXISTS models(
     mid INTEGER PRIMARY KEY AUTOINCREMENT,
     mtype TEXT NOT NULL,
     lag INTEGER ,
     batches INTEGER,
     epochs INTEGER,
     train_test_split REAL,
     has_run BOOLEAN NOT NULL
);"""

sql_create_model_layers_table  = """ CREATE TABLE IF NOT EXISTS model_layers(
    mid INTEGER,
    layer_nr INTEGER,
    units INTEGER not null,
    PRIMARY KEY (mid,layer_nr)
    FOREIGN KEY (mid) references models (mid) ON DELETE CASCADE
    );"""

 #layer_depth INTEGER,
 #    layers INTEGER,
 # these are derivable from a saved modell

#remember to clean fs of model as well on delete
sql_create_projects_table = """ CREATE TABLE IF NOT EXISTS projects(
    pid INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    mid INTEGER,

    FOREIGN KEY (mid) references models (mid) ON DELETE CASCADE
    );"""

sql_create_project_houses_table = """ CREATE TABLE IF NOT EXISTS project_houses(
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
        c.execute("DROP TABLE "+table_name,())
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

def add_project_db(conn,name):

    #no params kinda odd
    sql = ''' INSERT INTO projects(name)
              VALUES(?) '''
    try:
        cur = conn.cursor()
        cur.execute(sql, (name,))
        conn.commit()
        return True
    except Error as e:
        print(e)
        return False

def add_model_db(conn, mtype, lag, batches, epochs, train_test_split):
    sql = ''' INSERT INTO models(mtype,lag,batches,epochs,train_test_split,has_run)
              VALUES(?,?,?,?,?,?) '''
    try:
        cur = conn.cursor()
        cur.execute(sql, (mtype, lag, batches,epochs,train_test_split,False))
        #finding value of auto increment
        cur.execute("SELECT last_insert_rowid();")
        mid = None
        for mid in cur:
            mid = mid[0]
        conn.commit()
        return mid
    except Error as e:
        print(e)
        return 0

 

def add_house_to_project_db(conn, pid, lclid):
    #no params kinda odd
    sql = ''' INSERT INTO project_houses(pid,lclid)
              VALUES(?,?) '''
    try:
        cur = conn.cursor()
        cur.execute(sql, (pid,lclid,))
        conn.commit()
        return True
    except Error as e:
        print(e)
        return False

def add_houses_to_project_db(conn, pid, house_list):
    #no params kinda odd
    sql = f"DELETE FROM project_houses WHERE pid='{pid}'"
    try:
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        sql = ''' INSERT INTO project_houses(pid,lclid)
                VALUES(?,?) '''
        for lclid in house_list:
            cur = conn.cursor()
            cur.execute(sql, (pid,lclid,))
            conn.commit()
        return True
    except Error as e:
        print(e)
        return False

def add_layers_to_model_db(conn, mid, layers_list):
    #no params kinda odd
    sql = f"DELETE FROM model_layers WHERE mid='{mid}'"
    try:
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        sql = ''' INSERT INTO model_layers(mid,layer_nr,units)
                VALUES(?,?,?) '''
        for k in range(len(layers_list)):
            cur = conn.cursor()
            cur.execute(sql, (mid,k+1,layers_list[k],))
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
        cur.execute("UPDATE models SET mtype=?, lag=?, batches=?, epochs=?, train_test_split=? WHERE mid = ?",(mtype, lag, batches, epochs, train_test_split, mid))
        conn.commit()
    except Error as e:
        print(e)

def set_project_has_run(conn,mid):
    try:
        cur = conn.cursor()
        cur.execute("UPDATE models SET has_run=? WHERE mid = ?",(True, mid))
        conn.commit()
    except Error as e:
        print(e)
#### DELETE #####

def delete_project(conn,pid):
    try:
        cur = conn.cursor()
        
        #deleting model should cascade delete project but it does not.
        cur.execute("SELECT mid FROM projects WHERE pid = ?",(pid,))
        for mid in cur:
             #is tuple for some reason
             print(mid)
             print(type(mid[0]))
             if mid[0] is not None:
                 delete_model(conn, mid[0])
                 delete_all_project_house_db(conn, pid)
            
        cur.execute("DELETE FROM projects WHERE pid = ?",(pid,))
        conn.commit()
    except Error as e:
        print(e)

def delete_project_house_db(conn, pid, lclid):
    #no params kinda odd
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM project_houses where pid = ? AND lclid = ?", (pid,lclid,))
        conn.commit()
        return True
    except Error as e:
        print(e)
        return False

def delete_all_project_house_db(conn, pid):
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM project_houses where pid = ?", (pid,))
        conn.commit()
        return True
    except Error as e:
        print(e)
        return False


def delete_model(conn,mid,has_run):
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM models WHERE mid = ?",(mid,))
        conn.commit()
        if has_run:
            folder_path = "./saved_models/" +str(mid)
            shutil.rmtree(folder_path)
    except Error as e:
        print(e)

def delete_all_model_layers_db(conn, mid):
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM model_layerss where mid = ?", (mid,))
        conn.commit()
        return True
    except Error as e:
        print(e)
        return False       

##### SELECTS #####

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
    date_string = float(cur.fetchone()[0])
    print(date_string)
    years = int(date_string)
    months = int((date_string*12) % 12)
    days = int((date_string*365) % 365 % 31)
    hours = int((date_string*365*24) % 24)
    date_string_formated = f"{years}-{months}-{days} {hours}:00:00"

    result['avg_tstp'] = date_string_formated
    
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
    result['std_tstp'] = date_string_formated
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
    cur.execute(f"SELECT pid, name FROM projects") 
    result = {}

    projects = []
    for (pid,name) in cur:
        project = {"id": pid, "name": name}
        projects.append(project)
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
        for (mid,mtype,lag,batches,epochs,train_test_split,has_run) in cur:
            project["mtype"] = mtype
            project["lag"] = lag
            project["mid"] = mid
            project["batches"] = batches
            project["epochs"] = epochs
            project["train_test_split"] = train_test_split
            project["has_run"] = has_run
    cur.execute("SELECT lclid FROM project_houses WHERE pid = ?",(pid,))
    house_list = []
    for (lclid) in cur:
        house_list.append(lclid[0])
    project["houses"] = house_list
    return project

def select_model_layers(conn,mid):
 cur = conn.cursor()
 cur.execute("SELECT layer_nr, units FROM model_layers WHERE mid = ?",(mid,))
 layer_dict = {}
 for (layer_nr,units) in cur:
    layer_dict[str(layer_nr)] = units
 return layer_dict

#### SETUP ####

def setup():
    conn = create_connection(database)
    if conn is not None:
        #create_table(conn, sql_create_house_table)
        #create_table(conn, sql_create_dataset_table)
        #init_database(conn)
        #init_house_info(conn)

        drop_table(conn, "models")
        drop_table(conn, "projects")
        drop_table(conn, "project_houses")
        drop_table(conn, "model_layers")

        create_table(conn, sql_create_models_table)
        create_table(conn, sql_create_projects_table)
        create_table(conn, sql_create_project_houses_table)
        create_table(conn, sql_create_model_layers_table)



        conn.close()

if __name__ == '__main__':
    setup()