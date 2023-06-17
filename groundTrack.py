 
import sys 
import pytz    # $ pip install pytz
import tzlocal # $ pip install tzlocal
from datetime import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from beyond.dates import Date, timedelta
from beyond.io.tle import Tle
from beyond.frames import create_station

TWO_LINE_ELEMENT = """ISS (ZARYA)
1 25544U 98067A   23166.52504001  .00012512  00000+0  22070-3 0  9999
2 25544  51.6424 336.7579 0005373  84.9405  18.0183 15.50777566401535"""


tle = Tle(TWO_LINE_ELEMENT).orbit()

azims, elevs = [], []  
local_timezone = tzlocal.get_localzone() 

#N E ---> +
#W S ---> -

lat1NS = -34.6226
log1EW = -58.3902
MSL1 = 100 

counter = 0 
predictedpath = []

station = create_station('BPL', (23.2599333, 77.4126149, 495.23))
station2 = create_station('ISL', (lat1NS,  log1EW, MSL1))
 
for orb in station.visibility(tle, start=Date(2023, 6, 18, 00, 00, 00), stop=timedelta(hours=1), step=timedelta(seconds=7), events=(True)):

    elev = np.degrees(orb.phi)
    azim = np.degrees(-orb.theta) % 360
    azims.append(azim)
    elevs.append(90 - elev)   
    r = orb.r / 1000.
    
    str1 = orb.date.strftime("%m/%d/%Y  %H:%M:%S")
    utc_time = datetime.strptime(str1 , "%m/%d/%Y  %H:%M:%S")
    local_time = utc_time.replace(tzinfo=pytz.utc).astimezone(local_timezone)
    
    _date = local_time.strftime("%m/%d/%Y")
    _time = local_time.strftime("%H:%M:%S")

    
    #---FOR UTC -----------------------------
    # _date = orb.date.strftime("%m/%d/%Y")  |
    # _time = orb.date.strftime("%H:%M:%S")  |
    #----------------------------------------

    path = {
        "event" :  orb.event.info if orb.event is not None else "",
        "date" : _date , 
        "time" :_time,
        "azim":azim, 
        "elev":elev ,
        "distance" : r , 
        "radialvelocity" :orb.r_dot 
    }         
    
    predictedpath.append(path)

df = pd.DataFrame(predictedpath) 
 
# Grouping the given data into a csv file
grouped_data = []
group_start = 0
group_id = 0

for i in range(len(df)):
    event = df.loc[i, 'event']
    
    if event == 'AOS':
        group_end = i
        
        if group_start != group_end:
            # Extract the data between start and end indices
            group_data = df.loc[group_start:group_end-1].copy()
            group_data.loc[:, 'group_id'] = group_id
            grouped_data.append(group_data)
        
        # Start a new group
        group_start = i
        group_id += 1

# Check if there is remaining data after the last group start
if group_start < len(df):
    group_data = df.loc[group_start:].copy()
    group_data.loc[:, 'group_id'] = group_id
    grouped_data.append(group_data)

# Print the grouped data with a unique identifier for each group
for group in grouped_data:
    print(f"Group ID: {group['group_id'].iloc[0]}")
    print(group)
    print()

#Writing
grouped_df = pd.concat(grouped_data)
grouped_df.to_csv("predictedPath.csv", sep='\t', index=False)
            
            # plt.figure()
            # ax = plt.subplot(224, projection='polar')   
            # ax.set_theta_direction(-1)
            # ax.set_theta_zero_location('N')
            # plt.plot(np.radians(azims), elevs, '.')
            # ax.set_yticks(range(0, 90, 20))
            # ax.set_yticklabels(map(str, range(90, 0, -20)))
            # ax.set_rmax(90)   
            
            # if "no-display" not in sys.argv:
            #     plt.show()
            # azims.clear()
            # elevs.clear()
