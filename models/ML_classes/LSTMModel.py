
from ast import For
import pandas as pd
import numpy as np
from keras.models import Sequential, load_model
from keras.layers import LSTM, Dense

 
from ML_classes.NN_data_creator import plain_data_creator, temperature_data_creator
from ML_classes.evaluator import Evaluator

class LSTMModel():
    """
    A class to create a deep time series model
    """

    def __init__(self, data: pd.DataFrame, Y_var: str, lag: int, LSTM_layer_depths: list, epochs=10, batch_size=256, train_test_split=0, data_creator = "plain"):
        self.data = data 
        self.Y_var = Y_var 
        self.lag = lag 
        self.LSTM_layer_depths = LSTM_layer_depths
        #self.LSTM_layers = LSTM_layers
        self.batch_size = batch_size
        self.epochs = epochs
        self.train_test_split = train_test_split

        self.model = None
        self.Eval = None

        #mode for training
        if data_creator == "plain":
            self.dc = plain_data_creator()
        elif data_creator == "temperature":
            self.dc = temperature_data_creator()
        else:
             raise ValueError("unknown dc")
    
  

    def LSTModel(self):
        """
        A method to fit the LSTM model 
        """
        # Getting the data 
        #X_train, X_test, Y_train, Y_test = self.create_data_for_NN()
        X_train, X_test, Y_train, Y_test = self.dc.create_data_for_NN(self.data, self.Y_var, self.lag, self.train_test_split)

        # Defining the model
        model = Sequential()
        if len(self.LSTM_layer_depths) > 1:

            model.add(LSTM(self.LSTM_layer_depths[0], activation='relu', input_shape=(len(X_train[0]), 1), return_sequences=True))
            for idx, dephts in enumerate(self.LSTM_layer_depths[1:]):
                #model.add(LSTM(dephts, activation='relu'))

                if idx+1 == len(self.LSTM_layer_depths)-1:
                     model.add(LSTM(dephts, activation='relu'))
                else:
                     model.add(LSTM(dephts, activation='relu',return_sequences=True))

        else:
            model.add(LSTM(self.LSTM_layer_depths[0], activation='relu', input_shape=(len(X_train[0]), 1)))
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
            # _, X_test, _, _ = self.create_data_for_NN()
            _, X_test, _, _ = self.dc.create_data_for_NN(self.data, self.Y_var, self.lag, self.train_test_split)              

            # Making the prediction list 
            yhat = [y[0] for y in self.model.predict(X_test)]

        return yhat

    def predict_n_ahead(self, n_ahead: int):
        """
        A method to predict n time steps ahead
        """    
        #X, _, _, _ = self.create_data_for_NN(use_last_n=self.lag)        
        X, _, _, _ = self.dc.create_data_for_NN(self.data, self.Y_var, self.lag, self.train_test_split, use_last_n=self.lag)

        # Making the prediction list 
        yhat = []

        for _ in range(n_ahead):
            # Making the prediction
            fc = self.model.predict(X)
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
       
   