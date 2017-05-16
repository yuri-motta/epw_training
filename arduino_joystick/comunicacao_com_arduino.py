import serial
from serial import SerialException
import time

"""CONSTANTES"""
center_value_X = 481
center_value_Y = 507

"""INICIALIZACAO DE VARIAVEIS"""
X = "0"
Y = "0"

"""CONEXAO UART USB"""
arduino = serial.Serial('/dev/ttyUSB0', 9600)

while True:
	try:
        data = arduino.readline(5)
        vetor_mensagem = data.split(":", 1)
        if vetor_mensagem[0] == "X":
            X = vetor_mensagem[1]
        if vetor_mensagem[0] == "Y":
            Y = vetor_mensagem[1]

        mensagem_final = "X:" + X + ",Y:" + Y
        print mensagem_final


	except SerialException:
		print "falha na conexao USB"

