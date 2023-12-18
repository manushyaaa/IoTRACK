import sqlite3  
from utils import *
from tqdm import tqdm
from skyfield.api import wgs84, load
from datetime import timedelta, timezone , datetime as dt
from geopy import Nominatim
import time
import pytz

global SATNAME, LOCATION
ist_timezone = pytz.timezone('Asia/Kolkata')
precisepath = []

config = configparser.ConfigParser()
config_file_path = 'G:\\MinorProject\\december\\build10DEC\\op\\aos.ini'

if os.path.exists(config_file_path):
    os.remove(config_file_path)

def predict():
    try:
        current_date = dt.now().strftime('%d-%m-%Y')
        day = int(current_date[0:2])
        month = int(current_date[3:5])
        year = int(current_date[6:10])

        sy, sm, sd = year, month, day
        ey, em, ed = year, month, day + 1

        satName = str(input("Enter the satellite name: "))
        location = input("Enter the location: ")
        global SATNAME , LOCATION
        # satName = "ISS (ZARYA)"
        SATNAME = satName
        #location = 'Bhopal'
        LOCATION = location

        satellite = getTLE(satName)
        latNS, logEW = getLocation(location) # latNS, logEW = 22.2432, 77.43821
        #latNS, logEW = 32.0000, -137.7556
        #latNS, logEW = -51.1579, 179.3411
        QTH = wgs84.latlon(latNS, logEW)

        ts = load.timescale()
        t = ts.now()    

        predictionStartTime = ts.utc(sy, sm, sd)
        predictionEndTime = ts.utc(ey, em, ed)

        group_id = 0
        current_group_id = None

        t, events = satellite.find_events(QTH, predictionStartTime, predictionEndTime, altitude_degrees=0)
        event_names = 'AOS', 'MAX', 'LOS'

        predictedPath = []

        event_list = list(zip(t, events))
        difference = satellite - QTH
        for (ti, event) in zip(t, events):

            timePath = ti
            topocentric = difference.at(timePath)
            alt, az, distance = topocentric.altaz()
            name = event_names[event]

            if name == 'AOS':
                current_group_id = group_id
                group_id += 1

            path = {
                'name': name,
                'timeIST': ti.astimezone(pytz.timezone('Asia/Kolkata')),
                'elev': np.round(alt.degrees, 2),
                'azi': np.round(az.degrees, 2)
            }
            predictedPath.append(path)

        startTimes = []
        endTimes = []

        for i in range(len(predictedPath)):
            if predictedPath[i]['name'] == 'AOS':
                startTime = predictedPath[i]['timeIST']
                startTimes.append(startTime)

            if predictedPath[i]['name'] == 'LOS':
                endTime = predictedPath[i]['timeIST']
                endTimes.append(endTime)

        updated_startTimes = [time - timedelta(minutes=2) for time in startTimes]
        updated_endTimes = [time + timedelta(minutes=1) for time in endTimes]
        corrected_endTimes = [time + timedelta(minutes=1) for time in endTimes]

        timeBracket = list(zip(updated_startTimes, corrected_endTimes))

        i = 0 
        group_id = 0
        current_group_id = 0
        for i in tqdm(range(len(timeBracket))):
            current_group_id = group_id
            group_id += 1

            config.add_section(f'GROUP {i+1}')

            predictionStartTime = ts.utc(timeBracket[i][0])
            predictionEndTime = ts.utc(timeBracket[i][1] )
            interval = 1 # seconds
            current_time = predictionStartTime

            while current_time.tt <= predictionEndTime.tt:
                
                ti = current_time
                difference = satellite - QTH
                topocentric = difference.at(ti)
                alt, az, distance = topocentric.altaz()
                ti_ist = ti.astimezone(ist_timezone)
                ist_date = ti_ist.strftime('%d-%b-%y')
                ist_time = ti_ist.strftime('%H:%M:%S')
                for j in range(len(event_list)):
                    if ist_time == event_list[j][0].astimezone(ist_timezone).strftime('%H:%M:%S'):
                        event = event_list[j][1]
                        break
                    else:
                        event = '4'

                if event == 0:
                    event = 'AOS'
                elif event == 1:
                    event = 'MAX'
                elif event == 2:
                    event = 'LOS'
                else:
                    event = 'NONE'

                if event == 'AOS' :
                    azi = np.round(az.degrees, 2)
                    smov_bit , reposition_amount = calculate_movement(0, azi)
                    emov_bit = reverseDirection(smov_bit)
                    config.set(f'GROUP {i+1}', f'AOS', str(startTimes[i]))
                    config.set(f'GROUP {i+1}', f'START_MOV_BIT', str(smov_bit))
                    config.set(f'GROUP {i+1}', f'START_REPOSITION_DEG', str(reposition_amount))
                    config.set(f'GROUP {i+1}', f'LOS', str(endTimes[i]))
                    config.set(f'GROUP {i+1}', f'COMPLETED_MOV_BIT', str(emov_bit))
                    config.set(f'GROUP {i+1}', f'COMPLETED_REPOSITION_DEG', '0')
                else : 
                    smov_bit = 'NEU'
                    emov_bit = 'NEU'
                    reposition_amount = 0

                p_path = {
                    'group_id' : group_id,
                    'event' : event ,
                    'date': ist_date,
                    'timeIST': ist_time,
                    'timeUTC': ti.utc_strftime('%H:%M:%S'),
                    'azi': np.round(az.degrees, 2),
                    'elev': np.round(alt.degrees, 2),
                    'smov_bit': smov_bit ,
                    'emov_bit': emov_bit ,
                    'reposition_amount' : reposition_amount
                }
                
                precisepath.append(p_path)
                current_time += timedelta(seconds=interval)

        with open(config_file_path, 'w') as configfile:
            config.write(configfile)

        store_precisepath_in_database(satName, precisepath)
        return precisepath , updated_startTimes , updated_endTimes , startTimes , endTimes , satName , location

    except Exception as e:
        print(e)
        return

