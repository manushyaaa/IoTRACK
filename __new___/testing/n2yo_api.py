import requests 
from geopy.geocoders import Nominatim
from datetime import datetime

API_KEY = 'L4VF35-H3JFP4-6WRCWN-51V8'
NORAD_ID = 25544
def generateTabularJSON(data):

    data_list = json.loads(data)
    column_name = list(data_list[0].keys())
    print('\t'.join(column_name))
    for item in data_list : 
        print('\t'.join(str(item[column]) for column in column_name))
 

def getLocation(_userLocation):
    try : 
        geolocator = Nominatim(user_agent="MyApp")
        location = geolocator.geocode(_userLocation)
        lat = round(float(location.latitude), 5)
        lon = round(float(location.longitude), 5)
        return lat,lon
    
    except Exception as e : 
        print('An error occured while retrieving the location : ',e)
        return None 
 
observer_lat , observer_lng = getLocation('Old Subhash Nagar , Bhopal')
MSL =  495.23 

def getTLE(NORAD_ID):
    try : 
        urls = f'https://api.n2yo.com/rest/v1/satellite/tle/{NORAD_ID}&apiKey={API_KEY}'
        header = {
                'User-Agent': '...',
                'referer': 'https://...'
        }

        tle = requests.get(url=urls, headers=header)
         
        return tle.json() 
    except Exception as e : 
        print('TLE fetch error : ' , e)

 


def getRadioPasses(NORAD_ID, observer_lat, observer_lng, MSL, API_KEY):
    try:
        urls = f'https://api.n2yo.com/rest/v1/satellite/radiopasses/{NORAD_ID}/{observer_lat}/{observer_lng}/{MSL}/{1}/{1}&apiKey={API_KEY}'
        header = {
            'User-Agent': '...',
            'referer': 'https://...'
        }
        
        radioPasses = requests.get(url=urls, headers=header)
        passes_data = radioPasses.json()
        
        # Convert UTC timestamps to readable format
        for passage in passes_data['passes']:
            passage['startUTC'] = datetime.utcfromtimestamp(passage['startUTC']).strftime('%Y-%m-%d %H:%M:%S')
            passage['maxUTC'] = datetime.utcfromtimestamp(passage['maxUTC']).strftime('%Y-%m-%d %H:%M:%S')
            passage['endUTC'] = datetime.utcfromtimestamp(passage['endUTC']).strftime('%Y-%m-%d %H:%M:%S')
        
        return passes_data
    except Exception as e:
        print('TLE fetch error:', e)

from prettytable import PrettyTable

passes_data = getRadioPasses(NORAD_ID, observer_lat, observer_lng, MSL, API_KEY)

table = PrettyTable()
table.field_names = ['AOS', 'MAX', 'LOS', 'Start Azimuth', 'Max Azimuth', 'Max Elevation', 'End Azimuth']

for passage in passes_data['passes']:
    table.add_row([
        passage['startUTC'],
        passage['maxUTC'],
        passage['endUTC'],
        f"{passage['startAz']} ({passage['startAzCompass']})",
        f"{passage['maxAz']} ({passage['maxAzCompass']})",
        passage['maxEl'],
        f"{passage['endAz']} ({passage['endAzCompass']})"
    ])

print(table)
