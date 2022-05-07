from operator import mod
import os
from unicodedata import name
from flask import Flask, request, redirect, json, g
from flask_cors import CORS
from matplotlib.font_manager import json_dump
from numpy import empty
from sklearn.model_selection import TimeSeriesSplit, train_test_split

from setup_db import add_house_to_project_db, add_layers_to_model_db, delete_all_model_layers_db, delete_all_project_house_db, delete_project_house_db, setup, select_housedata_curve_db, select_housedata_count_db, select_lclids, update_project
from setup_db import select_projects, select_project, delete_project, add_project_db
from setup_db import delete_model, update_model, add_model_db, set_project_has_run, add_layers_to_model_db, delete_all_model_layers_db, select_model_layers
from setup_db import add_houses_to_project_db, delete_all_project_house_db

from helpers import retrieve_DT, retrieve_LSTM, retrieve_MLP, run_DT,run_LSTM,run_MLP

import sqlite3

import pandas as pd
import pickle
from datetime import datetime

# importing sys so we can find ML_classes
import sys
  
# adding ML_classes to the system path
sys.path.insert(0, '../../models/')


#from models.ML_classes
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





@app.route("/projects", methods=['GET'])
def get_projects():
   conn = get_db()  
   projects = select_projects(conn)
   print("gell")
   #projects = {"projects": [{"name": "lstmGOD", "id": 1},{"name": "mlpGOD", "id": 2}]}
   return json.dumps(projects)

@app.route('/projects',methods=["POST"])
def create_project():
    conn = get_db()
    #if any
    input_data = request.get_json()
    print(input_data)
    name = input_data["data"]["name"]
    print(name)
    add_project_db(conn,name)
   
    return json.dumps({"success": "success"})
   

@app.route('/project/<pid>',methods=["GET"])
def get_project(pid):
    conn = get_db()
    project = select_project(conn,pid)
    print(project["mid"])
    if project["mid"] is not None:
        print(project["mtype"])
        
        project["train_test_split"] = (1 - project["train_test_split"])*100
        data = make_model_dataframe( project["houses"])

        project["layer_dict"] = {}
        project["model_results"] = ""
        if project["mtype"] == "mlp" or project["mtype"] == "lstm":
            layer_dict = select_model_layers(conn,project["mid"])
            project["layer_dict"] = layer_dict
        if project["has_run"]:

            if project["mtype"] == "mlp":
                lc, layers, model_res = retrieve_MLP(project["mid"],data,project["lag"],project["batches"],project["epochs"],project["train_test_split"])
                project["layer_count"] = lc
                project["layers"] = layers
                model_res["time"] = data["tstp"].dt.strftime('%Y-%m-%d').tolist()
                model_res["energy_data"] = data["energy"].tolist()
                project["model_results"] = model_res
            elif project["mtype"] == "lstm":
                lc, layers, model_res = retrieve_LSTM(project["mid"],data,project["lag"],project["batches"],project["epochs"],project["train_test_split"])
                project["layer_count"] = lc
                project["layers"] = layers
                model_res["time"] = data["tstp"].dt.strftime('%Y-%m-%d').tolist()
                model_res["energy_data"] = data["energy"].tolist()
                project["model_results"] = model_res
            elif project["mtype"] == "dt":
                model_res = retrieve_DT(project["mid"],data,project["lag"],project["batches"],project["epochs"],project["train_test_split"])
                model_res["time"] = data["tstp"].dt.strftime('%Y-%m-%d').tolist()
                model_res["energy_data"] = data["energy"].tolist()
                project["model_results"] = model_res
    #print(project["layer_count"])
   # print(project["layers"])

    return json.dumps(project)

# perhaps callable in a different manner when model is created
@app.route('/project/<pid>',methods=["PUT"])
def server_update_project(pid):
     conn = get_db()
     input_data = request.get_json()
     mid = input_data["mid"]
     update_project(conn,pid,mid)
     return "success"

@app.route('/project/<pid>',methods=["DELETE"])
def server_delete_project(pid):
    conn = get_db()
    print("fgeg")
    delete_project(conn,pid)
    return json.dumps({"success": "successfully deleted"})


#if we want to delete and add house on a house by house basis
@app.route('/add_house/',methods=["POST"])
def add_house():
    conn = get_db()
    input_data = request.get_json()
    print(input_data)
    house= input_data["house"]
    pid = input_data["pid"]
    add_house_to_project_db(conn,pid,house)
    return json.dumps({"success": "successfully added house"})

@app.route('/delete_house/<pid>/<lclid>',methods=["DELETE"])
def server_delete_project_house(pid,lclid):
    conn = get_db()
    print("fgeg")
    delete_project_house_db(conn,pid,lclid)
    return json.dumps({"success": "successfully deleted"})


