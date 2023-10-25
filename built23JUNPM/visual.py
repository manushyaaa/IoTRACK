import serial
import time
from datetime import datetime
 

import json
from utils import generatePos , plot_motor_position 
 

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


def create_motor_elevation_animation(get_motor_and_elevation_angles, title="Motor and Elevation Movement Visualization"):
    # Initialize the figure and polar axis
    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'}, figsize=(6, 6))

    # Initialize a line that represents the motor position
    motor_line, = ax.plot([], [], lw=2, label='Motor Position')

    # Initialize a line that represents the elevation angle
    elevation_line, = ax.plot([], [], lw=2, label='Elevation')

    # Function to initialize the plot
    def init():
        motor_line.set_data([], [])
        elevation_line.set_data([], [])
        return motor_line, elevation_line

    # Function to update the plot with real-time motor and elevation angle data
    def update(frame):
        motor_angle_deg, elevation_angle_deg = get_motor_and_elevation_angles()
        motor_angle_deg_with_north = (450 - motor_angle_deg) % 360
        elevation_angle_deg_with_north = (450 - elevation_angle_deg) % 360
        motor_angle_rad = np.deg2rad(motor_angle_deg_with_north)
        elevation_angle_rad = np.deg2rad(elevation_angle_deg_with_north)
        motor_line.set_data([motor_angle_rad, motor_angle_rad], [0, 1])
        elevation_line.set_data([elevation_angle_rad, elevation_angle_rad], [0, 0.8])
        return motor_line, elevation_line

    # Create an animation
    ani = FuncAnimation(fig, update, frames=np.arange(0, 360, 1), init_func=init, blit=True)

    # Set the polar plot properties
    ax.set_rmax(1.2)
    ax.set_rticks([])  # Hide radial ticks
    ax.set_yticklabels([])  # Hide radial labels
    ax.set_xticks(np.arange(0, 2 * np.pi, np.pi / 4))
    ax.set_xticklabels(['North', 'Northwest', 'West', 'Southwest', 'South', 'Southeast', 'East', 'Northeast'])
    ax.set_theta_offset(np.pi/2)  # Rotate labels to align North with the top
    ax.set_theta_direction(-1)    # Reverse the direction of the angle labels

    # Add degree labels around the circle
    degree_labels = [0, 45, 90, 135, 180, 225, 270, 315]
    ax.set_thetagrids(degree_labels, labels=[f"{d}°" for d in degree_labels])

    # Set the title and adjust the position
    plt.title(title, y=1.1)

    # Add a legend to differentiate between motor and elevation lines
    ax.legend(loc='upper left')

    return ani











'''
Path: built23JUNPM/serialServer.py
Arduino Mega 2560 (COM5) , HWID: USB VID:PID=2341:0042 SER=24238313835351812262 LOCATION=1-4.3, VID: 9025, PID: 66, Name: COM5
USB Serial Port (COM3) , HWID: USB VID:PID=0403:6001 SER=A50285BIA, VID: 1027, PID: 24577, Name: COM3
'''
 
 
 




def startSerialServer():
    while True:


        try:
            while True:
                # Get the current time as a string with a newline character
                current_time = datetime.now().strftime('%H:%M:%S') 
                date = datetime.now().strftime('%d-%m-%y')
                 
                azi , ele = generatePos()

                packet = f'{current_time} ---- {date} ---- {azi} ---- {ele}\n'
                

                print(packet)
                time.sleep(2)  # Send the time every second

                

        except serial.SerialException as e:
            print("Serial communication error:", e)

        ser.close()

startSerialServer()

  
 
 




 