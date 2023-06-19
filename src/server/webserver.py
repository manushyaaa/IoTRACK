from flask import Flask, jsonify
from datetime import datetime
import pandas as pd
import time

app = Flask(__name__)
    
satellite_data = {}
def process_data():
    df = pd.read_excel('G:\STS\data\predictedPath.xlsx') 
    df['time'] = pd.to_datetime(df['time'])
    while True:
        current_time =datetime.now().strftime('%H:%M:%S') 
        filtered_df = df[df['time'].dt.strftime('%H:%M:%S') == current_time]

        if not filtered_df.empty:
            for index,row in filtered_df.iterrows():
                group = row[0]
                time_value = row[4]
                azim = row[5]
                elev = row[6]

                s = {
                    'time': time_value,
                    'azim': azim,
                    'elev' : elev
                }
                satellite_data.update(s)


                print(f'{time_value} {group} {azim} {elev}')

        time.sleep(1)

@app.route('/satellite-data', methods=['GET'])
def get_satellite_data():
    # Your code to retrieve and serialize the satellite data
    return jsonify(satellite_data)

if __name__ == '__main__':
    # Start a separate thread to process the data
    import threading
    data_thread = threading.Thread(target=process_data)
    data_thread.start()
  

    # Run the Flask application
    app.run(host='0.0.0.0', port=5000)
