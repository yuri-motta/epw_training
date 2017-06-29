import socket
import sys
import thread
import re
import time
import os
import serial

"""DADOS DE CONEXAO"""
HOST = "192.168.1.144"  # Symbolic name meaning all available interfaces
PORT = 4444  # Arbitrary non-privileged port

"""CONSTANTES"""
# versao utilizando a alimentacao do regulador de tensao, com 4.8V no VCC
DAC_min = 88 #equivale a 1.3V
DAC_0 = 155 #equivale a 2.3V
DAC_max = 223 #equivale a 3.3V
max_variacao_pos = DAC_max - DAC_0 #intervalo maximo de variacao positiva 2.3V a 3.3V
max_variacao_neg = DAC_0 - DAC_min #intervalo maximo de variacao negativa 2.3V a 1.3V

"""COMUNICACAO SERIAL"""
ser = serial.Serial('/dev/ttyS0',115200)


def conectado(con, cliente):
    print 'Conectado por', cliente

    while True:
        data = con.recv(1024)
        if not data: break
        print cliente, data

        """TRATAMENTO DA MENSAGEM RECEBIDA"""
        vetor_mensagem = data.split(",", 1)

        sinal_X = '-' in vetor_mensagem[0]
        sinal_Y = '-' in vetor_mensagem[1]

        vetor_valores = re.findall('\d+', data)

        X = float(vetor_valores[0])
        Y = float(vetor_valores[1])

        if sinal_X == True:  # caso X seja negativo
            X = X * (-1)

        if sinal_Y == True:  # caso Y seja negativo
            Y = Y * (-1)

        """CONVERSAO DO DAC_X PARA 12BIT"""

        if X > 0:
            porcentX = X / 100
            dacX = DAC_0 + round(porcentX * max_variacao_pos)

        if X == 0:
            dacX = DAC_0

        if X < 0:
            porcentX = abs(X / 100)  # modulo do numero dividido por 100
            dacX = DAC_0 - round(porcentX * max_variacao_neg)

        dacX = int(dacX)

        """CONVERSAO DO DAC_Y PARA 12BIT"""
        if Y > 0:
            porcentY = Y / 100
            dacY = DAC_0 + round(porcentY * max_variacao_pos)

        if Y == 0:
            dacY = DAC_0

        if Y < 0:
            porcentY = abs(Y / 100)  # modulo do numero dividido por 100
            dacY = DAC_0 - round(porcentY * max_variacao_neg)
        dacY = int(dacY)

        """MOSTRANDO OS VALORES DE DACX E DACY NA TELA"""
        print 'dacX'
        print dacX

        print 'dacY'
        print dacY

        """ENVIANDO A MENSAGEM SERIAL"""
        ser.write('x')
        ser.write(';')
        ser.write(chr(dacX))
        ser.write('y')
        ser.write(';')
        ser.write(chr(dacY))
        time.sleep(0.05)


        #global dacX_porta
        #global dacY_porta

        #dacX_porta.set_voltage(dacX, True)
        #dacY_porta.set_voltage(dacY, True)

    print 'Finalizando conexao do cliente', cliente
    con.close()
    thread.exit()

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

orig = (HOST, PORT)

tcp.bind(orig)
tcp.listen(1)

while True:
    con, cliente = tcp.accept()
    thread.start_new_thread(conectado, tuple([con, cliente]))

tcp.close()