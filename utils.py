import pytz    
import numpy as np 
import tzlocal 
from datetime import datetime
from beyond.dates import Date, timedelta


local_timezone = tzlocal.get_localzone() 
 
def timeconverter(_time):
    utc_time = datetime.strptime(_time , "%m/%d/%Y  %H:%M:%S")
    local_time = utc_time.replace(tzinfo=pytz.utc).astimezone(local_timezone)
    return local_time


def predictNow(satData , station):

    for orb in station.visibility(satData, start=Date.now(), stop=timedelta(hours=24), step=timedelta(seconds=60), events=True):
        elev = np.degrees(orb.phi)
        # Radians are counterclockwise and azimuth is clockwise
        azim = np.degrees(-orb.theta) % 360
        r = orb.r / 1000
        _datetime = timeconverter(orb.date.strftime("%m/%d/%Y  %H:%M:%S"))        

        _date = _datetime.strftime("%m/%d/%Y")
        _time = _datetime.strftime("%H:%M:%S")
        r = orb.r / 1000.

        if orb.event and orb.event.info.startswith('AOS') or orb.event and orb.event.info.startswith('LOS') or orb.event and orb.event.info.startswith('MAX')    :
            print("{event:7}  {orb.date}  {azim:7.2f}  {elev:7.2f} {r:10.2f} {orb.r_dot:10.2f}".format(
            orb=orb, r=r, azim=azim, elev=elev, event=orb.event.info if orb.event is not None else ""
            ))
        if orb.event and orb.event.info.startswith('LOS'):
            print("\n")

          

