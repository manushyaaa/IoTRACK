import pytz ,sys , time , socket
import numpy as np 
import pandas as pd
import tzlocal , json
from datetime import datetime 
import matplotlib.pyplot as plt
from geopy.geocoders import Nominatim

azims = []
elevs = []
predictedpath = []
local_timezone = tzlocal.get_localzone() 
 
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
 

def timeconverter(_time):
    try : 
        utc_time = datetime.strptime(_time , "%m/%d/%Y  %H:%M:%S")
        local_time = utc_time.replace(tzinfo=pytz.utc).astimezone(local_timezone)
        return local_time
    except Exception as e : 
        print('An Error occured while converting time', e)
        return None


#for plotting polar charts 

def plotPolar(_azims , _elevs):
    plt.figure()
    ax = plt.subplot(111, projection='polar')   
    ax.set_theta_direction(-1)
    ax.set_theta_zero_location('N')
    plt.plot(np.radians(_azims), _elevs, '.')
    ax.set_yticks(range(0, 90, 20))  
    ax.set_yticklabels(map(str, range(90, 0, -20)))
    ax.set_rmax(90)   
    
    if "no-display" not in sys.argv:
        plt.show()
    azims.clear()
    elevs.clear()


#for real-time prediction
 
def readData():
    data = pd.read_excel('data/predictedPath.xlsx', index_col=0) 
    for index, row in data.iterrows():
    # Access each column value for the current row
        column1_value = row['group']
        column2_value = row['event']
        column3_value = row['date']
        column4_value = row['time']
        column5_value = row['azim']
        column6_value = row['elev']

        # Process the data as desired
        print(f'Row {index}: Column1={column1_value}, Column2={column2_value}, Column3={column3_value}Column4={column4_value}, Column5={column5_value}, Column6={column6_value} Column7={column5_value}, Column8={column6_value}')
   

def serialDump():
  
    df=pd.read_excel('G:\STS\data\predictedPath.xlsx')    
    df['time'] = pd.to_datetime(df['time'])
    while True:
        
        current_time =datetime.now().strftime('%H:%M:%S') 
        filtered_df = df[df['time'].dt.strftime('%H:%M:%S') == current_time]

        if not filtered_df.empty:
            columns_to_print = ['group', 'time', 'azim' , 'elev']  # Modify with the actual column names you want to print
            print('{_current_time} {data}'.format(_current_time = current_time , data = filtered_df.loc[:, columns_to_print].to_string(index=False, header=False)))
        time.sleep(1)

def process_data():
    df=pd.read_excel('G:\STS\data\predictedPath.xlsx')    
    df['time'] = pd.to_datetime(df['time'])

    while True:
        current_time = datetime.now().strftime('%H:%M:%S')
        filtered_df = df[df['time'].dt.strftime('%H:%M:%S') == current_time]

        if not filtered_df.empty:
            for index,row in filtered_df.iterrows():
                group = row[0]
                time_value = row[4]
                azim = row[5]
                elev = row[6]
                print(f'{time_value} {group} {azim} {elev}')
        time.sleep(1)


def checkLatLog(latNS , logEW):

    if (latNS[len(latNS)-1] =='S'):
        latNS = ''.join(('-',latNS)) 
    
    if (logEW[len(logEW)-1] == 'W' ):
        logEW = ''.join(('-',logEW))
    
    _lat = latNS[:-1]
    _log = logEW[:-1]

    return float(_lat) , float(_log) 

def generateTabularJSON(data):

    data_list = json.loads(data)
    column_name = list(data_list[0].keys())
    print('\t'.join(column_name))
    for item in data_list : 
        print('\t'.join(str(item[column]) for column in column_name))
 

def check_internet_connection():
    try:
        # Attempt to connect to a reliable website
        socket.create_connection(("www.google.com", 80))
        return True
    except OSError:
        return False

 