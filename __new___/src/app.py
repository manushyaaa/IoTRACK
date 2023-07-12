from flask import Flask, render_template, session, request, redirect
from predictor import predict 
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'key'
 
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

    if request.method == 'POST':
        show_predictor = False
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

            prediction = predict(start_year , start_month , start_day , end_year , end_month , end_day , satName , location)
          
            if prediction is not None : 
                show_predictor = True
          
            return render_template('app.html', satName=satName, location=location, prediction = prediction , show_predictor = show_predictor )
             

    return render_template('app.html', satName=satName, location=location  )

@app.route('/loadTLE', methods=['GET', 'POST'])
def loadTLE():
    if request.method == 'POST':

        amateur_checked = 'amateur' in request.form
        weather_checked = 'weather' in request.form
        cubesat_checked = 'cubesat' in request.form
        other_checked = 'other' in request.form

        # loadTLE(amateur_checked , weather_checked ,cubesat_checked , other_checked)


        return redirect('/app')


if __name__ == '__main__':
    app.run(debug=True)
