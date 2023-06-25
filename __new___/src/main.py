from skyfield.api import wgs84 ,load
import numpy as np
from datetime import datetime, timedelta
from utils import getTLE,getLocation

  
satellite = getTLE('ISS (ZARYA)')
latNS , logEW = getLocation('Old Subhash Nagar')


bpl = wgs84.latlon(latNS, logEW)
ts = load.timescale()
t = ts.now()

difference = satellite - bpl
topocentric = difference.at(t)
steps = 60 #seconds

predictionStartTime= ts.utc(2023, 6, 25)
predictionEndTime = ts.utc(2023, 6, 26)


t , events  = satellite.find_events(bpl, predictionStartTime, predictionEndTime , altitude_degrees=0)
event_names = 'AOS', 'MAX', 'LOS'

startTime = None 
endTime = None



for (ti, event) in zip(t, events):
    timePath = ti
    topocentric = difference.at(timePath)
    alt, az, distance = topocentric.altaz()

    name = event_names[event]
    
    print(name, ti.utc_strftime('%d-%b-%y %H:%M:%S'), np.round(alt.degrees, 2), np.round(az.degrees, 2))

    if event == 0 and startTime is None: 
        startTime = ti 
    if event == 2 and endTime is None: 
        endTime = ti 

    if startTime is not None and endTime is not None:
        break 


time_interval = timedelta(seconds=5) 
current_time = startTime 

while current_time.utc_datetime() <= endTime.utc_datetime()  : 
    #print(current_time.utc_strftime("%Y-%m-%d %H:%M:%S") )
    timePath = current_time
    topocentric = difference.at(timePath)
    alt, az, distance = topocentric.altaz()
    print( current_time.utc_strftime('%d-%b-%y %H:%M:%S'), np.round(alt.degrees, 2), np.round(az.degrees, 2))    
    
    current_time += time_interval