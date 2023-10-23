'''
utils.py
Date: 2021-10-23 13:51:00
Python Version: 3.11.5
Functions: getTLE, getLocation, create_connection , predict , predictPrecise , getPredictedPath
'''

from geopy import Nominatim
import sqlite3
from sqlite3 import Error
import tqdm, os
from skyfield.api import wgs84, load
import numpy as np
import pandas as pd
import datetime, pytz
from tabulate import tabulate

global SATNAME , LOCATION
 

def create_connection():
    conn = None
    try:
        conn = sqlite3.connect('G:\MinorProject\IoTRACK\\built23JUN\op\database.db')  # Replace 'database.db' with your desired database file name
        return conn
    except Error as e:
        print(e)
    return conn
    
def getTLE(satName):
    # Define a list of URLs to check for TLE data
    urls = [
        'http://celestrak.org/NORAD/elements/weather.txt',
        'http://celestrak.org/NORAD/elements/amateur.txt',
        'http://celestrak.org/NORAD/elements/cubesat.txt'
    ]

    # Attempt to load TLE data from each URL
    for url in urls:
        try:
            os.chdir('G:\MinorProject\IoTRACK\\built23JUN\op')
            satellites = load.tle_file(url)
            by_name = {sat.name: sat for sat in satellites}
            if satName in by_name:
                return by_name[satName]
        except Exception as e:
            print(f"Error while fetching TLE from {url}: {e}")

    print(f"Satellite '{satName}' not found in any of the provided URLs.")
    return None

def getLocation(_userLocation):

    try : 

        geolocator = Nominatim(user_agent="MyApp")
        location = geolocator.geocode(_userLocation)
        lat = round(float(location.latitude), 5)
        lon = round(float(location.longitude), 5)
         
        return lat , lon

    except Exception as e : 
        print('An error occured while retrieving the location : ',e)

def getPredictedPath(GROUP_ID):
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()

            cursor.execute(f"SELECT timeUTC from predicted_path WHERE group_id ={GROUP_ID} AND name = 'AOS' ")   
            ROW = cursor.fetchone()

            if ROW : 
                predictionStartTime = ROW[0]

            cursor.execute(f"SELECT timeUTC from predicted_path WHERE group_id ={GROUP_ID} AND name = 'LOS' ")  
            ROW = cursor.fetchone()

            if ROW : 
                predictionEndTime = ROW[0]
            
            cursor.execute(f"SELECT date from predicted_path WHERE group_id ={GROUP_ID} AND name = 'AOS' ")   
            ROW = cursor.fetchone()

            if ROW : 
                _date = ROW[0]

            conn.close()
            return predictionStartTime, predictionEndTime , _date
        except Exception as e:
            print(f"An error occurred while getting the predicted path: {e}")
            conn.close()
            return None
    return None

ts = load.timescale()
t = ts.now()

def predict():
    try:
        # Get user inputs for prediction and call the predict function
        # start_year = int(input("Enter the start year: "))
        # start_month = int(input("Enter the start month: "))
        # start_day = int(input("Enter the start day: "))
        # end_year = int(input("Enter the end year: "))
        # end_month = int(input("Enter the end month: "))
        # end_day = int(input("Enter the end day: "))
        sy = 2023
        sm = 10
        sd = 24
        ey = 2023
        em = 10
        ed = 30
        satName = str(input("Enter the satellite name: "))
        location = input("Enter the location: ")

        global SATNAME 
        SATNAME = satName 

       

        predictedPath = []
        t = ts.now()

        satellite = getTLE(satName)
        latNS, logEW = getLocation(location)
        bpl = wgs84.latlon(latNS, logEW)


        global LOCATION 
        LOCATION = location
        
        difference = satellite - bpl

        predictionStartTime = ts.utc(sy, sm, sd)
        predictionEndTime = ts.utc(ey, em, ed)

        t, events = satellite.find_events(bpl, predictionStartTime, predictionEndTime, altitude_degrees=0)
        event_names = 'AOS', 'MAX', 'LOS'

        group_id = 0
        current_group_id = None

        for (ti, event) in zip(t, events):

            timePath = ti
            topocentric = difference.at(timePath)
            alt, az, distance = topocentric.altaz()

            name = event_names[event]

            if name == 'AOS':
                current_group_id = group_id
                group_id += 1                                                                                                       

            path = {
              
                'group': group_id,
                'name': name,
                'date': ti.utc_strftime('%d-%b-%y'),
                'timeIST': ti.astimezone(pytz.timezone('Asia/Kolkata')).strftime("%H:%M:%S"),
                'timeUTC': ti.astimezone(pytz.timezone('UTC')).strftime("%H:%M:%S"),
                'elev': np.round(alt.degrees, 2),
                'azi': np.round(az.degrees, 2)
            }
            predictedPath.append(path)

        df = pd.DataFrame(predictedPath)

        conn = create_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("DROP TABLE IF EXISTS predicted_path")  # Clear the existing table if it exists
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS predicted_path (

                    group_id INTEGER,
                    name TEXT,
                    date TEXT,
                    timeIST TEXT,
                    timeUTC TEXT,
                    azi REAL,
                    elev REAL
                )
                """
            )  # Create the table to store the predicted path

            for path in predictedPath:
                cursor.execute(
                    """
                    INSERT INTO predicted_path ( group_id, name, date, timeIST , timeUTC, azi, elev)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (                
                        path['group'],
                        path['name'],
                        path['date'],
                        path['timeIST'],
                        path['timeUTC'],
                        path['azi'],
                        path['elev'],
                    ),
                )  # Insert each path into the table

            conn.commit()
            conn.close()
            formatted_df = df[['group', 'name', 'date', 'timeIST', 'timeUTC', 'azi', 'elev']]
            formatted_df.columns = ['Group', 'Event', 'Date', 'TimeIST', 'TimeUTC', 'Azimuth (degrees)', 'Elevation (degrees)']
            formatted_df = formatted_df.set_index('Group')
            table = tabulate(formatted_df, headers='keys', tablefmt='pretty', showindex=True)
            info = f"Satellite Name: {satName}\nLocation: {location}\n"
            print(info)
            print(table)
            
        return df , satName , location
    except Exception as e:
        print("Prediction Error : ", e)
        return pd.DataFrame()  

