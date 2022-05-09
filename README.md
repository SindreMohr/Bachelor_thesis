# Predicting short term point load forecasting of power consumption in residential housing
Daniel Havstad, Danny Vo, Sindre Mohr

## About this project
Det finnes mange forskjellige modeller som blir brukt til å lage prediksjoner. Ved hjelp av deep learning modeller kan vi trene opp en modell til å lage predikasjoner frem i tid basert på tidligere målinger. I dette prosjektet vil vi lage en load forecasting system som vil lage predikasjoner for den neste timen. Vi vil lage ulike modeller for load forecasting av strømforbruket til et hushold og finne ut hvilken av algoritmene som vil gi best resultat. Dette vil så bli integrert og visualisert ved hjelp av et dashboard. 

## Models
- LSTM
- Perceptron
- SLP
- Decision tree
- Linær Regresjon

## How to run
- Use `pip install -r requirement.txt` to install the dependencies
### Start backend server
- Cd into dashboard/api
- Use `python api.py`

### Start frontend server
- Cd into dashboard/dashboard
- Use `npm install` and then `npm start` to start the server
- Open localhost in your browser

# API

export FLASK_ENV=development
export FLASK_APP=api.py
flask run

# Dashboard

## Introduction
The application is a dashboard used to interact with a deep learning model.

The model lets the user select which parts of a dataset to use in the model.


The dataset can be shown visually, and the user will be presented with information about the data:
- how many missing values are there
- how many values are there
- max-min values


The choosen data can be loaded, and the user is be able to manipulate the data with the following options:
- Remove
	- Holidays
	- Missing data entries
	- Start-Stop data (crop)
- Interpolate data for missing values
- Remove columns
- Scale data in a column by a factor(?)


The user then selects which model to use on the dataset. The user should is able to:
- Select training/test split
- Select which columns to use in the model
- Number of Epochs
- Length of lag
- When the predictions should be made for


The results from the model is presented in a default setup. The user is presented with:
- Accuracy
- Predicted values
- Predicted values together with measured values
- Lots of nice plots
The user can change in which way the result is displayed, and has multiple ways to export the result (csv, xlsx(?), pdf, quick-grab-copy-thingy)

## Backend
Backend API is written in Python Flask, and serves data with HTTP methods POST, GET.
The application utilizes a SQLite database, with a large focus on related tables. The data in question is large datasets, and therefore there are tables dedicated to describing the data, such that a request from the frontend won't require large calculations on the server side to respond.
The backend with serve multiple requests on different resources(?) where some take query parameters. The manipulation the user enters to the dataset will in practice not take effect before the API call to run the model. However, the impression to the user that a dataset is loaded buys the application time to run fetch information, and laod other neccessary resources.
The reasoning for using python on the backend is to have access to the code already written in python, as well as having access to the neccessary libraries pandas, numpy and TF.

## Frontend
Frontend is a react.js application fetching data from the API using ASYNC methods. The frontend utilizes forms for posting parameters to the API which will be used when running the model. The frontend is solely written for desktop, as there is little to no usage from mobile devices.


Usage:
	Either load existing project or create new
