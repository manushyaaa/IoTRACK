from api import getTLE
from beyond.frames import create_station
from beyond.io.tle import Tle
from utils import predictNow

NORAD_ID = 25544
prefix = 'BPL'
latNS = 23.2599333
logEW = 77.4126149
MSL =  495.23
azims, elevs = [], []  

satData = Tle(getTLE(NORAD_ID)).orbit()
station = create_station(prefix, (latNS,  logEW, MSL))

predictNow(satData , station)



 