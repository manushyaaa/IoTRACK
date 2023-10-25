'''
app.py
Date: 2021-10-23 13:51:00
Python Version: 3.11.511211
Functions: main_menu (main)
'''

from utils import getTLE, getLocation, create_connection, predict, predictPrecise, getPredictedPath
from serialServer import startSerialServer
from skyfield.api import wgs84, load

def main_menu():
    while True:
        print("Options:")
        print("1. Predict")
        print("2. Exit")

        choice = input("Enter your choice (1 or 2): ")

        if choice == "1":
            prediction = predict()
            if not prediction[0].empty:
                while True:
                    print("Options:")
                    print("1. PredictPrecise")
                    print("2. Predict Again")
                    print("3. Start Server")
                    print("4. Show Visualisation")
                    print("5. Exit")
                    choice = input("Enter your choice (1, 2, or 3): ")

                    if choice == "1":
                        predictPrecise()
                    elif choice == "2":
                        predict()
                    elif choice == "3":
                        startSerialServer()
                    elif choice == "4":
                       # startVisualizationThread() 
                        pass
                    elif choice == "5":
                        print("Exiting...")
                        return
                    else:
                        print("Invalid choice. Retry!")

        elif choice == "2":
            print("Exiting...")
            return
        else:
            print("Invalid choice. Please enter 1 to predict or 2 to exit.")

if __name__ == "__main__":
    main_menu()
