import socket
import sys
import re
import subprocess
from threading import Thread
import time
import os
import serial
import datetime


""" NOVA VERSAO DO SERVIDOR"""

""" ARGUMENTO DE ENTRADA E O NOME DO USUARIO"""
""" EX: python udp_server yuri"""

nome_usuario = str(sys.argv[1])

"""CONSTANTES"""
# versao utilizando a alimentacao do regulador de tensao, com 4.8V no VCC
DAC_min = 88 #equivale a 1.3V
DAC_0 = 155 #equivale a 2.3V
DAC_max = 223 #equivale a 3.3V
max_variacao_pos = DAC_max - DAC_0 #intervalo maximo de variacao positiva 2.3V a 3.3V

max_variacao_neg = DAC_0 - DAC_min #intervalo maximo de variacao negativa 2.3V a 1.3V

"""DADOS DE CONEXAO"""
HOST = "192.168.1.117"  # Symbolic name meaning all available interfaces
PORT = 4444  # Arbitrary non-privileged port

"""COMUNICACAO SERIAL"""
#ser = serial.Serial('/dev/ttyS0',115200)


"""CLASSE DO SERVIDOR UDP"""
class Udp_server(Thread):
    def __init__(self):
        global socket_server
        """Create socket server and bind to ip and port"""
        Thread.__init__(self)
        try:
            socket_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
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

    def run(self):
        """receive and send messages"""

        global socket_server
        f = open(nome_usuario + "_rtt" + ".dat", "w")
        c = open(nome_usuario + "_commands" + ".dat", "w")
        # now keep talking with the client

        try:
            while 1:
                # receive data from client (data, addr)
                d = socket_server.recvfrom(256)
                data = str(d[0])
                addr = d[1]

                if not data:
                    break

                #reply = 'OK...' + data
                #socket_server.sendto(reply, addr)


                print 'Message[' + addr[0] + ':' + str(addr[1]) + '] - ' + data.strip()
                #EXEMPLO DE MSG RECEBIDA: 'X=-30%,Y=-50%'

                if '%' in data:

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
                    #ser.write('x')
                    #ser.write(';')
                    #ser.write(chr(dacX))
                    #ser.write('y')
                    #ser.write(';')
                    #ser.write(chr(dacY))
                    """SALVANDO O HISTORICO DE COMANDOS EM ARQUIVO"""
                    c.write("IP: " + addr[0] + " Command: " + str(int(X)) + " " + str(int   (Y)) + "\n")

                else:
                    """SALVANDO O HISTORICO RTT EM ARQUIVO"""
                    f.write("IP: " + addr[0] + " " + data + "\n")

        except KeyboardInterrupt:
            f.close()
            pass

server = Udp_server()
server.run()
