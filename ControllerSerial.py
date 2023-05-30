from serial.tools import list_ports
import serial
import time

ports = list_ports.comports()
for port in ports: print(port)

ser = serial.Serial('COM9', 100)

DEAD_ZONE = 25
RES_OFFSET = 512 #1023/2

#reset the arduino
ser.setDTR(False)
time.sleep(1)
ser.flushInput()
ser.setDTR(True)

def read_data():
    kmax = 1
    for k in range(kmax):
        try:
            data = ser.readline().decode().rstrip()
            
            values = list(map(int, data[1:].replace('x', ' ').replace('y', ' ').split()))
            values = [x - RES_OFFSET for x in values[-2:]]
            x_value, y_value, b_value = [0 if abs(x) < DEAD_ZONE else x for x in values] + [int(data[1:].split('x')[0])]
            values = [x_value, y_value, b_value]

        except:
            print("Serial connection lost. Reconnecting...")
            ser.close() # close the serial port
            ser.open() # reopen the serial port 
    return values
