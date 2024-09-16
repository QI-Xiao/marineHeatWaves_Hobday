import pandas as pd
from erddapy import ERDDAP


server_url = "https://coastwatch.pfeg.noaa.gov/erddap/"
dataset_id = "ncdcOisst21Agg_LonPM180"   # "ncdcOisst21Agg"


def get_dataset_info(server, dataset_id):
    e = ERDDAP(server=server)
    e.dataset_id = dataset_id
    print(e.get_info_url())


# get_dataset_info(server_url, dataset_id)


def download_oisst_data(time_start, time_end):
    # Setup ERDDAP server and dataset
    e = ERDDAP(
        server=server_url,
        protocol="griddap"
    )

    # Specify dataset ID
    e.dataset_id = dataset_id

    # Set constraints for time, depth, latitude, and longitude
    e.constraints = {
        "time>=": time_start,
        "time<=": time_end,
        "zlev>=": 0,
        "zlev<=": 0,
        "latitude>=": 18,
        "latitude<=": 31,
        "longitude>=": -98,
        "longitude<=": -80,
    }

    # Specify the fields (variables) to retrieve
    e.variables = ["sst"]

    # Fetch the data in a Pandas DataFrame
    df = e.to_pandas(
        index_col="time (UTC)",
        parse_dates=True,
        skipna=True
    )

    # Clean up and rename columns
    df = df.reset_index()
    df = df.rename(columns={
        "time (UTC)": "t",
        "sst (C)": "temp",
        "longitude (degrees_east)": "lon",
        "latitude (degrees_north)": "lat"
    })

    # Drop rows with missing values
    df = df.dropna()

    return df


result = download_oisst_data('1982-01-01', '1982-01-03')

print(result)