import urequests
import ujson
import network

ssid = "BlackRose_G"
password = "ManMan!@#"
url = "http://127.0.0.1:5000/satellite-data"

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            pass
    print("Wi-Fi connected")
    print("IP address:", wlan.ifconfig()[0])

def retrieve_json_data():
    response = urequests.get(url)
    json_data = response.json()
    response.close()

    # Access specific values from the JSON data
    value1 = json_data["key1"]
    value2 = json_data["key2"]

    # Perform actions with the extracted values
    print("Value 1:", value1)
    print("Value 2:", value2)

connect_wifi()
retrieve_json_data()

