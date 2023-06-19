from machine import Pin
import esp
import gc
import network

try:
  import usocket as socket
except:
  import socket

 
esp.osdebug(None)

 
gc.collect()
 
station = network.WLAN(network.STA_IF)

station.active(True)
station.connect('BlackRose_G', 'ManMan123')

while station.isconnected() == False:
  pass

print('Connection successful')
print(station.ifconfig())

led = Pin(2, Pin.OUT)
