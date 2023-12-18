from utils import *
from predict import *
import serial
import serial.tools.list_ports
import configparser
import os
import time
import threading
import sqlite3
from datetime import datetime as dt
from datetime import timedelta

config = load_config()  # `config` is a `ConfigParser` object
update_tle_data() 

global SATNAME, LOCATION     
VID = config.getint('TTL_DEVICE_ID', 'VID')
PID = config.getint('TTL_DEVICE_ID', 'PID')
BAUD_RATE = config.getint('GENERAL', 'BAUDRATE')

output_file_path = 'predictions.txt'
current_time = dt.now() 

if os.path.exists(output_file_path):
    os.remove(output_file_path)


def get_com_port():
    ports = serial.tools.list_ports.comports()
    for port in ports:
        if port.vid == VID and port.pid == PID:
            print(colorize("\nFound your device:", 'blue'), port.device)
            return str(port.device)
    print("Device not found.")
    return None

data , UAOS , ULOS , AOS , LOS , SATNAME , LOCATION= predict()

print('Satellite Name : ' , SATNAME)
for path in data:
    if path['event'] in ['AOS', 'LOS', 'MAX']:
        print(path['timeIST'], path['event'],path['azi'], path['elev'])

with open(output_file_path, 'w') as file:
    prev_event = None  

    line = f"Prediction Time : {current_time.strftime('%H:%M:%S')} \n"
    file.write(line)
    line = f"Prediction Date : {current_time.strftime('%d-%m-%Y')} \n"
    file.write(line)
    line = f"Satellite Name : {SATNAME} \n"
    file.write(line)
    line = f"Location : {LOCATION} \n\n"
    file.write(line)
    line = f"Upcoming Events : \n"
    file.write(line)

    for path in data:
        if path['event'] in ['AOS', 'LOS', 'MAX']:
            if prev_event == 'LOS':
                file.write('\n')
            line = f"{path['timeIST']} {path['event']} {path['azi']} {path['elev']} \n"
            file.write(line)
            prev_event = path['event']

data_file = configparser.ConfigParser()
data_file.read('G:\\MinorProject\\december\\build10DEC\\op\\aos.ini')

direction = 'NEU'
reposition_amount = 0

while True:
    conn = sqlite3.connect('satellite_data.db')
    cursor = conn.cursor()

    com_port = get_com_port()
    print(com_port, BAUD_RATE)

    while not com_port:
        print(colorize("COM not found. Waiting...", "red"))
        time.sleep(1)
        com_port = get_com_port()

    try:
        ser = serial.Serial( com_port, BAUD_RATE)    
    
        while True :
            state = checkState(UAOS , AOS , LOS , ULOS)
            current_time = dt.now().strftime('%H:%M:%S')
            query = '''
                    SELECT * FROM predicted_path
                    WHERE satellite_name = ?
                        AND time_ist > ?
                    ORDER BY time_ist ASC
                    LIMIT 1
                '''
            next_group = cursor.execute(query, (SATNAME, current_time )).fetchone()
            next_group = next_group[0] if next_group else None

            if next_group == None:
                query = '''
                        SELECT MAX(group_id) FROM predicted_path
                    '''
                max_group = cursor.execute(query).fetchone()
                next_group = max_group[0]

            if next_group :  
                if conn:
                    cursor.execute("SELECT * FROM predicted_path WHERE time_ist = ?", (current_time,))
                    data = cursor.fetchall()
                    try:
                        if data:
                            for row in data:
                                group = row[0]
                                satname = row[1]
                                azi = row[6]
                                elev = row[7]
                                event = row[3]
                        
                                if state == 2 :
                                    direction = data_file.get(
                                        f'GROUP {next_group}', 'start_mov_bit')
                                    reposition_amount = data_file.get(
                                        f'GROUP {next_group}', 'start_reposition_deg')

                                elif state == 4:
                                    direction = data_file.get(
                                        f'GROUP {next_group}', 'completed_mov_bit')
                                    reposition_amount = data_file.get(
                                        f'GROUP {next_group}', 'completed_reposition_deg')

                                elif state == 3:
                                    direction = 'FREE'
                                    reposition_amount = '0'

                                else :
                                    direction = 'NEU'
                                    reposition_amount = '0'

                                packet = f'{current_time} {azi} {elev} {remove_space(satname)} {direction} {reposition_amount} x\n'
                                ser.write(packet.encode('utf-8'))
                                
                                if state == 2:
                                    print(colorize_output(f'{state , next_group}' , 'black' , 'on_green'),colorize_output(ignore_lastchar(packet) , 'white' , 'on_green'))
                                elif state == 4:
                                    print(colorize_output(f'{state , next_group}', 'black' , 'on_red'),colorize_output(ignore_lastchar(packet) , 'white' , 'on_red'))
                                else :
                                    print(colorize_output(f'{state , next_group}', 'black' , 'on_white'),colorize_output(ignore_lastchar(packet) , 'white' , 'on_blue'))
 
                        else :
                            elev , azi = generatePos(SATNAME , LOCATION)          
                            direction = 'NEU'
                            reposition_amount = '0'
                            packet = f'{current_time} {azi} {elev} {remove_space(SATNAME)} {direction} {reposition_amount} x\n'
                            ser.write(packet.encode('utf-8'))
                            print(colorize_output(f'{state , next_group}', 'black' , 'on_yellow'),colorize_output(ignore_lastchar(packet) , 'black' , 'on_yellow'))
                    except Exception as e:
                        print(e)
            else :
                print('No upcoming events')
                break

            time.sleep(1)
    except serial.SerialException as se:
        print(colorize(f"Serial Exception: {se}", "red"))
    except PermissionError as pe:
        print(colorize(f"Permission Error: {pe}", "red"))
    except Exception as e:
        print(colorize(f"An unexpected error occurred: {e}", "red"))
    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()
            print(colorize("Serial port closed.", "yellow"))