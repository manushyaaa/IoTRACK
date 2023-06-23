import numpy as np
import pandas as pd
import tzlocal , json
from datetime import datetime
from beyond.dates import Date, timedelta
from utils import timeconverter, plotPolar , generateTabularJSON

 
predictedpath = []
predictedpathprecision = []
local_timezone = tzlocal.get_localzone()


def predictNow(satData, station ):

    try : 
        predictedpath.clear()
        azims = []
        elevs = []
        group_id = 0
        current_group_id = None

        for orb in station.visibility(satData, start=Date.now(), stop=timedelta(hours=12), step=timedelta(seconds=120),
                                    events=True):
            
            elev = np.degrees(orb.phi)
            azim = np.degrees(-orb.theta) % 360

            elev = np.round(elev , 2)
            azim = np.round(azim , 2)

            _datetime = timeconverter(orb.date.strftime("%m/%d/%Y  %H:%M:%S"))
            _date = _datetime.strftime("%m/%d/%Y")
            _time = _datetime.strftime("%H:%M:%S")
            
            azims.append(azim)
            elevs.append(90 - elev)

            if orb.event and orb.event.info.startswith('AOS') or orb.event and orb.event.info.startswith(
                    'LOS') or orb.event and orb.event.info.startswith('MAX'):
                
                        if orb.event is not None and orb.event.info.startswith('AOS'):
                            current_group_id = group_id
                            group_id += 1

                        path = {
                            "group": group_id,
                            "event": orb.event.info if orb.event is not None else "",
                            "date": _date,
                            "time": _time,
                            "azim": azim,
                            "elev": elev
                        }

 
                        predictedpath.append(path)

                        #print(json.dumps( predictedpath , indent = 1))

                        # print("{event:7}  {date} {time}  {azim:7.2f}  {elev:7.2f}  ".format(
                        #     orb=orb, date=_date, time=_time, azim=azim, elev=elev,
                        #     event=orb.event.info if orb.event is not None else ""
                        # ))

        print("group\tevent\tdate\ttime\t\tazim\telev")
        for path in predictedpath:
            print("{group}\t\t{event}\t{date}\t{time}\t{azim}\t{elev}".format(**path))

 
        # selectGroup = int(input('select groupID: '))
        # azims = []
        # elevs = []

        # for path in predictedpath:
        #     if path["group"] == selectGroup:
        #         azims.append(path["azim"])
        #         elevs.append(90 - path["elev"])

        # plotPolar(azims, elevs)
        selectGroup = int(input("Produce tracking data ? Enter groupID : "))
        
        for path in predictedpath:
            if path["group"] == selectGroup:
                if path['event'] == 'AOS':
                    _ptime = path['time']
                    _pdate = path['date']
                    
                    # Extracting hour, minute, and second from _ptime
                    hour, minute, second = map(int, _ptime.split(':'))
                    
                    # Extracting day, month, and year from _pdate
                    month, day, year = map(int, _pdate.split('/'))
                    
                    # Reducing the hour by one
                    hour -= 1
                    minute = 0
                    second = 0
                    if hour < 0:
                        # If the hour becomes negative, adjust the date accordingly
                        hour += 24
                        formatted_date = Date(year, month, day - 1, hour, minute, second)
                    else:
                        formatted_date = Date( year, month, day, hour, minute, second)
                    
                    datetime_str = f"{_pdate} {_ptime}"
                    datetime_obj = datetime.strptime(datetime_str, "%m/%d/%Y %H:%M:%S")

                    print(datetime_obj)

                    print(formatted_date)
                            
                    print("Running precision predict ... pls wait ")
                    Predict(satData , station)

        
    except Exception as e : 
        print("Prediction Error : " , e)
    

      
def Predict(satData ,station): 
    group_id = 1
    current_group_id = None
    for orb in station.visibility(satData, start=Date(2023, 6, 24, 1, 00, 00), stop=timedelta(hours=2), step=timedelta(seconds=1),
                                events=True):
        elev = np.degrees(orb.phi)
        azim = np.degrees(-orb.theta) % 360

        azim = np.round(azim, 2)
        elev = np.round(elev, 2)

        _datetime = timeconverter(orb.date.strftime("%m/%d/%Y %H:%M:%S"))
        _date = _datetime.strftime("%m/%d/%Y")
        _time = _datetime.strftime("%H:%M:%S")

        r = orb.r / 1000.
        r = np.round(r, 2)
        orb.r_dot = np.round(orb.r_dot, 2)

        if orb.event is not None and orb.event.info.startswith('AOS'):
            current_group_id = group_id
            group_id += 1

        path = {
            "group": group_id,
            "event": orb.event.info if orb.event is not None else "",
            "date": _date,
            "time": _time,
            "azim": azim,
            "elev": elev,
            "distance": r,
            "radial-velocity": orb.r_dot
        }
 
        predictedpathprecision.append(path)

    print("Prediction Completed , writing ...")

    df = pd.DataFrame(predictedpathprecision)
    df.to_excel("G:\STS\data\predictedPath.xlsx")
        
    print("Done ...")