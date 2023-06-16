 
import sys
 
import pytz    # $ pip install pytz
import tzlocal # $ pip install tzlocal
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
from beyond.dates import Date, timedelta
from beyond.io.tle import Tle
from beyond.frames import create_station


tle = Tle("""ISS (ZARYA)
1 25544U 98067A   23166.18443237  .00010989  00000+0  19492-3 0  9994
2 25544  51.6399 338.4530 0005180  82.1865 277.9712 15.50766000401487""").orbit()

azims, elevs = [], []
 
  
local_timezone = tzlocal.get_localzone() 



station = create_station('BPL', (23.2599333, 77.4126149, 495.23))
 
for orb in station.visibility(tle, start=Date(2023, 6, 18, 00, 00, 00), stop=timedelta(hours=24), step=timedelta(seconds=15), events=(True)):

    elev = np.degrees(orb.phi)
    azim = np.degrees(-orb.theta) % 360

    azims.append(azim)
    elevs.append(90 - elev)   

    r = orb.r / 1000.
    
    if orb.event and orb.event.info.startswith('AOS') :
        
        print("         Date         Time          Azim      Elev      Distance   Radial Velocity")
        print("==================================================================================") 
    
    if orb.event and orb.event.info.startswith('AOS') or orb.event and orb.event.info.startswith('LOS') or orb.event and orb.event.info.startswith('MAX')    :
        
        str1 = orb.date.strftime("%m/%d/%Y  %H:%M:%S")
        utc_time = datetime.strptime(str1 , "%m/%d/%Y  %H:%M:%S")
        local_time = utc_time.replace(tzinfo=pytz.utc).astimezone(local_timezone)
          
        _date = local_time.strftime("%m/%d/%Y")
        _time = local_time.strftime("%H:%M:%S")
        
    

        print("{event:7} | {date} | {time}   | {azim:7.2f} | {elev:7.2f} | {r:10.2f} | {orb.r_dot:10.2f}".format(
        orb=orb, r=r,date = _date , time = _time, azim=azim, elev=elev, event=orb.event.info if orb.event is not None else ""
        ))
      
    if orb.event and orb.event.info.startswith("LOS"):
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

        pass
        print("                     ")
        print("                     ") 
        