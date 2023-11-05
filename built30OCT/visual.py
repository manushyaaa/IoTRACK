import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from utils import colorize_output 
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
 

# Define color variables
background_color = '#10225B'
background_alpha = 0.9 
azi_color = '#6BBBF4'
ele_color = '#E34C26'
patch_edge_color = '#E34C26'
grid_line_color = '#6BBBF4'
legend_text_color = '#6BBBF4'

def get_com_port_l():
    try:
        ports = serial.tools.list_ports.comports()
        for port in ports:
            if port.vid == VID_L and port.pid == PID_L:
                print(colorize_output("Found your device: ", 'blue', 'on_white'), port.device)
                return str(port.device)
        print(colorize_output("Device not found.", 'white', 'on_red'))
    except Exception as e:
        print(colorize_output(f"Error while listing COM ports: {e}", 'white' , "on_red"))
    return None

def show_visualization():

    try:
        com_port = get_com_port_l()
        if com_port is None:
            return

        ser_MEGA = serial.Serial(com_port, BAUD_RATE)        

        def create_motor_elevation_animation(get_motor_and_elevation_angles, title="AZI ELE", subplot_ratio=1):
    
             
            size_scale = 1.5
            fig = plt.figure(figsize=(8 * size_scale, 4 * size_scale))
            plt.rcParams['font.size'] = 7 * size_scale

            # Set background color
            fig.patch.set_facecolor(background_color)
            fig.patch.set_alpha(background_alpha)

            gs = fig.add_gridspec(2, 2, width_ratios=[1, 1], height_ratios=[subplot_ratio, 1 - subplot_ratio])

            # Azimuth subplot
            ax_azi = fig.add_subplot(gs[0, 0], projection='polar')
            motor_line, = ax_azi.plot([], [], lw=1.4 * size_scale, label='AZI', color=azi_color)
            azi_text = ax_azi.text(0, 0, 'AZI: ', fontsize=7 * size_scale, color=azi_color)

            # Elevation subplot
            ax_ele = fig.add_subplot(gs[0, 1], projection='polar')
            elevation_line, = ax_ele.plot([], [], lw=1.4 * size_scale, label='ELE', color=ele_color)
            ele_text = ax_ele.text(0, 0, 'ELE: ', fontsize=7 * size_scale, color=ele_color)

            def init():
                motor_line.set_data([], [])
                elevation_line.set_data([], [])
                return motor_line, elevation_line, azi_text, ele_text

            def update(frame):
                data = ser_MEGA.readline().decode('utf-8')
                data = data.strip() 
                print("RX : " ,colorize_output(  data, "white" , "on_green"))
            
                time_str, date_str, latitude_str, longitude_str = data.split("_")
    
                ele = float(latitude_str)
                azi = float(longitude_str)

                if ele <= 180:
                    elevation_angle_rad = np.deg2rad(ele)
                else:
                    elevation_angle_rad = np.deg2rad(ele - 360)

                motor_angle_rad = np.deg2rad(azi)
                motor_line.set_data([motor_angle_rad, motor_angle_rad], [0, 1 * size_scale])
                elevation_line.set_data([elevation_angle_rad, elevation_angle_rad], [0, 0.9 * size_scale])

                azi_text.set_text(f'AZI: {azi}°')
                ele_text.set_text(f'ELE: {ele}°')

                return motor_line, elevation_line, azi_text, ele_text

            # Create a semicircular patch to show the area covered by elevation line
            semicircle = plt.Polygon(np.column_stack([np.linspace(np.deg2rad(-90), np.deg2rad(90), 100), np.ones(100) * 0.9 * size_scale]),
                                    closed=True, fill=False, edgecolor=patch_edge_color, linewidth=2.1 * size_scale, alpha=0.5)
            ax_ele.add_patch(semicircle)

            for label_degree in range(-90, 91, 10):
                radian = np.deg2rad(label_degree)
                ax_ele.text(radian, 1 * size_scale, f"{label_degree}°", fontsize=7 * size_scale, color=ele_color, ha='center', va='center')

            degree_labels = [i * 10 for i in range(36)]

            for label_degree in degree_labels:
                radian = np.deg2rad(label_degree)
                ax_azi.text(radian, 1.05 * size_scale, f"{label_degree}°", fontsize=7 * size_scale, color=azi_color, ha='center', va='center')

            ani = FuncAnimation(fig, update, frames=np.arange(0, 360, 36000), init_func=init, blit=True)

            ax_azi.set_rmax(0.35 * size_scale)
            ax_azi.set_rticks([])
            ax_azi.set_yticklabels([])
            ax_azi.set_xticklabels([])

            ax_ele.set_rmax(0.35 * size_scale)
            ax_ele.set_rticks([])

            ax_azi.set_theta_zero_location("N")
            ax_azi.set_theta_direction(-1)

            ax_ele.set_theta_zero_location("N")
            ax_ele.set_theta_direction(-1)

            ax_ele.grid(False)
            ax_ele.set_yticklabels([])
            ax_ele.set_xticklabels([])

            for degree in degree_labels:
                radian = np.deg2rad(degree)
                if degree in [0, 90, 180, 270]:
                    ax_azi.plot([radian, radian], [0, 0.9 * size_scale], color=grid_line_color, linestyle='-', linewidth=1.4 * size_scale, alpha=0.1)
                else:
                    ax_azi.plot([radian, radian], [0, 0.9 * size_scale], color=grid_line_color, linestyle='-', linewidth=0.35 * size_scale, alpha=0.1)

            ax_azi.plot(0, 0, marker='o', markersize=1.5 * size_scale, color=azi_color)
            ax_ele.plot(0, 0, marker='o', markersize=1.5 * size_scale, color=ele_color)

            ax_azi.legend(loc='upper left')
            ax_ele.legend(loc='upper left')

            ax_azi.spines['polar'].set_edgecolor(azi_color)
            ax_ele.spines['polar'].set_edgecolor(ele_color)
        
            ax_azi.spines['polar'].set_linewidth(2.1 * size_scale)
            
            ax_azi.spines['polar'].set_alpha(0.5)
            ax_azi.set_facecolor('none')  

            ax_ele.spines['polar'].set_linewidth(0)
            ax_ele.set_facecolor('none')

            ax_ele.fill_between(np.linspace(np.deg2rad(-90), np.deg2rad(90), 100), 0, 0.9 * size_scale, color=ele_color, alpha=0.1)

            plt.suptitle(title, fontsize=10 * size_scale, fontweight='bold', x=0.5, y=0.95, color=legend_text_color)
            fig.patch.set_alpha(background_alpha)

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

    except Exception as e:
        print(f"Visualization Error: {e}")
      

 