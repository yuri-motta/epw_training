import socket
import sys
import re
import thread
from threading import Thread
import time
import os
import serial

"""CONSTANTES"""
# versao utilizando a alimentacao do regulador de tensao, com 4.8V no VCC
DAC_min = 88 #equivale a 1.3V
DAC_0 = 155 #equivale a 2.3V
DAC_max = 223 #equivale a 3.3V
max_variacao_pos = DAC_max - DAC_0 #intervalo maximo de variacao positiva 2.3V a 3.3V
max_variacao_neg = DAC_0 - DAC_min #intervalo maximo de variacao negativa 2.3V a 1.3V

"""DADOS DE CONEXAO"""
HOST = "192.168.1.144"  # Symbolic name meaning all available interfaces
PORT = 4444  # Arbitrary non-privileged port

"""COMUNICACAO SERIAL"""
#ser = serial.Serial('/dev/ttyS0',115200)

"""CLASSE DO SERVIDOR TCP"""
#class Tcp_server(Thread):
def __init__(self):
    global socket_server
    """Create socket server and bind to ip and port"""
    Thread.__init__(self)
    try:
        socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print 'Socket created'
    except socket.error, msg:
        print 'Failed to create socket. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
        sys.exit()

    # Bind socket to local host and port
    try:
        socket_server.bind((HOST, PORT))
    except socket.error, msg:
        print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
        sys.exit()

    print 'Socket bind complete'
    socket_server.listen(10)
    print 'now socket tcp is listening'

def conectado(con, cliente):

    print 'Conectado por', cliente

    while True:
        msg = con.recv(1024)
        if not msg: break
        print cliente, msg
    print 'Finalizando conexao do cliente', cliente
    con.close()
    thread.exit()

def run(self):
    """receive and send messages"""

    global socket_server

    # now keep talking with the client
    while 1:

        con, cliente = socket_server.accept()
        print 'Connected with ' + con[0] + ':' + str(cliente[1])
        thread.start_new_thread(conectado, tuple([con, cliente])
        #EXEMPLO DE MSG RECEBIDA: 'X=-30%,Y=-50%'
#server = Tcp_server()
#server.run()

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

        """MUDANDO A TENSAO DOS DACS"""
        global dacX_porta
        global dacY_porta

        dacX_porta.set_voltage(dacX, True)
        dacY_porta.set_voltage(dacY, True)