def predictPrecise():
    try:
        whichGroup = int(input("Enter the group number: "))

        ps , pe , date = getPredictedPath(whichGroup)

        predictionStartTime = datetime.datetime.strptime(ps, '%H:%M:%S')
        predictionEndTime = datetime.datetime.strptime(pe, '%H:%M:%S')
        ps_date_formatted = datetime.datetime.strptime(date, '%d-%b-%y')

        ps_formatted = predictionStartTime.strftime('%H%M%S')
        pe_formatted = predictionEndTime.strftime('%H%M%S')         
        ps_date_formatted = ps_date_formatted.strftime('%Y%m%d')

        pe_start_hour = int(pe_formatted[0:2])
        pe_start_min = int(pe_formatted[2:4])
        pe_start_sec = int(pe_formatted[4:6])

        ps_end_hour = int(ps_formatted[0:2])
        ps_end_min = int(ps_formatted[2:4])
        ps_end_sec = int(ps_formatted[4:6])

        ps_date_year = int(ps_date_formatted[0:4])
        ps_date_month = int(ps_date_formatted[4:6])
        ps_date_day = int(ps_date_formatted[6:8])
        
        print(ps_date_year, ps_date_month, ps_date_day)
        print( ps_end_hour, ps_end_min, ps_end_sec)
        print(pe_start_hour, pe_start_min, pe_start_sec)
        ist_timezone = pytz.timezone('Asia/Kolkata')

        satellite = getTLE(SATNAME)
        latNS, logEW = getLocation(LOCATION) 
        bpl = wgs84.latlon(latNS, logEW )

        difference = satellite - bpl

        predictionEndTime = ts.utc(ps_date_year, ps_date_month, ps_date_day, pe_start_hour, pe_start_min, pe_start_sec)
        predictionStartTime = ts.utc(ps_date_year, ps_date_month,  ps_date_day, ps_end_hour, ps_end_min, ps_end_sec)
            
        interval = 2
        
        current_time = predictionStartTime
        predictedPath = []
        conn = create_connection()
        while current_time.tt <= predictionEndTime.tt:
            ti = current_time
            difference = satellite - bpl
            topocentric = difference.at(ti)
            alt, az, distance = topocentric.altaz()


            if  alt.degrees >= 0 :
                
                ti_ist = ti.astimezone(ist_timezone)
                ist_date = ti_ist.strftime('%d-%b-%y')
                ist_time = ti_ist.strftime('%H:%M:%S')

                path = {
                    'date': ist_date,
                    'timeIST': ist_time,
                    'timeUTC': ti.utc_strftime('%H:%M:%S'),
                    'elev': np.round(az.degrees, 2),
                    'azi': np.round(alt.degrees, 2)
                }

                predictedPath.append(path)

            # Increment the current time by the interval
            current_time += datetime.timedelta(seconds=interval)
    
            
        if conn:
            cursor = conn.cursor()
            cursor.execute("DROP TABLE IF EXISTS precisePredict")  # Clear the existing table if it exists
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS precisePredict (
                
                    date TEXT,
                    timeIST TEXT,
                    timeUTC TEXT,
                    azi REAL,
                    elev REAL
                )
                """
            )  # Create the table to store the predicted path

            for path in predictedPath:
                cursor.execute(
                    """
                    INSERT INTO precisePredict ( date, timeIST ,timeUTC, azi, elev)
                    VALUES ( ?, ?,?, ?, ?)
                    """,
                    (   
                        
                        path['date'],
                        path['timeIST'],
                        path['timeUTC'],
                        path['azi'],
                        path['elev']
                    ),
                )  # Insert each path into the table

            conn.commit()
            conn.close() 

            print("done")
 
    except Exception as e:
        print(f"An error occurred while predicting the path: {e}")
 