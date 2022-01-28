# -----------------------------------------------------------
# READING DATASET FROM CSV INTO PANDAS DATAFRAME
#
# Author:
# email:  
# -----------------------------------------------------------

from ast import Raise
import pandas as pd
import numpy as np
import os

# Saving project directory to return cur to directory after file reads
project_directory = os.getcwd()
# Change directory name to the name of the datasetfolder
data_directory = "./data" 

# Dataset directory for daily and halfhourly datasets
daily_dataset_directory = data_directory + "/daily_dataset/daily_dataset/"
halfhourly_dataset_directory = data_directory + "/halfhourly_dataset/halfhourly_dataset/"

# Listing all available files in the different dataset directories
daily_dataset_files = os.listdir(daily_dataset_directory)
halfhourly_dataset_files = os.listdir(halfhourly_dataset_directory)


def load_data_into_dataframe(dataset_option):
    """Returns dataframe for given dataset_option"""
    dataset_files_csv = []

    # Populates the list based on argument
    if dataset_option == "daily":
        dataset_files_csv = daily_dataset_files
        os.chdir(daily_dataset_directory)       # Change to directory to enable reading of csv files
    elif dataset_option == "halfhourly":
        dataset_files_csv = halfhourly_dataset_files
        os.chdir(halfhourly_dataset_directory)  # Change to directory to enable reading of csv files

    # Check if there is actually data in the list before reading to dataframe
    if dataset_files_csv:
        df = pd.concat((pd.read_csv(file) for file in dataset_files_csv))
        os.chdir(project_directory)
    else:
        raise FileNotFoundError(f"No files available for dataset option: '{dataset_option}'")
    return df

if __name__ == "__main__":
    dataframe = load_data_into_dataframe("halfhourly")
    print(dataframe.head())