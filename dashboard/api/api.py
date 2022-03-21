from flask import Flask, request, redirect, json, g
from flask_cors import CORS

from setup_db import setup, select_housedata_db, select_lclids
import sqlite3

import pandas as pd
from datetime import datetime

app = Flask(__name__)

CORS(app)
DATABASE = './database.db'

#setting the database up
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        g._database = sqlite3.connect(DATABASE)
        db = g._database
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.after_request
def add_header(response):
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['Access-Control-Allow-Methods'] = "POST, GET, OPTIONS"
    response.headers['Access-Control-Allow-Headers'] = "Content-Type, Content-Length, Authorization"
    return response

# split up into different get routes instead of post or replace with actual csv/db call routes 
@app.route("/get_lclids", methods=['GET'])
def data():
    conn = get_db()
    data = select_lclids(conn)
    print(data)
    return json.dumps({'data': data})

@app.route("/household/<lclid>", methods=['GET'])
def get_household_data(lclid):
    conn = get_db()

    datalist = select_housedata_db(conn,lclid)
    time = datalist['time']
    values = datalist['values']

    # df = pd.read_csv('../../../data/ouput.csv')
    #df =  pd.DataFrame(datalist)
    # df['tstp'] = [datetime.strptime(x, '%Y-%m-%d %H:%M:%S') for x in df['tstp']]
    # df["tstp"] = pd.to_datetime(df["tstp"])
    # #df["energy(kWh/hh)"] = pd.to_numeric(df["energy(kWh/hh)"], downcast="float", errors="coerce")

    # #max_value_energy = df["energy(kWh/hh)"].max()
    # #df['energy(kWh/hh)'] = df['energy(kWh/hh)'].apply(lambda x: x / max_value_energy)
    # # Sorting the values
    # df.sort_values('tstp', inplace=True)

    # #lclid_list = df['LCLid'].unique()
    
    # filt = df["LCLid"] == lclid
    # hh = df[filt]
    
    # hh.pop("LCLid")
    # hh = hh.set_index("tstp")
    # hh = hh.resample("H").sum()
    # hh = hh.reset_index()
    
    return json.dumps({'house_data': datalist})


if __name__ == "__main__":
    app.run(debug=True)