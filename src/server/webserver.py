from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/satellite-data', methods=['GET'])
def get_satellite_data():
    # Your code to retrieve and serialize the satellite data
    satellite_data = {
        'variable1': 123,
        'variable2': 456,
        'variable3': 789,
        # ...
    }
    return jsonify(satellite_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
