
import math


class Evaluator():
    def __init__(self, y_test, data, predictions, train_test_split, lag):
        self.y_test = y_test
        self.predictions = predictions
        self.data = data
        self.train_test_split = train_test_split
        self.lag = lag
    
    def MSE(self):
        
        n = len(self.y_test)
        squared_error = 0
        for i in range(n):
            squared_error += (self.y_test[i] - self.predictions[i]) ** 2
        squared_error = squared_error / n
        return squared_error

    def RMSE(self):
        
        return math.sqrt(self.MSE())

    def MAE(self):
     
        n = len(self.y_test)
        error = 0
        for i in range(n):
            error += abs(self.y_test[i] - self.predictions[i])
        error = error / n
        return error

    def MAPE(self):

        n = len(self.y_test)
        error = 0
        for i in range(n):
            #cant divide by 0
            if self.y_test[i] == 0:
                print(i)
                continue
            error += (abs(self.y_test[i] - self.predictions[i])/self.y_test[i])*100
        error = error / n
        return error


    def peak_daily_consumption(self):
       
        #making data equal to test
        datetime_X_test = self.data["tstp"].tolist()
        datetime_X_test = datetime_X_test[self.lag:]
        index = round(len(datetime_X_test) * self.train_test_split)
        datetime_X_test = datetime_X_test[-index:]
        
        #finding daily peaks
        curr_day =datetime_X_test[0].day_name()
        curr_datetime = datetime_X_test[0]
        curr_peak= 0
        curr_peak_index = 0
        peak_indexes = []
        peaks = []
        peak_dates = []
        for cur in range(len(datetime_X_test)):
            if self.y_test[cur] > curr_peak:
                curr_peak = self.y_test[cur]
                curr_peak_index = cur
                curr_datetime = datetime_X_test[cur]
               
            if curr_day != datetime_X_test[cur].day_name():
                #the day changes, possible loss of peak on first day due to cut of measurements
                peaks.append(curr_peak)
                peak_dates.append(curr_datetime)
                peak_indexes.append(curr_peak_index)
                curr_peak = 0

            
                curr_day = datetime_X_test[cur].day_name()
             
        # finding peak deviation (MAPE)
        n = len(peaks)
        error = 0
        for k in range(n):  
            if peaks[k] == 0:
                print(k)
                continue
            error += (abs(peaks[k] - self.predictions[peak_indexes[k]])/peaks[k])*100
        error = error / n

        return peaks, peak_dates,  peak_indexes, error
        #print(self.data["tstp"].iloc[cursor])