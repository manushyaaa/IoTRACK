import time
import pyserial

ser = pyserial.Serial('COM1', 115200, timeout=0.050)
count = 0

while True:
    ser.write(f'Sent {count} time(s)'.encode())  # Encode the string as bytes before sending
    time.sleep(1)
    count += 1
