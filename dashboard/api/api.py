from unicodedata import name
from flask import Flask, request, redirect, json, g
from flask_cors import CORS
from sklearn.model_selection import TimeSeriesSplit

from setup_db import setup, select_housedata_curve_db, select_housedata_count_db, select_lclids
import sqlite3

import pandas as pd
from datetime import datetime

# importing sys so we can find ML_classes
import sys
  
# adding ML_classes to the system path
sys.path.insert(0, '../../')

from ML_classes.MLPModel import MLPModel


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
    #print(data)
    return json.dumps({'data': data})

@app.route("/household_data_curve/<lclid>", methods=['GET'])
def get_household_data_curve(lclid):
    conn = get_db()
    datalist = select_housedata_curve_db(conn,lclid)
    return json.dumps({'house_data': datalist})

@app.route("/household_data_count/<lclid>", methods=['GET'])
def get_household_data_count(lclid):
    conn = get_db()
    datalist = select_housedata_count_db(conn,lclid)
    return json.dumps({'house_data_count': datalist})

#obtaining a dataframe to feed into model
def make_model_dataframe(house_list):
    conn = get_db()
    df = pd.DataFrame()
    for house in house_list:
        datalist = select_housedata_curve_db(conn,house)
        tlist = datalist["time"]
        vlist = datalist["values"]
        tseries = pd.Series(data=tlist,name="tstp")
        vseries = pd.Series(data=vlist,name="energy")
        res_df = pd.merge(tseries, vseries, right_index=True, left_index=True)
    df = pd.concat(df,res_df)
    return df

#making the dataframe suitable for model
def dataframe_preprocess(df):

    #for hourly data, consider alternate method with these uncommented
    #hh = hh.set_index("tstp")
    #hh = hh.resample("H").sum()
    #hh = hh.reset_index()

    #normalization
    df_max = df['energy'].max()
    df['energy'] = df['energy'].apply(lambda x: x / df_max)

    return df

if __name__ == "__main__":
    app.run(debug=True)