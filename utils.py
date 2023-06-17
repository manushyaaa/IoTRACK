import pytz ,sys    
import numpy as np 
import pandas as pd
import tzlocal 
from datetime import datetime
from beyond.dates import Date, timedelta
import matplotlib.pyplot as plt

azims = []
elevs = []
predictedpath = []
local_timezone = tzlocal.get_localzone() 

def checkLatLog(latNS , logEW):

    if (latNS[len(latNS)-1] =='S'):
        latNS = ''.join(('-',latNS)) 
    
    if (logEW[len(logEW)-1] == 'W' ):
        logEW = ''.join(('-',logEW))
    
    _lat = latNS[:-1]
    _log = logEW[:-1]

    return float(_lat) , float(_log) 
 
def timeconverter(_time):
    utc_time = datetime.strptime(_time , "%m/%d/%Y  %H:%M:%S")
    local_time = utc_time.replace(tzinfo=pytz.utc).astimezone(local_timezone)
    return local_time


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
def predictNow(satData , station, plot):
     
    for orb in station.visibility(satData, start=Date.now(), stop=timedelta(hours=6), step=timedelta(seconds=60), events=True):
        elev = np.degrees(orb.phi)
        # Radians are counterclockwise and azimuth is clockwise
        azim = np.degrees(-orb.theta) % 360
         
        _datetime = timeconverter(orb.date.strftime("%m/%d/%Y  %H:%M:%S"))        
        _date = _datetime.strftime("%m/%d/%Y")
        _time = _datetime.strftime("%H:%M:%S")
        r = orb.r / 1000.
        azims.append(azim)
        elevs.append(90 - elev) 
        if orb.event and orb.event.info.startswith('AOS') or orb.event and orb.event.info.startswith('LOS') or orb.event and orb.event.info.startswith('MAX')    :
            print("{event:7}  {date} {time}  {azim:7.2f}  {elev:7.2f} {r:10.2f} {orb.r_dot:10.2f}".format(
            orb=orb, r=r, date = _date, time =_time ,azim=azim, elev=elev, event=orb.event.info if orb.event is not None else ""
            ))
        if orb.event and orb.event.info.startswith('LOS'):
            print("\n")
    if plot==True :    
        plotPolar(azims , elevs)
        
#for detailed predictions for serial data input 
def predictPrecise(satData , station, date , duration , steps , plot):
     
    for orb in station.visibility(satData, start=date, stop=timedelta(hours=duration), step=timedelta(seconds=steps), events=True):
        elev = np.degrees(orb.phi)
        # Radians are counterclockwise and azimuth is clockwise
        azim = np.degrees(-orb.theta) % 360
         
        _datetime = timeconverter(orb.date.strftime("%m/%d/%Y  %H:%M:%S"))        
        _date = _datetime.strftime("%m/%d/%Y")
        _time = _datetime.strftime("%H:%M:%S")
        r = orb.r / 1000.
        azims.append(azim)
        elevs.append(90 - elev) 
 
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
    
    if plot==True :    
        plotPolar(azims , elevs)
