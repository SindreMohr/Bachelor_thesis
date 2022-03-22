from flask import Flask, request, redirect, json, g
from flask_cors import CORS

from setup_db import setup, select_housedata_curve_db, select_housedata_count_db, select_lclids
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


if __name__ == "__main__":
    app.run(debug=True)