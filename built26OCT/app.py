# app.py
from menu import MainMenu
from serial_server import SerialListener
import multiprocessing
from visual import show_visualization

def run_visualization():
    try:
        show_visualization()
    except Exception as e:
        print(f"Visualization Error: {e}")

def main():
    main_menu = MainMenu()
   
    visualization_process = multiprocessing.Process(target=run_visualization)
    
   
    visualization_process.start()
    
    main_menu.run()

if __name__ == "__main__":
    main()


'''
project_directory/1
│
├── app.py
│
├── built23JUNPM/
│   ├── op/
│   │   └── config.json
│   │
│   └── serialServer.py
│
├── utils.py
│
├── prediction.py
│
├── serial_server.py
│
├── visual.py
│
├── database.py
│
└── data/
    └── ... (if you have additional data files)
'''