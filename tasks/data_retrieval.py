"""
This file covers the first part of getting the data for the west-nile project.

Mosquito trap data is retrieved from the CoC's Open Data API, but weather data and spray data
was just retrieved manually. Static copies of the data are then stored in the `data/` directory
to ensure the same data is used for all runs of the project.
"""

import pandas as pd
import time
import glob

from sodapy import Socrata

# TODO: Pull new data from API and see how results differ.
# TODO: Check if data format changes. API states that data may be formatted differently in the
# future.

# Define client to access the City of Chicago's Open Data API
client = Socrata("data.cityofchicago.org", None)

# Get data from API, limit of first 50k records (returned as a list of dictionaries)
# String parameter is the dataset identifier based on the URL
# https://data.cityofchicago.org/Health-Human-Services/West-Nile-Virus-WNV-Mosquito-Test-Results/jqe8-8r6s/about_data
results = client.get("jqe8-8r6s", limit=50000)

# Convert to pandas DataFrame
results_df = pd.DataFrame.from_records(results)

# Having issues with weather data beyond 2014, so data is limited to before 2015
results_df["date"] = pd.to_datetime(results_df["date"])
results_df = results_df[results_df["date"] < "2015-01-01"]

# For convienence, save a static copy (to ensure data stays the same throughout my work on this
# project). But ideally, it would be best to automatically pull the latest data from the API.
results_df.to_pickle("../data/mosquito_data.pkl")


# Converting weather and spray data, downloaded manually, to pickle format for easier access later.
# TODO: Get more updated weather and spray data, as these are static copies (e.g. using API)
weather_df = pd.read_csv("weather.csv")
weather_df.to_pickle("../data/weather.pkl")

spray_df = pd.read_csv("spray.csv")
spray_df.to_pickle("../data/spray.pkl")
