import serial
import time
from datetime import datetime
import json
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from utils import generatePos, plot_motor_position

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
        azi, ele = get_motor_and_elevation_angles()
        motor_angle_deg_with_north = (450 - azi) % 360
        elevation_angle_deg_with_north = (450 - ele) % 360

        # Calculate elevation angle in radians with support for negative elevations
        if elevation_angle_deg_with_north <= 180:
            elevation_angle_rad = np.deg2rad(elevation_angle_deg_with_north)
        else:
            elevation_angle_rad = np.deg2rad(elevation_angle_deg_with_north - 360)

        motor_angle_rad = np.deg2rad(motor_angle_deg_with_north)
        motor_line.set_data([motor_angle_rad, motor_angle_rad], [0, 1])
        elevation_line.set_data([elevation_angle_rad, elevation_angle_rad], [0, 0.8])
        return motor_line, elevation_line

    # Create an animation
    ani = FuncAnimation(fig, update, frames=np.arange(0, 360, 0.1), init_func=init, blit=True)

    ax.set_rmax(1.2)
    ax.set_rticks([])  # Hide radial ticks
    ax.set_yticklabels([])  # Hide radial labels
  
    ax.set_theta_zero_location("N")
    ax.set_theta_direction(-1)  # Rotate labels to align 0 degrees with the top



    # Add degree labels around the circle
    degree_labels = [0, 45, 90, 135, 180, 225, 270, 315]
    ax.set_thetagrids(degree_labels, labels=[f"{d}°" for d in degree_labels])

    # Set the title and adjust the position
    plt.title(title, y=1.1)

    # Add a legend to differentiate between motor and elevation lines
    ax.legend(loc='upper left')

    return ani

def get_motor_and_elevation_angles():
    

    current_time = datetime.now().strftime('%H:%M:%S')
    date = datetime.now().strftime('%d-%m-%y')
        
    ele, azi = generatePos() 

    packet = f'{current_time} ---- {date} ---- {azi} ---- {ele}\n'
    

    print(packet)
    return azi, ele

# Call create_motor_elevation_animation with get_motor_and_elevation_angles
ani = create_motor_elevation_animation(get_motor_and_elevation_angles, title="Motor and Elevation Movement Visualization")

# Start the animation
plt.show()
