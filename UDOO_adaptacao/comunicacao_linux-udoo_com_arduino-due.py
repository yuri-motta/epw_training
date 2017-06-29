import serial
from threading import Thread
import socket
import sys

# PORTA SERIAL UTILIZADA
ser = serial.Serial('/dev/ttyS0', 9600)

while True:
    data = ser.readline(5)
    print data