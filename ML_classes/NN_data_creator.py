from operator import mod
import pandas as pd
import numpy as np
#from pyrsistent import T


class plain_data_creator():
    
    @staticmethod
    def create_X_Y(ts: list, lag: int) -> tuple:
        """
        A method to create X and Y matrix from a time series list for the training of 
        deep learning models 
        """
        X, Y = [], []

        if len(ts) - lag <= 0:
            X.append(ts)
        else:
            for i in range(len(ts) - lag):
                Y.append(ts[i + lag])
                X.append(ts[i:(i + lag)])

        X, Y = np.array(X), np.array(Y)

        # Reshaping the X array to an linear input shape 
        X = np.reshape(X, (X.shape[0], X.shape[1], 1))
        return X, Y         

    def create_data_for_NN(self,
        data, Y_var, lag, train_test_split,
        use_last_n=None
        ):
        """
        A method to create data for the neural network model
        """
        # Extracting the main variable we want to model/forecast
        y = data[Y_var].tolist()

        # Subseting the time series if needed
        if use_last_n is not None:
            y = y[-use_last_n:]

        # The X matrix will hold the lags of Y 
        X, Y = self.create_X_Y(y, lag)

        # Creating training and test sets 
        X_train = X
        X_test = []

        Y_train = Y
        Y_test = []

        if train_test_split > 0:
            index = round(len(X) * train_test_split)
            X_train = X[:(len(X) - index)]
            X_test = X[-index:]     
            
            Y_train = Y[:(len(X) - index)]
            Y_test = Y[-index:]

        return X_train, X_test, Y_train, Y_test




class temperature_data_creator():
    
    @staticmethod
    def create_X_Y(ts: list, tlist: list, lag: int) -> tuple:
        """
        A method to create X and Y matrix from a time series list for the training of 
        deep learning models 
        """
        X, Y = [], []

        if len(ts) - lag <= 0:
           temp = ts.copy()

           for number in tlist:
               temp.append(number)
           X.append(temp)
        else:
            for i in range(len(ts) - lag):
                Y.append(ts[i + lag])
                energy_x = ts[i:(i + lag)]
                temp_x = tlist[i:(i+lag)]
                for number in temp_x:
                    #print(number)
                    energy_x.append(number)
                X.append(energy_x)

        X, Y = np.array(X), np.array(Y)

        # Reshaping the X array to an linear input shape 
        X = np.reshape(X, (X.shape[0], X.shape[1], 1))
        return X, Y         

    def create_data_for_NN(self,
        data, Y_var, lag, train_test_split,
        use_last_n=None
        ):
        """
        A method to create data for the neural network model
        """
        # Extracting the main variable we want to model/forecast
        y = data[Y_var].tolist()
        t = data["temperature"].tolist()
        # Subseting the time series if needed
        if use_last_n is not None:
            y = y[-use_last_n:]

        # The X matrix will hold the lags of Y 
        X, Y = self.create_X_Y(y, t, lag)

        # Creating training and test sets 
        X_train = X
        X_test = []

        Y_train = Y
        Y_test = []

        if train_test_split > 0:
            index = round(len(X) * train_test_split)
            X_train = X[:(len(X) - index)]
            X_test = X[-index:]     
            
            Y_train = Y[:(len(X) - index)]
            Y_test = Y[-index:]

        return X_train, X_test, Y_train, Y_test