from serial.tools import list_ports
import serial
import time

ports = list_ports.comports()
for port in ports: print(port)

ser = serial.Serial('COM9', 100)

dead_zone = 25

#reset the arduino
ser.setDTR(False)
time.sleep(1)
ser.flushInput()
ser.setDTR(True)

def readData():
    kmax = 1
    for k in range(kmax):
        try:
            data = ser.readline()
            data = data.decode().rstrip()
            Verdier = data.split('x')[1].split('y')
            Verdier.append(int(data.split('x')[0][1:]))
            #print(data)

            Verdier[0], Verdier[1] = int(Verdier[0]) - 1023 // 2, int(Verdier[1]) - 1023 // 2

            Verdier[0] = 0 if Verdier[0] < dead_zone and Verdier[0] > -dead_zone else Verdier[0]
            Verdier[1] = 0 if Verdier[1] < dead_zone and Verdier[1] > -dead_zone else Verdier[1]

            Verdier[0], Verdier[1] = Verdier[0] * 2, Verdier[1] * 2

        except:
            print("Serial connection lost. Reconnecting...")
            ser.close() # close the serial port
            ser.open() # reopen the serial port 
    return Verdier

print(readData())