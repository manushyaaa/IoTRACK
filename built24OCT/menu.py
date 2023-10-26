 
from prediction import Prediction
from serial_server import SerialServer

class MainMenu:
    def run(self):
        while True:
            print("Options:")
            print("1. Predict")
            print("2. Exit")

            choice = input("Enter your choice (1 or 2): ")

            if choice == "1":
                prediction_menu = PredictionMenu()
                prediction_menu.run()
            elif choice == "2":
                print("Exiting...")
                return
            else:
                print("Invalid choice. Please enter 1 to predict or 2 to exit.")

class PredictionMenu:
    def run(self):
        while True:
            print("Options:")
            print("1. Predict")
            print("2. Predict Precise")
            print("3. Start Server")
            print("4. Show Visualization")
            print("5. Back to Main Menu")
            print("6. Exit")

            choice = input("Enter your choice (1, 2, 3, 4, 5, or 6): ")

            if choice == "1":
                prediction = Prediction()
                prediction.predict()
            elif choice == "2":
                prediction = Prediction()
                prediction.predict_precise()
            elif choice == "3":
                server = SerialServer()
                server.start_server()
            elif choice == "4":
                # Add code for visualization
                pass
            elif choice == "5":
                return
            elif choice == "6":
                print("Exiting...")
                exit()
            else:
                print("Invalid choice. Retry!")
