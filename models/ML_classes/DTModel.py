
import imp
from operator import mod
import pandas as pd
import numpy as np
import math
import os
from keras.models import Sequential, load_model
from keras.layers import  Input, Dense

from sklearn import tree

#
from ML_classes.NN_data_creator import plain_data_creator, temperature_data_creator
from ML_classes.evaluator import Evaluator

class DTModel():
    """
    A class to create a deep time series model
    """

    def __init__(self, data: pd.DataFrame, Y_var: str, lag: int, epochs=10, batch_size=256, train_test_split=0, data_creator = "plain"):
        self.data = data 
        self.Y_var = Y_var 
        self.lag = lag 
        self.batch_size = batch_size
        self.epochs = epochs
        self.train_test_split = train_test_split

        self.model = None
        self.eval = None

        #mode for training
        if data_creator == "plain":
            self.dc = plain_data_creator()
        elif data_creator == "temperature":
            self.dc = temperature_data_creator()
        else:
             raise ValueError("unknown dc")
    def alter_x_shape(self, x):
        # naive slow o(n^2)
        res = []
        for element in x:
            
            temp = []
            for val in element:
               val = val[0]
               temp.append(val)
            #temp = temp[0]
            res.append(temp)
        res = np.asarray(res)
        #print(res)
        return res

    def DTModel(self):
        """
        A method to fit the Linear model 
        """
        # Getting the data 
        X_train, _, Y_train, Y_test = self.dc.create_data_for_NN(self.data, self.Y_var, self.lag, self.train_test_split)
        #print(X_train)
        #X_train, Y_train = self.dc.create_X_Y(ts = self.data[self.Y_var], lag = self.lag )
        #X_test = self.alter_x_shape(X_test)
        X_train =  self.alter_x_shape(X_train)
       # print(X_train)
        #print(Y_train)

        # Defining the model
        model = tree.DecisionTreeRegressor()
       
        model = model.fit(X_train, Y_train)
       
        # Saving the model to the class 
        self.model = model

        self.eval = Evaluator(Y_test,self.data,self.predict(),self.train_test_split,self.lag)


        return model

    def predict(self) -> list:
        """
        A method to predict using the test data used in creating the class
        """
        yhat = []

        if(self.train_test_split > 0):
        
            # Getting the last n time series 
            _, X_test, _, _ = self.dc.create_data_for_NN(self.data, self.Y_var, self.lag, self.train_test_split)  
            X_test = self.alter_x_shape(X_test)

            #print(X_test)
            # Making the prediction list 
            yhat = [y for y in self.model.predict(X_test)]

        return yhat

    def predict_n_ahead(self, n_ahead: int):
        """
        A method to predict n time steps ahead
        """    
        X, _, _, _ = self.dc.create_data_for_NN(self.data, self.Y_var, self.lag, self.train_test_split, use_last_n=self.lag)
        X = self.alter_x_shape(X)

        # Making the prediction list 
        yhat = []
        #print(X.shape)
        for _ in range(n_ahead):
            # Making the prediction
            fc = self.model.predict(X)
            #print(fc)
            yhat.append(fc)

            # Creating a new input matrix for forecasting
            X = np.append(X, fc)

            # Ommiting the first variable
            X = np.delete(X, 0)

            # Reshaping for the next iteration
            X = np.reshape(X, (1, len(X)))
            #print(X.shape)
        return yhat    
    
    def plot_dt(self):
        tree.plot_tree(self.model, max_depth=3)
       
    