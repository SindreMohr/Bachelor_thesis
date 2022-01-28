# -----------------------------------------------------------
# PREPROCESSING DATAFRAME
#
# Author:
# email:  
# -----------------------------------------------------------

from data_read import load_data_into_dataframe
import pandas as pd


def data_preprocessing(dataset_option, drop_row=True):
    """
    Preprocessing data in dataframe from specified dataset, and dropping empty rows based on input
    TODO:
        [ ] Missing Values 
        [ ] Data Standardization
        [ ] Data Normalization
        [ ] Data binning
    """
    df = load_data_into_dataframe(dataset_option)

    # Checking for empty cells
    missing_values = df.isna().sum()                            # Counts number of empty cells
    missing_values_percentage = missing_values/len(df)*100      # Percentage of cells empty

    if drop_row:
        df.dropna(axis=0, inplace=True)                         # Removing rows with missing data
    elif not drop_row:
        pass # Interpolating?

if __name__ == "__main__":
    data_preprocessing("daily")
