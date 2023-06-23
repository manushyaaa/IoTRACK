from api import getTLE
from beyond.frames import create_station
from beyond.io.tle import Tle
from beyond.dates import Date  
from utils import getLocation, check_internet_connection   
from predict import predictNow ,Predict
import json

if check_internet_connection() : 
    print("starting...")
        
    NORAD_ID = 25544

    prefix = 'BPL'
    MSL =  495.23 

    
    latNS , logEW = getLocation("Old Subhash Nagar Bhopal") 
    station = create_station(prefix, (latNS,  logEW, MSL))

    
    satData = Tle(getTLE(NORAD_ID)).orbit()

    
    
    date =   Date(2023, 6, 24, 12, 00, 00, scale="UTC")     #(YYYY,M,D,HR,MIN,SEC)
    duration = 12                        #predict in hours 
    steps = 30                           #precison upto (in seconds)

    #predictNow(satData , station ) # predicts 24hrs 
    Predict(satData ,station)
# data = predictPrecise( satData ,
#                        station , 
#                        date , 
#                        duration , 
#                        steps , 
#                        plot=False ,
#                        write_to_file=True)  

# print(json.dumps(data , indent=2))
 
#serialDump()


#process_data()
else : 
    print("Network connectivity error , pls check your internet connection")