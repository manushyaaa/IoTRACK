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
list3 = [359 , 358 , 357 , 356 , 355 , 354 , 353 , 352 , 351 , 350 , 349 , 348 , 347]
list33 = [346 , 345 , 344 , 343 , 342 , 341 , 340 , 339 , 338 , 337 , 336 , 335 , 334 , 333 , 332 , 331 , 330 ]
list4 = [ 1 , 2 , 3 , 4 , 5 , 6 , 7 , 8 , 9 , 10]
list5 = [ 3 , 6 , 9 , 12 , 15 , 18 , 21 , 24 , 27 , 30]
list6 = [ 45 , 43 , 41 , 39 , 37 , 35 , 33 , 31 , 29 , 27]


for i in range(359 , 325 , -4):
    packet = f'{dt.now().strftime("%H:%M:%S")} {i} 0 ISS_(ZARYA) {MOV_BIT} 0 x\n'
    ser.write(packet.encode('utf-8'))
    print(packet)
    time.sleep(5)

# for i in list33:
#     packet = f'{dt.now().strftime("%H:%M:%S")} {i} 0 ISS_(ZARYA) {MOV_BIT} 0 x\n'
#     ser.write(packet.encode('utf-8'))
#     print(packet)
#     time.sleep(5)
