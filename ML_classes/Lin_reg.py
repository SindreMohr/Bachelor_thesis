import math
from operator import mod
from textwrap import indent
from typing_extensions import Self
import pandas as pd
import numpy as np

from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

from datetime import datetime, timedelta

from ML_classes.NN_data_creator import plain_data_creator


class Lin_reg_baseline():
   def __init__(self, data: pd.DataFrame, Y_var: str, train_test_split=0.15, mode="basic", lag = 24):
        self.data = data 
        self.Y_var = Y_var
        self.train_test_split = train_test_split
        self.mode = mode
        self.lag = lag

        self.dc = plain_data_creator()

        # Extracting the main variable we want to model/forecast
        self.y = data[Y_var].tolist()
        x = []
        for i in range(len(self.y)):
            x.append(i)
        index = round(len(self.y)* self.train_test_split)
        
        #
        self.x_train = []
        self.x_test = []
        self.y_train = np.array(self.y[:-index])
        self.y_test = np.array(self.y[-index:])
        if self.mode == "basic":
            self.x_train = np.array(x[:-index]).reshape((-1,1))
            self.x_test = np.array(x[-index:]).reshape((-1,1))
        elif self.mode =="tstp":
            temp =  data.tstp.values.astype(np.int64) // 10 ** 9
            temp = temp.tolist()
            self.x_train = np.array(temp[:-index]).reshape((-1,1))
            self.x_test =  np.array(temp[-index:]).reshape((-1,1))
        elif self.mode == "auto":
            self.x_train, self.x_test, self.y_train, self.y_test = self.dc.create_data_for_NN(self.data,self.Y_var,self.lag,self.train_test_split)
            self.x_train = self.alter_x_shape(self.x_train)
            
            self.x_test = self.alter_x_shape(self.x_test)
           


            #print(self.x_train)
            #print( f"one vector:  {self.x_train[0]}")
            #print(self.x_train.shape)
            #print(len(self.y_train))
            

        else:
            raise ValueError("mode unrecognized")
        
        self.model = None

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
    
   def alter_x_shape_alt(self, x):
        res = []
        for _ in range(self.lag):
            res.append([])
        for element in x:
            
            for k in range(self.lag):
               val = element[k][0]
               res[k].append(val)
           
        res = np.asarray(res)
        
        return res


   def model_init(self):
     #x_ = PolynomialFeatures(degree=2, include_bias=False).fit_transform(self.x_train)
     self.model = LinearRegression().fit(self.x_train, self.y_train)
        
   def predictions(self):
      # x_ = PolynomialFeatures(degree=2, include_bias=False).fit_transform(self.x_test)
       predictions = self.model.predict(self.x_test)

       return predictions

   def predict_n_ahead(self,n):
      
       predictions = []
       if self.mode == "basic":
           predict_from = len(self.y)
           for _ in range(n):
               predict_from += 1
               x = np.array(predict_from).reshape((-1,1))
               predictions.append(self.model.predict(x))
       elif self.mode == "tstp":
            predict_from = self.x_train[-1][0]
            for _ in range(n):
                predict_from += 3600
                x = np.array(predict_from).reshape((-1,1))
                predictions.append(self.model.predict(x))
       elif self.mode == "auto":
            X, _, _, _ = self.dc.create_data_for_NN(self.data, self.Y_var, self.lag, self.train_test_split, use_last_n=self.lag)
            X = self.alter_x_shape(X)
            for _ in range(n):
                # Making the prediction
                fc = self.model.predict(X)
                #print(fc)
                predictions.append(fc)

                # Creating a new input matrix for forecasting
                X = np.append(X, fc)

                # Ommiting the first variable
                X = np.delete(X, 0)

                # Reshaping for the next iteration
                X = np.reshape(X, (1, len(X)))
       return predictions

   def evaluateMSE(self):
        predictions = self.predictions()

         # Getting actual y 
        y_test = self.y_test
        # print(len(predictions))
        # print(len(y_test))

        n = len(y_test)
        squared_error = 0
        for i in range(n):
            squared_error += (y_test[i] - predictions[i]) ** 2
        squared_error = squared_error / n
        return squared_error

   def evaluateRMSE(self):
        
        return math.sqrt(self.evaluateMSE())
   def evaluateMAE(self):
        predictions = self.predictions()

         # Getting actual y 
        y_test = self.y_test
        error = 0
        n = len(y_test)
        for i in range(n):
            error += abs(y_test[i] - predictions[i])
        error = error / n
        return error
   def evaluateMAPE(self):
        predictions = self.predictions()

          # Getting actual y 
        y_test = self.y_test
        n = len(y_test)
        error = 0
        for i in range(n):
            #cant divide by 0
            if y_test[i] == 0:
                continue
            error += (abs(y_test[i] - predictions[i])/y_test[i])*100
        error = error / n
        return error
   def print_test(self):
        pass