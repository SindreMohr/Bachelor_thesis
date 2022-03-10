from flask import Flask, request, redirect, json, g
from flask_cors import CORS

from setup_db import setup, select_housedata_db
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
@app.route("/get_data", methods=['GET', 'POST'])
def data():
    if request.method == "POST":
        content = request.get_json('content')
        content = content['content']
        if content == 'all':
            houses = ["MAC000150", "MAC000152", "MAC000153", "MAC000165", "MAC000169", "MAC000168","MAC000159","MAC000173", "MAC000179","MAC000181", "MAC000152", "MAC000153", "MAC000165", "MAC000169", "MAC000168","MAC000159","MAC000173", "MAC000179","MAC000181", "MAC000152", "MAC000153", "MAC000165", "MAC000169", "MAC000168","MAC000159","MAC000173", "MAC000179","MAC000181", "MAC000152", "MAC000153", "MAC000165", "MAC000169", "MAC000168","MAC000159","MAC000173", "MAC000179","MAC000181" ]
            loaded_data = houses
            return {'data': loaded_data}
        elif "MAC" in content:
            # Make db call to get information about house
            loaded_data = [1,10,5,3,5,6,3]
            return json.dumps({'data': loaded_data})
    return ""

@app.route("/household/<lclid>", methods=['GET'])
def get_household_data(lclid):
    df = pd.read_csv('../../../data/ouput.csv')
    df['tstp'] = [datetime.strptime(x, '%Y-%m-%d %H:%M:%S') for x in df['tstp']]
    #df["tstp"] = pd.to_datetime(df["tstp"])
    df["energy(kWh/hh)"] = pd.to_numeric(df["energy(kWh/hh)"], downcast="float", errors="coerce")

    max_value_energy = df["energy(kWh/hh)"].max()
    df['energy(kWh/hh)'] = df['energy(kWh/hh)'].apply(lambda x: x / max_value_energy)
    # Sorting the values
    df.sort_values('tstp', inplace=True)

    #lclid_list = df['LCLid'].unique()
    
    filt = df["LCLid"] == lclid
    hh = df[filt]
    
    hh.pop("LCLid")
    hh = hh.set_index("tstp")
    hh = hh.resample("H").sum()
    hh = hh.reset_index()

    return json.dumps({'data': hh})

if __name__ == "__main__":
    app.run(debug=True)