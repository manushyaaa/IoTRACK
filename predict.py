import pytz ,sys    
import numpy as np 
import pandas as pd
import tzlocal , json
from datetime import datetime
from beyond.dates import Date, timedelta 
from utils import timeconverter,plotPolar

azims = []
elevs = []
predictedpath = []
local_timezone = tzlocal.get_localzone() 

def predictNow(satData , station, plot):
    
    azims = []
    elevs = []

    for orb in station.visibility(satData, start=Date.now(), stop=timedelta(hours=12), step=timedelta(seconds=60), events=True):
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
        


# #for detailed predictions for serial data input 
def predictPrecise(satData, station, date, duration, steps, plot , write_to_file):
    azims = []
    elevs = []
    group_id = 1
    current_group_id = None

    for orb in station.visibility(satData, start=date, stop=timedelta(hours=duration), step=timedelta(seconds=steps), events=True):
        elev = np.degrees(orb.phi)
        azim = np.degrees(-orb.theta) % 360

        azim = np.round(azim, 2)
        elev = np.round(elev, 2)

        _datetime = timeconverter(orb.date.strftime("%m/%d/%Y %H:%M:%S"))
        _date = _datetime.strftime("%m/%d/%Y")
        _time = _datetime.strftime("%H:%M:%S")

        r = orb.r / 1000.
        r = np.round(r , 2)
        orb.r_dot = np.round(orb.r_dot , 2)

        if orb.event is not None and orb.event.info.startswith('AOS'):
            current_group_id = group_id
            group_id += 1

        path = {
                "group": current_group_id,
                "event": orb.event.info if orb.event is not None else "",
                "date": _date,
                "time": _time,
                "azim": azim ,
                "elev": elev,
                "distance": r ,
                "radialvelocity":(orb.r_dot)                  
        }

        azims.append(azim)
        elevs.append(90 - elev)
        predictedpath.append(path)
 
        if plot==True :    
            plotPolar(azims , elevs)
        if write_to_file==True :    
            df = pd.DataFrame(predictedpath) 
            df.to_excel("output.xlsx")  
    return predictedpath
 

     