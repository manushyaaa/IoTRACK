from skyfield.api import load
from geopy import Nominatim

def getTLE(satName):
    try : 
        stations_url = 'http://celestrak.org/NORAD/elements/stations.txt'
        satellites = load.tle_file(stations_url)
    
        by_name = {sat.name: sat for sat in satellites}
        satellite = by_name[satName]
        return satellite
    except Exception as e : 
        print("TLE Fetch Error : " , e)

def getLocation(_userLocation):

    try : 

        geolocator = Nominatim(user_agent="MyApp")
        location = geolocator.geocode(_userLocation)
        lat = round(float(location.latitude), 5)
        lon = round(float(location.longitude), 5)
         
        return lat , lon

    except Exception as e : 
        print('An error occured while retrieving the location : ',e)


 
    