import numpy as np
import pandas as pd
from geotracker.utils import Utils


def get_circle_centers_radius(
    spacing,
    top_left=(52.635010, 13.198130),
    bottom_right=(52.39405827510934, 13.596147274545292),
) -> tuple:
    """
    Wrapper around the utils function get_circlegrid_list.
    Has Berlins top_left and bottom_right coordinates already coded in

    Returns a list of center coordinates and one radius in meters and one in
    degrees in order to allow us to check for whether coordinates are in the
    circle.
    Meters = for showing to users, because easy to interpret
    Degrees = necessary for calculations
    """
    # Top left and bottom right of a square covering the entiretty of Berlin

    #  get a number of cirlces with the specified spacing.
    center_coords, mradius, degradius = Utils().get_circlegrid_list(
        top_left, bottom_right, spacing, 1.2
    )


    return center_coords, mradius, degradius


def is_restaurant_in_circle(observation, center_lat, center_lon, degradius) -> bool:
    """
    Takes as an input one row of a dataframe and returns boolean indicating
    whether a restaurant falls into a circle specified center coordinates and the
    circle's radius in degrees.
    """

    obs_lat = observation["lat"]
    obs_lon = observation["lon"]

    return (obs_lat-center_lat)**2 + (obs_lon-center_lon)**2 <= degradius**2


def restaurants_in_circle(df, center_lat, center_lon, degradius) -> pd.DataFrame:
    """
    Takes as an input a dataframe and returns a dataframe of observations which
    fall into the circle
    """

    df_in_circle = df[(df["latitude"]-center_lat)**2 + (df["longitude"]-center_lon)**2 <= degradius**2]

    return df_in_circle



def calculate_circle_weights(restaurants_df, good_review_threshold=2.5):
    """
    For a data frame of restaurants that fall into a circle, this returns
    a weight for the circle which is a count of "good" restaurants.
    Good restaurants are restaurants whose average review score exceeds
    good_review_threshold
    """

    return restaurants_df[restaurants_df.avg_review_score > good_review_threshold].sum()
