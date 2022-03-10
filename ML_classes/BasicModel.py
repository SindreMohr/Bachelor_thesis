from operator import mod
from textwrap import indent
from typing_extensions import Self
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class Baseline():
   def __init__(self, data: pd.DataFrame, Y_var: str, train_test_split=0):
        self.data = data 
        self.Y_var = Y_var
        self.train_test_split = train_test_split
        # Extracting the main variable we want to model/forecast
        self.y = data[Y_var].tolist()


   def predictions(self):
       predictions = self.y[0:len(self.y)-2]
       predictions.insert(0,self.y[0])

       return predictions

   def test_predictions(self):
       index = round(len(self.y) * self.train_test_split)
       predictions = self.y[index:len(self.y)-2]
       predictions.insert(0,self.y[0])

       return predictions

   def predict_n_ahead(self,n):
       predictions = []
       for _ in range(n):
           predictions.append(self.y[-1])
       return predictions


















if __name__ == "__main__":
    df = pd.read_csv('./data/ouput.csv')
    df['tstp'] = [datetime.strptime(x, '%Y-%m-%d %H:%M:%S') for x in df['tstp']]
    #df["tstp"] = pd.to_datetime(df["tstp"])
    df["energy(kWh/hh)"] = pd.to_numeric(df["energy(kWh/hh)"], downcast="float", errors="coerce")

    max_value_energy = df["energy(kWh/hh)"].max()
    max_value_energy = df["energy(kWh/hh)"].max()
    df['energy(kWh/hh)'] = df['energy(kWh/hh)'].apply(lambda x: x / max_value_energy)
    # Sorting the values
    df.sort_values('tstp', inplace=True)

    lclid_list = df['LCLid'].unique()
    def find_household(identification):
        affluenthh_filt = df["LCLid"] == identification
        affluent_hh_data = df[affluenthh_filt]
        return affluent_hh_data

    hh = find_household("MAC000150")
    hh.pop("LCLid")
    hh = hh.set_index("tstp")
    hh = hh.resample("H").sum()
    hh = hh.reset_index()



    bs = Baseline(data=hh, Y_var="energy(kWh/hh)",train_test_split=0.15)
    print(bs.predictions())