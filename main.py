from api import getTLE
from beyond.frames import create_station
from beyond.io.tle import Tle
from beyond.dates import Date  
from utils import checkLatLog , readData ,serialDump
from predict import predictPrecise 
import json

NORAD_ID = 25544
prefix = 'BPL'
latNS = '23.2599333N'
logEW = '77.4126149E'
MSL =  495.23
 
satData = Tle(getTLE(NORAD_ID)).orbit()
latNS , logEW = checkLatLog(latNS , logEW)
station = create_station(prefix, (latNS,  logEW, MSL))

date = Date(2023,6,18,00,00,00)#(YYYY,M,D,HR,MIN,SEC)
duration = 4#in hours 
steps = 1#precise in seconds 

#predictNow(satData , station, plot=False)

# data = predictPrecise( satData ,
#                        station , 
#                        date , 
#                        duration , 
#                        steps , 
#                        plot=False ,
#                        write_to_file=True)  

# print(json.dumps(data , indent=2))
 
serialDump()