from flask import Flask, render_template, session, request
from utils import getTLE, getLocation
from skyfield.api import wgs84 ,load
import numpy as np
from datetime import datetime
import time ,json
import sqlite3
from sqlite3 import Error

app = Flask(__name__)
app.secret_key = 'key'
 
ts = load.timescale()

def create_connection():
    conn = None
    try:
        conn = sqlite3.connect('database.db')  # Replace 'database.db' with your desired database file name
        return conn
    except Error as e:
        print(e)

    return conn


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/app', methods=['GET', 'POST'])
def mainPage():
    if 'satName' not in session:
        session['satName'] = None
    if 'location' not in session:
        session['location'] = None
    if 'predictionStartTime' not in session:
        session['predictionStartTime'] = None
    if 'predictionEndTime' not in session:
        session['predictionEndTime'] = None

 

    satName = session['satName']
    location = session['location']
    # prediction = session['prediction']
 

    if request.method == 'POST':
        if 'submit_button_time' in request.form:
            

            satName = request.form.get('user_input0')
            session['satName'] = satName
            
            location = request.form.get('user_input1')
            session['location'] = location
             
            prediction_start_date = request.form.get('prediction_start_date')
            prediction_end_date = request.form.get('prediction_end_date')
          

            start_date =  datetime.strptime(prediction_start_date, '%Y-%m-%d')
            start_year = start_date.year
            start_month = start_date.month
            start_day = start_date.day

            # Get the year, month, and day from the prediction end date
            end_date =  datetime.strptime(prediction_end_date, '%Y-%m-%d')
            end_year = end_date.year
            end_month = end_date.month
            end_day = end_date.day

            prediction = predict(start_year , start_month , start_day , end_year , end_month , end_day)

            return render_template('app.html', satName=satName, location=location, prediction = prediction)
             

    return render_template('app.html', satName=satName, location=location)



def predict(sy , sm , sd , ey , em , ed):

    try :
        predictedPath = []
        t = ts.now()
    
        satellite = getTLE(session['satName'])
        latNS, logEW = getLocation(session['location'])
        bpl = wgs84.latlon(latNS, logEW)


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

if __name__ == '__main__':
    app.run(debug=True)
