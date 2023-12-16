# (1, 3) 12:28:12 170.32 -75.8 ISS_(ZARYA) NEU 0 x

import serial , time
from datetime import datetime as dt 



MOV_BIT = 'FWD' 

ser = serial.Serial( 'COM3' , 115200 )
 
 
# for i in range(331 ,360, 1) : 
#     packet = f'{dt.now().strftime("%H:%M:%S")} {i} 0 ISS_(ZARYA) {MOV_BIT} 0 x\n'
#     ser.write(packet.encode('utf-8'))
#     print(packet)
#     time.sleep(2)

list1 = [353 , 354 , 355 , 356 , 357 , 358 , 359 , 360 , 0 , 1 , 2, 3, 4]
list2 = [3 ,2  , 1 , 0 , 359 , 358 , 357 , 356 , 355 , 354 , 353 , 352 , 351]
for i in list2:
    packet = f'{dt.now().strftime("%H:%M:%S")} {i} 0 ISS_(ZARYA) {MOV_BIT} 0 x\n'
    ser.write(packet.encode('utf-8'))
    print(packet)
    time.sleep(6)