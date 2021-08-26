#!/usr/bin/env python3
import serial
import time

if __name__ == '__main__':
    try:
        ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    except:
        ser = serial.Serial('/dev/ttyACM1', 9600, timeout=1)
    ser.flush()
#     ser.write(b"wash\n")
#     time.sleep(5) # Wait for Arduino to load
#     ser.write(b"dry\n")
#     time.sleep(5)
#     ser.write(b"sterilize\n")
    
    while True:
        line = ser.readline().decode('utf-8').rstrip()
        print(line)
        


#     while True:
#         ser.write(b"dry\n")
#         line = ser.readline().decode('utf-8').rstrip()
#         print(line)
#         time.sleep(1)