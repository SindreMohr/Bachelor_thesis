
import imp
from operator import mod
import pandas as pd
import numpy as np
import math
from keras.models import Sequential, load_model
from keras.layers import  Input, Dense

#
from ML_classes.NN_data_creator import plain_data_creator

class LinearModel():
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
    
    # @staticmethod
    # def create_X_Y(ts: list, lag: int) -> tuple:
    #     """
    #     A method to create X and Y matrix from a time series list for the training of 
    #     deep learning models 
    #     """
    #     X, Y = [], []

    #     if len(ts) - lag <= 0:
    #         X.append(ts)
    #     else:
    #         for i in range(len(ts) - lag):
    #             Y.append(ts[i + lag])
    #             X.append(ts[i:(i + lag)])

    #     X, Y = np.array(X), np.array(Y)

    #     # Reshaping the X array to an linear input shape 
    #     X = np.reshape(X, (X.shape[0], X.shape[1], 1))
    #     return X, Y         

    # def create_data_for_NN(
    #     self,
    #     use_last_n=None
    #     ):
    #     """
    #     A method to create data for the neural network model
    #     """
    #     # Extracting the main variable we want to model/forecast
    #     y = self.data[self.Y_var].tolist()

    #     # Subseting the time series if needed
    #     if use_last_n is not None:
    #         y = y[-use_last_n:]

    #     # The X matrix will hold the lags of Y 
    #     X, Y = self.create_X_Y(y, self.lag)

    #     # Creating training and test sets 
    #     X_train = X
    #     X_test = []

    #     Y_train = Y
    #     Y_test = []

    #     if self.train_test_split > 0:
    #         index = round(len(X) * self.train_test_split)
    #         X_train = X[:(len(X) - index)]
    #         X_test = X[-index:]     
            
    #         Y_train = Y[:(len(X) - index)]
    #         Y_test = Y[-index:]

    #     return X_train, X_test, Y_train, Y_test

    def LinearModel(self):
        """
        A method to fit the Linear model 
        """
        # Getting the data 
        X_train, X_test, Y_train, Y_test = self.dc.create_data_for_NN(self.data, self.Y_var, self.lag, self.train_test_split)

       # print(X_train)
        #print(Y_train)

        # Defining the model
        model = Sequential()
        model.add(Input(shape=(self.lag),))
        model.add(Dense(1))
        model.compile(optimizer='adam', loss='mse')

        # Defining the model parameter dict 
        keras_dict = {
            'x': X_train,
            'y': Y_train,
            'batch_size': self.batch_size,
            'epochs': self.epochs,
            'shuffle': False
        }

        if self.train_test_split > 0:
            keras_dict.update({
                'validation_data': (X_test, Y_test)
            })

        # Fitting the model 
        model.fit(
            **keras_dict
        )

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

            # Making the prediction list 
            yhat = [y[0] for y in self.model.predict(X_test)]

        return yhat

    def predict_n_ahead(self, n_ahead: int):
        """
        A method to predict n time steps ahead
        """    
        X, _, _, _ = self.dc.create_data_for_NN(self.data, self.Y_var, self.lag, self.train_test_split, use_last_n=self.lag)

        # Making the prediction list 
        yhat = []

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
            X = np.reshape(X, (1, len(X), 1))

        return yhat    
    
    def save_lstm_model(self):
        #consider saving and loading other parameters
        self.model.save("./saved_models/lstm_model")
    def load_lstm_model(self):
        #currently doesnt load other class parameters ...
        # add options for households perhaps
        model_load =  load_model("./saved_models/lstm_model")
        self.model = model_load
       
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
            error += (abs(y_test[i] - predictions[i])/y_test[i])*100
        error = error / n
        return error