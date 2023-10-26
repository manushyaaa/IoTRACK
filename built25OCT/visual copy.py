import serial
import time
from datetime import datetime
import json
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from utils import generatePos
from multiprocessing import Process, Pipe

def create_motor_elevation_animation(get_motor_and_elevation_angles, title="Motor and Elevation Movement Visualization"):
    fig = plt.figure(figsize=(12, 6))

    # Create the subplot for the polar chart (azimuth)
    ax1 = fig.add_subplot(121, polar=True)
    
    motor_line, = ax1.plot([], [], lw=2, label='AZI', color='blue')

    azi_text = ax1.text(0, 0, 'AZI: ', fontsize=10, color='blue')

    def init():
        motor_line.set_data([], [])
        return motor_line, azi_text
    
    def update(frame):
        azi, _ = get_motor_and_elevation_angles()

        motor_angle_rad = np.deg2rad(azi)
        motor_line.set_data([motor_angle_rad, motor_angle_rad], [0, 1.2])
        
        azi_text.set_text(f'AZI: {azi}°')
        
        return motor_line, azi_text

    ani1 = FuncAnimation(fig, update, frames=np.arange(0, 360, 0.1), init_func=init, blit=True)

    ax1.set_rmax(1.2)
    ax1.set_rticks([]) 
    ax1.set_yticklabels([])  
    ax1.set_theta_zero_location("N")
    ax1.set_theta_direction(-1) 

    degree_labels = [i * 10 for i in range(36)]
    ax1.set_thetagrids(degree_labels, labels=[f"{d}°" for d in degree_labels], fontsize=8, color='blue')
    for degree in degree_labels:
        radian = np.deg2rad(degree)
        if degree in [0, 90, 180, 270]:
            ax1.plot([radian, radian], [0, 1], color='black', linestyle='-', linewidth=1, alpha=0.5)
        else:
            ax1.plot([radian, radian], [0, 1], color='lightgray', linestyle='-', linewidth=0.5, alpha=0.1)

    ax1.plot(0, 0, marker='o', markersize=3, color='black'  )
    ax1.set_title("Polar Chart (Azimuth)", fontsize=10, fontweight='bold', loc='left')
    ax1.legend(loc='upper left')

    # Create the subplot for the semicircle chart (elevation)
    ax2 = fig.add_subplot(122, aspect='equal', polar=True)
    
    semicircle = plt.Polygon(np.column_stack([np.linspace(np.deg2rad(-90), np.deg2rad(90), 100), np.ones(100)*0.8]), closed=True, fill=False, edgecolor='red', linewidth=3, alpha=0.5)
    ax2.add_patch(semicircle)

    for label_degree in range(-90, 91, 10):
        radian = np.deg2rad(label_degree)
        ax2.text(radian, 0.9, f"{label_degree}°", fontsize=8, color='red', ha='center', va='center')

    ax2.set_rmax(1.2)
    ax2.set_rticks([]) 
    ax2.set_yticklabels([])  
    ax2.set_theta_zero_location("N")
    ax2.set_theta_direction(-1) 

    ax2.set_title("Semicircle Chart (Elevation)", fontsize=10, fontweight='bold', loc='left')

    # Define a function for updating elevation
    def update_elevation(conn):
        while True:
            _, ele = conn.recv()

            elevation_angle_rad = np.deg2rad(ele)

            # Clear previous elevation line
            ax2.cla()
            ax2.add_patch(semicircle)  # Redraw the semicircle

            # Update elevation line
            ax2.plot([elevation_angle_rad, elevation_angle_rad], [0, 0.8], lw=2, label='ELE', color='red')
            ax2.text(0, 0.1, f'ELE: {ele}°', fontsize=10, color='red')
            ax2.set_rmax(1.2)
            ax2.set_rticks([]) 
            ax2.set_yticklabels([])  
            ax2.set_theta_zero_location("N")
            ax2.set_theta_direction(-1)
            fig.canvas.flush_events()
            time.sleep(0.1)

    parent_conn, child_conn = Pipe()
    elevation_process = Process(target=update_elevation, args=(child_conn,))
    elevation_process.daemon = True
    elevation_process.start()

    return ani1, parent_conn

 
if __name__ == '__main__':
    def get_motor_and_elevation_angles():    
        current_time = datetime.now().strftime('%H:%M:%S')
        date = datetime.now().strftime('%d-%m-%y')
        ele, azi = generatePos() 
        packet = f'{current_time} ---- {date} ---- {azi} ---- {ele}\n'    
        print(packet)
        return azi, ele

    ani1, elevation_conn = create_motor_elevation_animation(get_motor_and_elevation_angles, title="Motor and Elevation Movement Visualization")
    plt.show()