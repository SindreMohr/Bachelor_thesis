from data_read import load_data_into_dataframe
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime


#is giga slow
def find_correlation():
    df = load_data_into_dataframe("halfhourly")
    df["tstp"] = pd.to_datetime(df["tstp"])
    df = df.set_index("tstp")
    df["energy(kWh/hh)"] = pd.to_numeric(df["energy(kWh/hh)"], downcast="float", errors="coerce")

    weather_data = pd.read_csv("./data/weather_hourly_darksky.csv")
    weather_data["time"] = pd.to_datetime(weather_data["time"])
    weather_data = weather_data.set_index("time")

    #houses = df["LCLid"].unique()
    #houses = pd.Series(houses, name="house")    

    houses = ["MAC000150", "MAC000152", "MAC000153", "MAC000165", "MAC000169", "MAC000168","MAC000159","MAC000173", "MAC000179","MAC000181" ]

    temp_energy_corr =  []
    count = 0
    for house in houses:
        count += 1
        print(count)
        print(house)
        filt = df["LCLid"] == house
        temp_df = df[filt]
        temp_df = temp_df.resample("H").sum()
        weather_data_f = weather_data[temp_df.index[0]:temp_df.index[-1]]
        correlation = temp_df["energy(kWh/hh)"].corr(weather_data_f["temperature"])
        temp_energy_corr.append(correlation)
        print(temp_energy_corr[0])
    print(temp_energy_corr)

if __name__ == "__main__":
    find_correlation()