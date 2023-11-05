import sys
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from utils import colorize_output, generatePos
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np
import serial
import datetime
from PyQt5.QtWidgets import QApplication, QMainWindow, QFrame, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import QTimer

VID_L = 9025
PID_L = 66
BAUD_RATE = 115200
BACKGROUND_COLOR = '#10225B'
BACKGROUND_ALPHA = 1
AZI_COLOR = '#6BBBF4'
ELE_COLOR = '#E34C26'
# Define other constants...
background_color = '#10225B'
background_alpha = 1
azi_color = '#6BBBF4'
ele_color = '#E34C26'
patch_edge_color = '#E34C26'
grid_line_color = '#6BBBF4'
legend_text_color = '#6BBBF4'

class RealTimePolarChart(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = "Real-time Polar Chart"
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(100, 100, 800, 600)
        self.central_widget = QFrame()
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout()
        self.central_widget.setLayout(layout)

        self.canvas = self.create_polar_chart()
        layout.addWidget(self.canvas)

        self.quit_button = QPushButton("Quit", self)
        self.quit_button.clicked.connect(self.close_application)
        layout.addWidget(self.quit_button)

        self.time_label = QLabel()
        layout.addWidget(self.time_label)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)

    def create_polar_chart(self):
        title = "AZI ELE"
        subplot_ratio = 1
        size_scale = 1.2

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
            ele, azi = generatePos("NOAA 18", "Abode Valley Potheri")
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

        # Create a semicircular patch to show the area covered by the elevation line
        semicircle = plt.Polygon(
            np.column_stack([np.linspace(np.deg2rad(-90), np.deg2rad(90), 100), np.ones(100) * 0.9 * size_scale]),
            closed=True, fill=False, edgecolor=patch_edge_color, linewidth=2.1 * size_scale, alpha=0.5)
        ax_ele.add_patch(semicircle)

        for label_degree in range(-90, 91, 10):
            radian = np.deg2rad(label_degree)
            ax_ele.text(radian, 1 * size_scale, f"{label_degree}°", fontsize=7 * size_scale, color=ele_color, ha='center',
                        va='center')

        degree_labels = [i * 10 for i in range(36)]

        for label_degree in degree_labels:
            radian = np.deg2rad(label_degree)
            ax_azi.text(radian, 1.05 * size_scale, f"{label_degree}°", fontsize=7 * size_scale, color=azi_color, ha='center',
                        va='center')

        ani = FuncAnimation(fig, update, frames=np.arange(0, 360, 1000), init_func=init, blit=True)

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
                ax_azi.plot([radian, radian], [0, 0.9 * size_scale], color=grid_line_color, linestyle='-', linewidth=1.4 * size_scale,
                            alpha=0.1)
            else:
                ax_azi.plot([radian, radian], [0, 0.9 * size_scale], color=grid_line_color, linestyle='-', linewidth=0.35 * size_scale,
                            alpha=0.1)

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

        canvas = FigureCanvas(ani._fig)
        return canvas

    def update_time(self):
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.time_label.setText("Current Time: " + current_time)

    def close_application(self):
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RealTimePolarChart()
    window.show()
    sys.exit(app.exec_())
