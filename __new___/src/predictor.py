from utils import getTLE, getLocation ,create_connection
from skyfield.api import wgs84 ,load
import numpy as np

ts = load.timescale()
def predict(sy , sm , sd , ey , em , ed , satName , location ):

    try :
        predictedPath = []
        t = ts.now()
    
        satellite = getTLE(satName)
        latNS, logEW = getLocation(location)
        #bpl = wgs84.latlon(23.24871118985121, 77.43505588150911)
        bpl = wgs84.latlon(latNS , logEW)


        difference = satellite - bpl

        predictionStartTime=  ts.utc(sy , sm, sd)
        predictionEndTime = ts.utc( ey , em , ed)


        t , events  = satellite.find_events(bpl, predictionStartTime, predictionEndTime , altitude_degrees=0)
        event_names = 'AOS', 'MAX', 'LOS'


        group_id = 0
        current_group_id = None

        for (ti, event) in zip(t, events):

            timePath = ti
            topocentric = difference.at(timePath)
            alt, az, distance = topocentric.altaz()

            name = event_names[event]

        

            if name == 'AOS':
                current_group_id = group_id
                group_id += 1

            path = {
                'group' : group_id,
                'name' : name , 
                'date' : ti.utc_strftime('%d-%b-%y'),
                'time' : ti.utc_strftime('%H:%M:%S'),
                'azi' :  np.round(alt.degrees, 2),
                'elev' : np.round(az.degrees, 2)
            }
            predictedPath.append(path)
            conn = create_connection()
            if conn:
                cursor = conn.cursor()
                cursor.execute("DROP TABLE IF EXISTS predicted_path")  # Clear the existing table if it exists
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS predicted_path (
                        group_id INTEGER,
                        name TEXT,
                        date TEXT,
                        time TEXT,
                        azi REAL,
                        elev REAL
                    )
                    """
                )  # Create the table to store the predicted path

                for path in predictedPath:
                    cursor.execute(
                        """
                        INSERT INTO predicted_path (group_id, name, date, time, azi, elev)
                        VALUES (?, ?, ?, ?, ?, ?)
                        """,
                        (
                            path['group'],
                            path['name'],
                            path['date'],
                            path['time'],
                            path['azi'],
                            path['elev'],
                        ),
                    )  # Insert each path into the table

                conn.commit()
                conn.close()
            

             
            
        return predictedPath
    except Exception as e : 
        print("Prediction Error : " , e)
        return None