def store_precisepath_in_database(satellite_name, precisepath):
    try:        
        conn = sqlite3.connect('satellite_data.db')
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS predicted_path")
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS predicted_path (
                group_id INTEGER,
                satellite_name TEXT,
                date_today TEXT,
                event TEXT,
                time_ist TEXT,
                time_utc TEXT,
                azi REAL,
                elev REAL,
                smov_bit TEXT,
                emov_bit TEXT,
                reposition_amount REAL
            )
        ''')
        date_today = dt.now().strftime('%d-%m-%Y')

        for entry in precisepath:
            cursor.execute('''
                INSERT INTO predicted_path (
                    group_id ,satellite_name, date_today, event, time_ist, time_utc, azi, elev, smov_bit , emov_bit, reposition_amount
                ) VALUES (?,?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                entry['group_id'],
                satellite_name,
                date_today,
                entry['event'],
                entry['timeIST'],
                entry['timeUTC'],
                entry['azi'],
                entry['elev'],
                entry['smov_bit'],
                entry['emov_bit'],
                entry['reposition_amount']
            ))
        # Commit the changes and close the connection
        conn.commit()
        conn.close()

        print("Data stored successfully!")

    except Exception as e:
        print("Error:", e)

#packet = f'{current_time} {AZI} {ELE} {_SATNAME} {_LOCATION} {DIRECTION} {RESPOSITION} x\n'

# for i in range(len(UAOS)):
#     print(UAOS[i].astimezone(ist_timezone).strftime('%H:%M:%S'), AOS[i].astimezone(ist_timezone).strftime('%H:%M:%S'), LOS[i].astimezone(ist_timezone).strftime('%H:%M:%S'), ULOS[i].astimezone(ist_timezone).strftime('%H:%M:%S'))

# while True :
#     current_time = dt.now(timezone.utc)

#     print(checkState(current_time , UAOS , AOS , LOS , ULOS))
#     time.sleep(1)


