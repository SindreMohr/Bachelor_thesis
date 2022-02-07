# -----------------------------------------------------------
# READING DATASET FROM CSV INTO PANDAS DATAFRAME
#
# Author:
# email:  
# -----------------------------------------------------------

import pandas as pd
import os
import time
import datetime


# Saving project directory to return cur to directory after file reads
project_directory = os.getcwd()
# Change directory name to the name of the dataset directory
data_directory = "./data" 

# Dataset directory for daily and halfhourly datasets
daily_dataset_directory = data_directory + "/daily_dataset/daily_dataset/"
halfhourly_dataset_directory = data_directory + "/halfhourly_dataset/halfhourly_dataset/"

# Listing all available files in the different dataset directories
daily_dataset_files = os.listdir(daily_dataset_directory)
halfhourly_dataset_files = os.listdir(halfhourly_dataset_directory)

def unix_time(timestamp):
    values = timestamp.split(" ")
    date = values[0].split("-")
    year = int(date[0])
    month = int(date[1])
    day = int(date[2])
    date = datetime.date(year, month, day)
    clock = values[1].split(":")
    hour = int(clock[0])
    minute = int(clock[1])
    second = int(0)
    clock = datetime.time(hour, minute, second)
    return datetime.datetime.combine(date, clock)

def load_data_into_dataframe(dataset_option):
    """Returns dataframe for given dataset_option"""
    dataset_files_csv = []
    index_opt = ""

    # Populates the list based on argument
    if dataset_option == "daily":
        index_opt = "day"
        dataset_files_csv = daily_dataset_files
        os.chdir(daily_dataset_directory)       # Change to directory to enable reading of csv files
    elif dataset_option == "halfhourly":
        index_opt = "tstp"
        dataset_files_csv = halfhourly_dataset_files
        os.chdir(halfhourly_dataset_directory)  # Change to directory to enable reading of csv files

    # Check if there is actually data in the list before reading to dataframe
    if dataset_files_csv:
        start = time.time()
        if index_opt == "tstp":
            #df = pd.concat((pd.read_csv(file, converters={'tstp': unix_time}) for file in dataset_files_csv), ignore_index=False)
            df = pd.concat((pd.read_csv(file) for file in dataset_files_csv), ignore_index=False)
            #df["tstp"] = df["tstp"].apply(unix_time)
        else:
            df = pd.concat((pd.read_csv(file) for file in dataset_files_csv), ignore_index=False)
        os.chdir(project_directory)
        print(df.head())
        print(start - time.time())
    else:
        raise FileNotFoundError(f"No files available for dataset option: '{dataset_option}'")
    
    return df

if __name__ == '__main__':
    load_data_into_dataframe("halfhourly")