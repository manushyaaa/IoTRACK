import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from utils import generatePos, colorize, colorize_output
import numpy as np
from datetime import datetime
import serial
import json

# Load configuration from a JSON file
with open("G:\MinorProject\IoTRACK\\built26OCT\config.json", "r") as config_file:
    config = json.load(config_file)

VID_L = config["serial_vid_MEGA"]
PID_L = config["serial_pid_MEGA"]
BAUD_RATE = config["serial_baud"]
 
def get_com_port_l():
    ports = serial.tools.list_ports.comports()
    for port in ports:
        if port.vid == VID_L and port.pid == PID_L:
            print("Found your device:", port.device)
            return str(port.device)
    print("Device not found.")
    return None

def show_visualization():

    com_port = get_com_port_l()
    ser_MEGA = serial.Serial(com_port, BAUD_RATE)

    def create_motor_elevation_animation(get_motor_and_elevation_angles, title="AZI ELE Visualization"):
        fig, ax = plt.subplots(subplot_kw={'projection': 'polar'}, figsize=(6, 6))
        
        motor_line, = ax.plot([], [], lw=2, label='AZI', color='blue')
        elevation_line, = ax.plot([], [], lw=2, label='ELE', color='red')
        
        azi_text = ax.text(0, 0, 'AZI: ', fontsize=10, color='blue')
        ele_text = ax.text(0, 0.1, 'ELE: ', fontsize=10, color='red')

        def init():
            motor_line.set_data([], [])
            elevation_line.set_data([], [])
            return motor_line, elevation_line, azi_text, ele_text
        
        def update(frame):
            data = ser_MEGA.readline().decode('utf-8')
            data = data.strip() 
            print(colorize_output(data, "white" , "on_blue"))
             
            time_str, date_str, latitude_str, longitude_str = data.split("_")
 
            ele = float(latitude_str)
            azi = float(longitude_str)
    
            if ele <= 180:
                elevation_angle_rad = np.deg2rad(ele)
            else:
                elevation_angle_rad = np.deg2rad(ele - 360)

            motor_angle_rad = np.deg2rad(azi)
            motor_line.set_data([motor_angle_rad, motor_angle_rad], [0, 1.2])
            elevation_line.set_data([elevation_angle_rad, elevation_angle_rad], [0, 0.8])
            
            azi_text.set_text(f'AZI: {azi}°')
            ele_text.set_text(f'ELE: {ele}°')
            
            return motor_line, elevation_line, azi_text, ele_text

        # Create a semicircular patch to show the area covered by elevation line
        semicircle = plt.Polygon(np.column_stack([np.linspace(np.deg2rad(-90), np.deg2rad(90), 100), np.ones(100)*0.8]), closed=True, fill=False, edgecolor='red', linewidth=3, alpha=0.5)
        ax.add_patch(semicircle)

        for label_degree in range(-90, 91, 10):
            radian = np.deg2rad(label_degree)
            ax.text(radian, 0.9, f"{label_degree}°", fontsize=8, color='red', ha='center', va='center')
    
        ani = FuncAnimation(fig, update, frames=np.arange(0, 360, 0.1), init_func=init, blit=True)

        ax.set_rmax(1.2)
        ax.set_rticks([]) 
        ax.set_yticklabels([])  
    
        ax.set_theta_zero_location("N")
        ax.set_theta_direction(-1) 

        degree_labels = [i * 10 for i in range(36)]
        ax.set_thetagrids(degree_labels, labels=[f"{d}°" for d in degree_labels], fontsize=8, color='blue')
        for degree in degree_labels:
            radian = np.deg2rad(degree)
            if degree in [0, 90, 180, 270]:
                ax.plot([radian, radian], [0, 1], color='black', linestyle='-', linewidth=1, alpha=0.5)
            else:
                ax.plot([radian, radian], [0, 1], color='lightgray', linestyle='-', linewidth=0.5, alpha=0.1)

        # Add a center point
        ax.plot(0, 0, marker='o', markersize=3, color='black'  )
        plt.title(title, y=1.1, fontsize=10, fontweight='bold', loc='left')
        ax.legend(loc='upper left')

        # Change the main circle color to blue
        ax.spines['polar'].set_edgecolor('blue')
        ax.spines['polar'].set_linewidth(3)
        ax.spines['polar'].set_alpha(0.5)

        return ani

    def get_motor_and_elevation_angles():
        current_time = datetime.now().strftime('%H:%M:%S')
        date = datetime.now().strftime('%d-%m-%y')

        ele, azi = generatePos()
        packet = f'{current_time} ---- {date} ---- {azi} ---- {ele}\n'

        print(packet)
        return azi, ele     

    ani = create_motor_elevation_animation(get_motor_and_elevation_angles)
    plt.show()
 

 



 