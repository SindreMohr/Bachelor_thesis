
from calendar import month
from data_read import load_data_into_dataframe
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date, datetime


#is giga slow
def find_correlation():
    df = pd.read_csv('./data/ouput.csv')
    df["tstp"] = pd.to_datetime(df["tstp"])

    #space to format datetime values into numeric
    #day string is stored
    df["day"] = df["tstp"].dt.day_name()

    #days =  df["day"].unique()
    #print(days)
    days_dict = {
            'Monday': 1,
            'Tuesday': 2,
            'Wednesday': 3,
            'Thursday': 4,
            'Friday': 5,
            'Saturday': 6,
            'Sunday': 7
        }
    days = []
    weekends = []

    bank_holidays=  pd.read_csv('./data/uk_bank_holidays.csv')
    bank_holidays["Bank holidays"] = pd.to_datetime(bank_holidays["Bank holidays"])


    for _, val in df["tstp"].iteritems():
        name = val.day_name()
        days.append(days_dict[name])
        if name == "Sunday" or name == "Saturday":
            weekends.append(1)
        else:
            weekends.append(0)
        for _, bh in bank_holidays["Bank holidays"].iteritems():
            if val.date() == bh.date():
                weekends[-1] = 1
                #print( weekends[-1])
    df["day"]= pd.Series(days, name="day")
    df["weekend"]= pd.Series(weekends, name="weekend")
    
    #month string is stored
    df["month"] = df["tstp"].dt.month_name()
    #months =  df["month"].unique()
    #print(months)

    months_dict = {
        "January": 1,
        "February": 2,
        "March": 3,
        "April": 4,
        "May": 5,
        "June": 6,
        "July": 7,
        "August": 8,
        "September": 9,
        "October": 10,
        "November": 11,
        "December": 12
    }
    
    for _, val in df["month"].iteritems():
        days.append(months_dict[val])
    df["month"]= pd.Series(days, name="month")

    #print(df)

    df = df.set_index("tstp")
    df["energy(kWh/hh)"] = pd.to_numeric(df["energy(kWh/hh)"], downcast="float", errors="coerce")

    #getting weather data and setting index as datetime
    weather_data = pd.read_csv("./data/weather_hourly_darksky.csv")
    weather_data["time"] = pd.to_datetime(weather_data["time"])
    weather_data = weather_data.set_index("time")


    #attempt at finding houses
    #houses = df["LCLid"].unique()
    #houses = pd.Series(houses, name="house")    
    #hardcoded them instead
    houses = ["MAC000150", "MAC000152", "MAC000153", "MAC000165", "MAC000169", "MAC000168","MAC000159","MAC000173", "MAC000179","MAC000181" ]

    #temp lists for adding to final df
    temp_correlations =  []
    app_temp_correlations = []

    #wind
    wind_bearing_correlations = []
    wind_speed_correlations = []
    
    #time
    day_correlations= []
    month_correlations = []
    weekend_correlations = []

    #for loop init
    count = 0
    for house in houses:
        count += 1
        print(count)
        print(house)
        #finding house and making hourly
        filt = df["LCLid"] == house
        temp_df = df[filt]
        temp_df = temp_df.resample("H").sum()
        # slicing weather data to the same time period as house data
        weather_data_t = weather_data[temp_df.index[0]:temp_df.index[-1]]
        
        #finding various correlations
        temp_correlation = temp_df["energy(kWh/hh)"].corr(weather_data_t["temperature"])
        temp_correlations.append(temp_correlation)
        #print(temp_energy_corr[count-1])

        app_temp_correlation = temp_df["energy(kWh/hh)"].corr(weather_data_t["apparentTemperature"])
        app_temp_correlations.append(app_temp_correlation)

        #wind
        wind_bearing_correlation = temp_df["energy(kWh/hh)"].corr(weather_data_t["windBearing"])
        wind_bearing_correlations.append(wind_bearing_correlation)

        wind_speed_correlation = temp_df["energy(kWh/hh)"].corr(weather_data_t["windSpeed"])
        wind_speed_correlations.append(wind_speed_correlation)

        #day/month correlation
        day_correlation = temp_df["energy(kWh/hh)"].corr(temp_df["day"])
        day_correlations.append(day_correlation)

        weekend_correlation = temp_df["energy(kWh/hh)"].corr(temp_df["weekend"])
        weekend_correlations.append(weekend_correlation)

        month_correlation = temp_df["energy(kWh/hh)"].corr(temp_df["month"])
        month_correlations.append(month_correlation)


        print("done")


    
    #stitching together dataframe to hold correlations
    temp_energy_correlations = pd.Series(data=temp_correlations, name="tempCorr")
    app_temp_correlations = pd.Series(data=app_temp_correlations, name="apparentTempCorr")
    wind_bearing_correlations = pd.Series(data=wind_bearing_correlations, name="windBearingCorr")
    wind_speed_correlations = pd.Series(data=wind_speed_correlations, name="windSpeedCorr")

    day_correlations= pd.Series(data=day_correlations, name="day")
    month_correlations =pd.Series(data=weekend_correlations, name="weekend")
    weekend_correlations = pd.Series(data=month_correlations, name="month")


    houses = pd.Series(name="LCLid", data=houses)

    #making df
    corr_df = pd.merge(houses, temp_energy_correlations, right_index= True, left_index= True)
    corr_df["apparentTempCorr"] = app_temp_correlations
    corr_df["windBearingCorr"] = wind_bearing_correlations
    corr_df["windSpeedCorr"] = wind_speed_correlations
    corr_df["day"] = day_correlations
    corr_df["month"] = month_correlations
    corr_df["weekend"] = weekend_correlations

    #assuming energy is x variable, negative temperature correlation means 
    print(corr_df)     
    return corr_df       

if __name__ == "__main__":
    find_correlation()