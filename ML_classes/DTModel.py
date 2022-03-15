
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
from ML_classes.NN_data_creator import plain_data_creator

class DTModel():
    """
    A class to create a deep time series model
    """

    def __init__(self, data: pd.DataFrame, Y_var: str, lag: int, epochs=10, batch_size=256, train_test_split=0):
        self.data = data 
        self.Y_var = Y_var 
        self.lag = lag 
        self.batch_size = batch_size
        self.epochs = epochs
        self.train_test_split = train_test_split
        self.dc = plain_data_creator()
    
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
        X_train, _, Y_train, _ = self.dc.create_data_for_NN(self.data, self.Y_var, self.lag, self.train_test_split)

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
       
    def evaluateMSE(self):
        predictions = self.predict()

         # Getting actual y 
        _, _, _, y_test = self.dc.create_data_for_NN(self.data, self.Y_var, self.lag, self.train_test_split)
        n = len(y_test)
        squared_error = 0
        for i in range(n):
            squared_error += (y_test[i] - predictions[i]) ** 2
        squared_error = squared_error / n
        return squared_error

    def evaluateRMSE(self):
        
        return math.sqrt(self.evaluateMSE())

    def evaluateMAE(self):
        predictions = self.predict()

         # Getting actual y 
        _, _, _, y_test = self.dc.create_data_for_NN(self.data, self.Y_var, self.lag, self.train_test_split)
        n = len(y_test)
        error = 0
        for i in range(n):
            error += abs(y_test[i] - predictions[i])
        error = error / n
        return error

    def evaluateMAPE(self):
        predictions = self.predict()

         # Getting actual y 
        _, _, _, y_test = self.dc.create_data_for_NN(self.data, self.Y_var, self.lag, self.train_test_split) 
        n = len(y_test)
        error = 0
        for i in range(n):
            #cant divide by 0
            if y_test[i] == 0:
                continue
            error += (abs(y_test[i] - predictions[i])/y_test[i])*100
        error = error / n
        return error