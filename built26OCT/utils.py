'''
utils.py
Date: 2021-10-23 13:51:00
Python Version: 3.11.5
Functions: getTLE, getLocation, create_connection , predict , predictPrecise , getPredictedPath
'''

from geopy import Nominatim
import sqlite3
from sqlite3 import Error
import tqdm
import os
from skyfield.api import wgs84, load
import numpy as np
import pandas as pd
import datetime
import time
import pytz
from tabulate import tabulate
from termcolor import colored  # Import the termcolor library for coloring text

OPERATION_DIR = "op"
global SATNAME, LOCATION
ts = load.timescale()
t = ts.now()


def create_connection():
    conn = None
    script_directory = os.path.dirname(os.path.abspath(__file__))
    database_file = 'database.db'
    op_directory_path = os.path.join(script_directory, OPERATION_DIR)
    if not os.path.exists(op_directory_path):
        os.makedirs(op_directory_path)
    database_path = os.path.join(op_directory_path, database_file)

    try:
        conn = sqlite3.connect(database_path)
        return conn
    except Error as e:
        print(e)
    return conn


def getTLE(satName):

    script_directory = os.path.dirname(os.path.abspath(__file__))
  
    op_directory_path = os.path.join(script_directory, OPERATION_DIR)
    if not os.path.exists(op_directory_path):
        os.makedirs(op_directory_path)
    TLE_path = os.path.join(op_directory_path)

    urls = [
        'http://celestrak.org/NORAD/elements/weather.txt',
        'http://celestrak.org/NORAD/elements/amateur.txt',
        'http://celestrak.org/NORAD/elements/cubesat.txt'
    ]

    for url in urls:
        try:
            os.chdir(TLE_path)
            satellites = load.tle_file(url)
            by_name = {sat.name: sat for sat in satellites}
            if satName in by_name:
                return by_name[satName]
        except Exception as e:
            print(f"Error while fetching TLE from {url}: {e}")
    print(f"Satellite '{satName}' not found in any of the provided URLs.")
    return None


def getLocation(_userLocation):
    try:
        geolocator = Nominatim(user_agent="MyApp")
        location = geolocator.geocode(_userLocation)
        lat = round(float(location.latitude), 5)
        lon = round(float(location.longitude), 5)

        return lat, lon
    except Exception as e:
        print('An error occured while retrieving the location : ', e)


def getPredictedPath(GROUP_ID):
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(
                f"SELECT timeUTC from predicted_path WHERE group_id ={GROUP_ID} AND name = 'AOS' ")
            ROW = cursor.fetchone()

            if ROW:
                predictionStartTime = ROW[0]

            cursor.execute(
                f"SELECT timeUTC from predicted_path WHERE group_id ={GROUP_ID} AND name = 'LOS' ")
            ROW = cursor.fetchone()

            if ROW:
                predictionEndTime = ROW[0]

            cursor.execute(
                f"SELECT date from predicted_path WHERE group_id ={GROUP_ID} AND name = 'AOS' ")
            ROW = cursor.fetchone()

            if ROW:
                _date = ROW[0]
            conn.close()
            return predictionStartTime, predictionEndTime, _date
        except Exception as e:
            print(f"An error occurred while getting the predicted path: {e}")
            conn.close()
            return None
    return None


def colorize(val, color):
    return colored(val, color)

def colorize_output(val, color , on_color):
    return colored(val, color , on_color  )

def generatePos():
    t = ts.now()
    satName = 'ISS (ZARYA)'
    location = 'Abode Valley Potheri '

    satellite = getTLE(satName)
    latNS, logEW = getLocation(location)
    bpl = wgs84.latlon(latNS, logEW)

    difference = satellite - bpl
    topocentric = difference.at(t)
    alt, az, distance = topocentric.altaz()

    elev = np.round(alt.degrees, 2)
    azi = np.round(az.degrees, 2)
    return elev, azi
