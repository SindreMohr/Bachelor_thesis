
import imp
from operator import mod
import pandas as pd
import numpy as np
import math
from keras.models import Sequential, load_model
from keras.layers import  Input, Dense

#
from ML_classes.NN_data_creator import plain_data_creator, temperature_data_creator
from ML_classes.evaluator import Evaluator

class MLPModel():
    """
    A class to create a deep time series model
    """

    def __init__(self, data: pd.DataFrame, Y_var: str, lag: int, layer_depths: list, layer_count: int, epochs=10, batch_size=256, train_test_split=0, data_creator = "plain"):
        self.data = data 
        self.Y_var = Y_var 
        self.lag = lag 
        self.layer_count = layer_count
        self.layer_depths = layer_depths
        self.batch_size = batch_size
        self.epochs = epochs
        self.train_test_split = train_test_split

        self.model = None
          #mode for training
        if data_creator == "plain":
            self.dc = plain_data_creator()
        elif data_creator == "temperature":
            self.dc = temperature_data_creator()
        else:
             raise ValueError("unknown dc")
    

    def MLPModel(self):
        """
        A method to fit the Linear model 
        """
        # Getting the data 
        X_train, X_test, Y_train, Y_test = self.dc.create_data_for_NN(self.data, self.Y_var, self.lag, self.train_test_split)

       
        # Defining the model
        model = Sequential()
        model.add(Input(shape=(len(X_train[0])),))
        #building layers to specification, activation method can be passed in as part of list as a tuple
        for j in range(self.layer_count):
            model.add(Dense(self.layer_depths[j], activation="relu"))
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
        self.history = model.fit(
            **keras_dict
        )

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
    
   