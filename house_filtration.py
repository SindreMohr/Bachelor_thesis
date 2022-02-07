import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

from data_read import load_data_into_dataframe


def house_filtration_select(house_select="ACORN-E", num=10):
    '''
    House filtration
    Filters based on:
    - house_select: The type of houses to select
    - num: Number of houses to select from (most data, to least)
    Default values:
    - house_select: ACORN-E
    - num: 10
    Returns filtered dataframe
    '''

    # Loading data
    h_df = load_data_into_dataframe("halfhourly")
    hhi_df = pd.read_csv("./data/informations_households.csv")

    acorn_e_filter = hhi_df["Acorn"] == house_select
    acorn_e_hh = hhi_df[acorn_e_filter]

    LCLid_filter = h_df["LCLid"].isin(acorn_e_hh["LCLid"])

    # filtering based on LCLid
    house_datacount = h_df[LCLid_filter]

    # Retrieve id of the NUM most measured houses
    house_datacount_most_data = house_datacount["LCLid"].value_counts().iloc[0:num].index.tolist()
    
    # filter data again based on those ids
    n_households_filter =h_df["LCLid"].isin(house_datacount_most_data)
    filtered_hh_data = h_df[n_households_filter]

    print(filtered_hh_data["LCLid"].unique())

    return filtered_hh_data

