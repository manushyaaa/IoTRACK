import pytz ,sys    
import numpy as np 
import pandas as pd
import tzlocal , json
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
 