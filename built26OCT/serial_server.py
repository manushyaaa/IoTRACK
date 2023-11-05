# serial_server.py
'''
Path: built23JUNPM/serialServer.py
Arduino Mega 2560 (COM5) , HWID: USB VID:PID=2341:0042 SER=24238313835351812262 LOCATION=1-4.3, VID: 9025, PID: 66, Name: COM5
USB Serial Port (COM3) , HWID: USB VID:PID=0403:6001 SER=A50285BIA, VID: 1027, PID: 24577, Name: COM3
'''
import serial
import time
from datetime import datetime
from utils import create_connection
import os
import serial.tools.list_ports
import json
from utils import generatePos,colorize, colorize_output
 
 
with open("G:\MinorProject\IoTRACK\\built26OCT\config.json", "r") as config_file:
    config = json.load(config_file)

VID = config["serial_vid"]
PID = config["serial_pid"]
BAUD_RATE = config["serial_baud"]

VID_L = config["serial_vid_MEGA"]
PID_L = config["serial_pid_MEGA"]
 

def get_com_port():
    ports = serial.tools.list_ports.comports()
    for port in ports:
        if port.vid == VID and port.pid == PID:
            print(colorize("\nFound your device:", 'blue'), port.device)
            return str(port.device)
    print("Device not found.")
    return None

def get_com_port_l():
    ports = serial.tools.list_ports.comports()
    for port in ports:
        if port.vid == VID_L and port.pid == PID_L:
            print(colorize("\nFound your device:", 'blue'), port.device)
            return str(port.device)
    print("Device not found.")
    return None
 
def startSerialServer():
    while True:
        # Wait for the COM port to become available
        com_port = get_com_port()
        while not com_port:
            print(colorize("COM not found. Waiting...", "red"))
            time.sleep(1)
            com_port = get_com_port()

        try:
            ser = serial.Serial(com_port, BAUD_RATE)
        except serial.SerialException as e:
            print(colorize("Serial communication error:", 'red'), e)

        try:
            while True:
                current_time = datetime.now().strftime('%H:%M:%S') 
                date = datetime.now().strftime('%d-%m-%y')
                 
                azi , ele = generatePos()

                packet = f'{current_time}_{date}_{azi}_{ele}\n'
                packet_console = f'{current_time}_{date}_{azi}_{ele}'
                print(colorize_output(packet_console, "white" , "on_blue"))

                ser.write(packet.encode('utf-8'))
                time.sleep(1) 
        except serial.SerialException as e:
            print(colorize("Serial communication error:", 'red'), e)

        ser.close()


def SerialListener():
    com_port = get_com_port_l()
    while not com_port:        
        print(colorize("MEGA not found. Waiting...", "red"))
        time.sleep(1)
        com_port = get_com_port_l()

    try:
        ser_MEGA = serial.Serial(com_port, BAUD_RATE)
    except serial.SerialException as e:
        print(colorize("Serial communication error:", 'red'), e)
    
    try : 
        while True:
            data = ser_MEGA.readline().decode('utf-8')
            data = data.strip() 
           
            time_str, date_str, latitude_str, longitude_str = data.split("_")
 
            latitude = float(latitude_str)
            longitude = float(longitude_str)
           
            packet = f'{time_str} {date_str} {latitude} {longitude}'

            print(colorize_output(packet, "white" , "on_green"))
       
      
    except serial.SerialException as e:
        print(colorize("Serial communication error:", 'red'), e)
    ser_MEGA.close()

class SerialServer:
    def start_server(self):
        startSerialServer()
    
# SerialListener()


# satellite_data= {}
# conn = create_connection()
# while True : 
#     if conn:
#         cursor = conn.cursor()
#         current_time =datetime.now().strftime('%H:%M:%S') 
#         data = cursor.execute(f"SELECT azi , elev from precisePredict where time == '{current_time}'")
#         data = cursor.fetchone()
#         if data : 
#             print(data[0] , data[1])

#     time.sleep(1) 

 
# try:
#     conn = create_connection()    
#     while True:
#         if conn:
#             cursor = conn.cursor()
#             current_time =datetime.now().strftime('%H:%M:%S') 
#             data = cursor.execute(f"SELECT azi , elev from precisePredict where time == '{current_time}'")
#             data = cursor.fetchone()
#         # Send data
#             if data : 
#                 data_to_send = f'{data[0]} {data[1]} NOAA_18 11111111 33333333 x\n'.encode()
#                 print("data sent : " , data[0] , data[1])
#                 ser.write(data_to_send)
        
#             time.sleep(1)

 





 