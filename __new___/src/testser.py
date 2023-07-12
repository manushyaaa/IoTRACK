import serial

# Open the serial connection
ser = serial.Serial('COM9', 9600)  # Replace 'COM9' with the appropriate COM port
ser.timeout = 1  # Set a timeout value (in seconds) for reading

try:
    # Send data
    data_to_send = b'Testing RX/TX connection'
    ser.write(data_to_send)

    # Receive data
    data_received = ser.readline()
    print("Received:", data_received.decode().strip())

except serial.SerialException as e:
    print("Serial port error: ", str(e))

finally:
    # Close the serial connection
    ser.close()
