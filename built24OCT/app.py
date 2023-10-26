# app.py
from menu import MainMenu

def main():
    main_menu = MainMenu()
    main_menu.run()

if __name__ == "__main__":
    main()


    '''
project_directory/
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