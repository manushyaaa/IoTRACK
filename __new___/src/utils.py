from skyfield.api import load
from geopy import Nominatim
import sqlite3
from sqlite3 import Error
 

def create_connection():
    conn = None
    try:
        conn = sqlite3.connect('database.db')  # Replace 'database.db' with your desired database file name
        return conn
    except Error as e:
        print(e)

    return conn

def getTLE(satName):
    try : 
        stations_url = 'http://celestrak.org/NORAD/elements/weather.txt'
        satellites = load.tle_file(stations_url)
    
        by_name = {sat.name: sat for sat in satellites}
        satellite = by_name[satName]
        return satellite
    except Exception as e : 
        print("TLE Fetch Error : " , e)

# def loadTLE(amateur , weather , cubesat , other):
    
#     if amateur : 
#         stations_url = 'http://celestrak.org/NORAD/elements/amateur.txt'
#         satellites = load.tle_file(stations_url)
    

#     if weather : 
#         stations_url = 'http://celestrak.org/NORAD/elements/weather.txt'
#         satellites = load.tle_file(stations_url)

#     if cubesat : 
#         stations_url = 'http://celestrak.org/NORAD/elements/cubesat.txt'
#         satellites = load.tle_file(stations_url)

#     if other : 
#         stations_url = 'G:\MinorProject\IoTRACK\other.txt'
#         satellites = load.tle_file(stations_url)


    
#     pass

def getLocation(_userLocation):

    try : 

        geolocator = Nominatim(user_agent="MyApp")
        location = geolocator.geocode(_userLocation)
        lat = round(float(location.latitude), 5)
        lon = round(float(location.longitude), 5)
         
        return lat , lon

    except Exception as e : 
        print('An error occured while retrieving the location : ',e)



    