#todo
@app.route('/save_project/<pid>',methods=["PUT"])
def save_project(pid):
    conn = get_db()
    result_dict = {}


    input_data = request.get_json()['data']
    print(input_data)
    house_list = input_data["houses"]
    pid = input_data["pid"]
    mid = input_data["mid"]
    parameters = input_data["parameters"]
    
    #updating proj data
    delete_all_project_house_db(conn,pid)
    add_houses_to_project_db(conn,pid,house_list)

    #crude check to see if parameters are initiated
    if parameters["model"] != "":
        #reformating param input
        model_str = parameters["model"].lower()
        lag = parameters["lag"]
        lag = int(lag)
        epoch = int(parameters["epoch"])
        train_test_split = parameters["training"]
        train_test_split = float(train_test_split)
        train_test_split = 1- (train_test_split/100)

        if mid is None:    
            mid = add_model_db(conn,model_str, lag,256,epoch,train_test_split)
            update_project(conn,pid,mid)
        else:
            update_model(conn, mid, model_str, lag, 256, epoch, train_test_split)

        if model_str == "lstm" or model_str == "mlp":
            layers = parameters["layerDictionary"]
            layers = list(layers.values())
            layers = [int(x) for x in layers]
            if len(layers) != 0:
                add_layers_to_model_db(conn,mid,layers)
    result_dict["mid"] = mid
    return result_dict

    #update_model(conn, 1, parameters["model"], parameters["lag"], "", parameters["epoch"], parameters["training"])
    return json.dumps({"success": "successfully saved"})

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
    conn = get_db()
    print("running model")
    if request.json:
        print(request.json)
        content = request.json["content"]
        print(content)
        house_list = content["dataset"]
        m_df = make_model_dataframe(house_list)
        param_dict = content["parameters"]
        model_str = param_dict["model"].lower()
        
        model_id = content["mid"]
        model = None
        print(model_id)

        lag = param_dict["lag"]
        lag = int(lag)
        epoch = int(param_dict["epoch"])
        #print(type(epoch))

        #model wants traintestsplit as size of test
        train_test_split = param_dict["training"]
        train_test_split = float(train_test_split)
        train_test_split = 1- (train_test_split/100)
        print(train_test_split)
        projectID = content["projectID"]
        # print(m_df)
        dict = {}
        if model_str.lower() == "dt":
          epoch = 1
          model, dict =  run_DT(m_df,lag,train_test_split,epoch)
          
        elif model_str == "lstm":
            #lstm mlp may need additional params from dict
            layers = param_dict["layerDictionary"]
            layers = list(layers.values())
            layers = [int(x) for x in layers]
            print(layers)
            print("headfsaf")
            model, dict = run_LSTM(m_df,lag,train_test_split,epoch,layers)
            
        elif model_str == "slp" or model_str.lower() == "mlp":
            layers = param_dict["layerDictionary"]
            layers = list(layers.values())
            layers = [int(x) for x in layers]
            print(layers)
            #if slp layers=1 perhaps
            model, dict = run_MLP(m_df,lag,train_test_split,epoch,layers)
        else:
            return ValueError("No suitable model class was specified")

        dict["energy_data"] = m_df["energy"].tolist()
        dict["time"] = m_df["tstp"].dt.strftime('%Y-%m-%d').tolist()
        dict["mid"] = model_id

        #updating proj data
        delete_all_project_house_db(conn,projectID)
        add_houses_to_project_db(conn,projectID,house_list)
        #saving the model
        if model_id is None:
            model_id = add_model_db(conn,model_str,lag, 256, epoch, train_test_split)
            print(model_id)
            dict["mid"] = model_id
            update_project(conn,projectID,model_id)
            if model_str == "lstm" or model_str == "mlp" or model_str == "slp":
                layers = param_dict["layerDictionary"]
                layers = list(layers.values())
                layers = [int(x) for x in layers]

                add_layers_to_model_db(conn, model_id,layers)

                model.model.save("./saved_models/"+str(model_id))
            elif model_str == "dt":
                filename = "./saved_models/" + str(model_id) + "/dt.sav"
                dirpath = "./saved_models/" + str(model_id)
                os.mkdir(dirpath)
                pickle.dump(model.model, open(filename, 'wb'))
            set_project_has_run(conn,model_id)
        else:
            print("update model")
            update_model(conn, model_id, model_str, lag, 256, epoch, train_test_split)
            if model_str == "lstm" or model_str == "mlp" or model_str == "slp":
                layers = param_dict["layerDictionary"]
                layers = list(layers.values())
                layers = [int(x) for x in layers]

                add_layers_to_model_db(conn, model_id,layers)
                model.model.save("./saved_models/"+str(model_id))
            elif model_str == "dt":
                filename = "./saved_models/" + str(model_id) + "/dt.sav"
                os.remove(filename)
                pickle.dump(model.model, open(filename, 'wb'))
            set_project_has_run(conn,model_id)

        return json.dumps(dict)

    return "f"




if __name__ == "__main__":
    app.run(debug=True)