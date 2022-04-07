import imp
from pyexpat import model
from unicodedata import name
from flask import Flask, request, redirect, json, g
from flask_cors import CORS
from matplotlib.font_manager import json_dump
from sklearn.model_selection import TimeSeriesSplit, train_test_split

from setup_db import setup, select_housedata_curve_db, select_housedata_count_db, select_lclids
import sqlite3

import pandas as pd
from datetime import datetime

# importing sys so we can find ML_classes
import sys
  
# adding ML_classes to the system path
sys.path.insert(0, '../../')

from ML_classes.MLPModel import MLPModel
from ML_classes.LSTMModel import LSTMModel
from ML_classes.DTModel import DTModel

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
        tseries = pd.to_datetime(tseries)

        vseries = pd.Series(data=vlist,name="energy")
        res_df = pd.merge(tseries, vseries, right_index=True, left_index=True)

      

        df = pd.concat([df,res_df])
     

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

@app.route("/run-model", methods=['POST'])
def run_model():
    print("running model")
    if request.json:
        print(request.json)
        content = request.json["content"]
        print(content)
        house_list = content["dataset"]
        m_df = make_model_dataframe(house_list)
        param_dict = content["parameters"]
        model_str = param_dict["model"]
        
        lag = param_dict["lag"]
        epoch = int(param_dict["epoch"])
        
        
        #model wants traintestsplit as size of test
        train_test_split = param_dict["training"]
        train_test_split = float(train_test_split)
        train_test_split = 1- (train_test_split/100)
        print(train_test_split)
        projectID = content["projectID"]
        print(m_df)
        dict = {}
        if model_str.lower() == "dt":
          dict =  DT(m_df,lag,train_test_split,epoch)
          #dict["data"] = m_df.to_json()
          #return json.dumps(dict)
        elif model_str.lower() == "lstm":
            #lstm mlp may need additional params from dict
            layers = param_dict["layer"]
            dict = LSTM(m_df,lag,train_test_split,epoch)
            #return json.dumps(dict)
        elif model_str.lower() == "slp" or model_str.lower() == "mlp":
            layers = param_dict["layer"]
            #if slp layers=1 perhaps
            dict = MLP(m_df,lag,train_test_split,epoch)
        else:
            return ValueError("No suitable model class was specified")

        dict["energy_data"] = m_df["energy"].tolist()
        dict["time"] = m_df["tstp"].dt.strftime('%Y-%m-%d').tolist()
           
        return json.dumps(dict)

    return "f"


def DT(data,lag,train_test,epoch):

    DT = DTModel(
    data = data,
    Y_var = 'energy',
    lag = lag,
    epochs = epoch,
    batch_size = 256,
    train_test_split = train_test
    )
    #training
    DT.DTModel()
    print("done training")
    model_result_dict = {}
    model_result_dict["predictions"] = DT.predict()
    model_result_dict["mse"] = DT.eval.MSE()
    model_result_dict["rmse"] = DT.eval.RMSE()
    model_result_dict["mae"] = DT.eval.MAE()
    model_result_dict["mape"] = DT.eval.MAPE()

    peaks, peak_dates, peak_indexes, res = DT.eval.peak_daily_consumption()
    model_result_dict["daily_peaks"] = peaks
    model_result_dict["daily_peak_dates"] = peak_dates
    model_result_dict["daily_peaks_indexes"] = peak_indexes
    model_result_dict["daily_peaks_res"] = res

    return model_result_dict

def LSTM(data,lag,train_test,epoch):

    LSTM = LSTMModel(
        data = data,
        Y_var = 'energy',
        lag = lag,
        LSTM_layer_depths = [50],
        epochs =epoch,
        batch_size = 256,
        train_test_split = train_test
    )
    #training
    LSTM.LSTModel()

    print("done training")
    model_result_dict = {}
    model_result_dict["predictions"] = LSTM.predict()
    model_result_dict["predictions"] =   [ float(x) for x in  model_result_dict["predictions"] ]

    model_result_dict["mse"] = LSTM.eval.MSE()
    model_result_dict["rmse"] = LSTM.eval.RMSE()
    model_result_dict["mae"] = LSTM.eval.MAE()
    model_result_dict["mape"] = LSTM.eval.MAPE()

    peaks, peak_dates, peak_indexes, res = LSTM.eval.peak_daily_consumption()
    model_result_dict["daily_peaks"] = peaks
    model_result_dict["daily_peak_dates"] = peak_dates
    model_result_dict["daily_peaks_indexes"] = peak_indexes
    model_result_dict["daily_peaks_res"] = res


    return model_result_dict

def MLP(data,lag,train_test,epoch):

    MLP = MLPModel(
        data = data,
        Y_var = 'energy',
        lag = lag,
        layer_depths = [30],
        layer_count= 1,
        epochs =epoch,
        batch_size = 256,
        train_test_split = train_test
    )
    #training
    MLP.MLPModel()

    print("done training")
    model_result_dict = {}
    model_result_dict["predictions"] = MLP.predict()
    model_result_dict["predictions"] =   [ float(x) for x in  model_result_dict["predictions"] ]


    model_result_dict["mse"] = MLP.eval.MSE()
    model_result_dict["rmse"] = MLP.eval.RMSE()
    model_result_dict["mae"] = MLP.eval.MAE()
    model_result_dict["mape"] = MLP.eval.MAPE()

    peaks, peak_dates, peak_indexes, res = MLP.eval.peak_daily_consumption()
    model_result_dict["daily_peaks"] = peaks
    model_result_dict["daily_peak_dates"] = peak_dates
    model_result_dict["daily_peaks_indexes"] = peak_indexes
    model_result_dict["daily_peaks_res"] = res

    #print(type(model_result_dict["mse"]))
    #print(type(model_result_dict["predictions"][0]))
    #print(type(model_result_dict["daily_peaks"][0]))
    #print(type(model_result_dict["daily_peak_dates"][0]))
    return model_result_dict

if __name__ == "__main__":
    app.run(debug=True)