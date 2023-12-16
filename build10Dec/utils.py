'''
utils.py
Date: 2021-12-10 00:58:00
Python Version: 3.11.5
Description: Utility functions for the satellite tracking system.
'''

from geopy import Nominatim
import sqlite3
from sqlite3 import Error
import tqdm
import os
from skyfield.api import wgs84, load
import numpy as np
import pandas as pd
from datetime import timezone,datetime as dt
import time
import pytz
from tabulate import tabulate
from termcolor import colored  # Import the termcolor library for coloring text
import configparser

global SATNAME, LOCATION
ts = load.timescale()
t = ts.now()

def load_config():
    config = configparser.ConfigParser()
    config.read('G:\\MinorProject\\IoTRACK\\build10Dec\\op\\config.ini')
    return config

OPERATION_DIR = load_config().get('OPERATION', 'operation_dir')

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


def update_tle_data():
    try:
        config = load_config()

        tle_updated_str = config.get('GENERAL', 'TLE_UPDATED')
        tle_updated = dt.strptime(tle_updated_str, "%Y-%m-%d")

        print(tle_updated_str)
        if tle_updated.date() != dt.now().date():
            colorize(print("TLEs are not updated. Updating now..."), "red")
            urls = [
                'http://celestrak.org/NORAD/elements/stations.txt',
                'http://celestrak.org/NORAD/elements/weather.txt',
                'http://celestrak.org/NORAD/elements/amateur.txt',
                'http://celestrak.org/NORAD/elements/cubesat.txt'
            ]

            for url in urls:
                try:
                    os.chdir(os.path.join(os.path.dirname(
                        os.path.abspath(__file__)), OPERATION_DIR))
                    load.tle_file(url)
                except Exception as e:
                    print(f"Error while fetching TLE from {url}: {e}")
 
            config['GENERAL']['TLE_UPDATED'] = dt.now().strftime(
                "%Y-%m-%d")

            with open('config.ini', 'w') as configfile:
                config.write(configfile)
 

            print("TLEs updated successfully.")
        else:
            colorize(print("TLEs last updated on : ", tle_updated_str), "green")
    except Exception as e:
        print(f"Error: {e}")


def getTLE(satName):
    # Ensure TLE data is up-to-date before retrieving
    script_directory = os.path.dirname(os.path.abspath(__file__))

    op_directory_path = os.path.join(script_directory, OPERATION_DIR)
    if not os.path.exists(op_directory_path):
        os.makedirs(op_directory_path)
    TLE_path = os.path.join(op_directory_path)
 

    urls = [
        'http://celestrak.org/NORAD/elements/stations.txt',
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


def generatePos(_satName, _location):
    t = ts.now()

    satellite = getTLE(_satName)
    latNS, logEW = getLocation(_location)
    bpl = wgs84.latlon(latNS, logEW)

    difference = satellite - bpl
    topocentric = difference.at(t)
    alt, az, distance = topocentric.altaz()

    elev = np.round(alt.degrees, 2)
    azi = np.round(az.degrees, 2)
    return elev, azi


def getLocation(_userLocation):
    try:
        geolocator = Nominatim(user_agent="MyApp")
        location = geolocator.geocode(_userLocation)
        lat = round(float(location.latitude), 5)
        lon = round(float(location.longitude), 5)
        return lat, lon
    except Exception as e:
        print('An error occured while retrieving the location : ', e)

def colorize(val, color):
    return colored(val, color)


def colorize_output(val, color, on_color):
    return colored(val, color, on_color)


def remove_space(string):
    return string.replace(" ", "_")


def ignore_lastchar(s):
    return s[:-1]


def checkState(updated_aos_time, aos_time, los_time, updated_los_time):
    current_time = dt.now(timezone.utc)
    for at, lt, uat, ult in zip(aos_time, los_time, updated_aos_time, updated_los_time):
        if current_time < uat:  # wait State
            state = 1
            break
        elif current_time >= uat and current_time < at:  # start State
            state = 2
            break
        elif current_time > at and current_time < lt:   # inside State
            state = 3
            break
        elif current_time >= lt and current_time < ult:  # end State
            state = 4
            break
        else:
            state = 1

    return state


def calculate_movement(initial_position, next_azimuth):
    if next_azimuth >= 180:
        movement_direction = "BCK"
        movement_amount = next_azimuth - initial_position
    else:
        movement_direction = "FWD"
        movement_amount = abs(initial_position - next_azimuth)
    return movement_direction, movement_amount


def reverseDirection(direction):
    if direction == 'FWD':
        return 'BCK'
    elif direction == 'BCK':
        return 'FWD'
