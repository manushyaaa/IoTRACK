'''
app.py
Date: 2021-10-23 03:54:00
Python Version: 3.11.5
Functions: main_menu
'''

from utils import getTLE, getLocation, create_connection, predict, predictPrecise , getPredictedPath
from skyfield.api import wgs84, load
 

def main_menu():
    while True:
        print("Options:")
        print("1. Predict")
        print("2. Exit")
        print("3. Get Predicted Path")
                         

        choice = input("Enter your choice (1 or 2): ")

        menu = {
            "1": predict_menu,
            "2": exit_program,
            "3": getPredictedPath(1),
        }

        chosen_function = menu.get(choice)
        if chosen_function:
            chosen_function()
        else:
            print("Invalid choice. Please enter 1 to predict or 2 to exit.")

def predict_menu():
    prediction = predict()
    if not prediction.empty:
        while True:
            print("Options:")
            print("1. PredictPrecise")
            print("2. Predict Again")
            print("3. Exit")
            choice = input("Enter your choice (1, 2, or 3): ")

            predict_menu_options = {
                "1": predictPrecise,
                "2": lambda:predict(),   
                "3": exit_program
            }

            chosen_function = predict_menu_options.get(choice)
            if chosen_function:
                chosen_function()
                if choice == "3":
                    break
            else:
                print("Invalid choice. Retry!")

def exit_program():
    print("Exiting...")

if __name__ == "__main__":
    main_menu()

