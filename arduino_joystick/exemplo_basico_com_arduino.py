import serial

ser = serial.Serial('/dev/ttyUSB0', 9600)
while True:
    print ser.readline(10) #le ate 10 bytes, senao timeout
