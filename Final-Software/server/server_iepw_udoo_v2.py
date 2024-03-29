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
""" VERSAO COM VIDEO STREAMING AUTOMATICO"""

""" ARGUMENTO DE ENTRADA E O NOME DO USUARIO"""
""" EX: python udp_server yuri"""

nome_usuario = str(sys.argv[1])

"""CONSTANTES"""
# versao utilizando a alimentacao do regulador de tensao, com 4.8V no VCC
DAC_min = 101  # equivale a 1.5V
DAC_0 = 169  # equivale a 2.5V
DAC_max = 223  # equivale a 3.3V
max_variacao_pos = DAC_max - DAC_0  # intervalo maximo de variacao positiva 2.3V a 3.3V

max_variacao_neg = DAC_0 - DAC_min  # intervalo maximo de variacao negativa 2.3V a 1.3V

"""DADOS DE CONEXAO"""
HOST = "192.168.1.119"  # ip servidor comandos
PORT = 4444  # porta do servidor de comandos
video_port = 4444  # porta do video
http_port = 4444

"""COMUNICACAO SERIAL"""
ser = serial.Serial('/dev/ttyS0',115200)


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

        global socket_server, video_port, http_port
        f = open(nome_usuario + "_rtt" + ".dat", "w")
        c = open(nome_usuario + "_commands" + ".dat", "w")
        # now keep talking with the client

        #inicio do streaming por http
        self.url_http = "http://" + HOST + ":"+ str(http_port)
        subprocess.Popen(["ffmpeg", "-i", "/dev/video2", "-s", "640x480", "-r", "15", "-f", "mpegts", "-fflags","nobuffer", "-listen","1","%s" % self.url_http])

        try:
            while 1:
                # receive data from client (data, addr)
                d = socket_server.recvfrom(256)
                data = str(d[0])
                addr = d[1]

                if not data:
                    break

                # reply = 'OK...' + data
                # socket_server.sendto(reply, addr)


                print 'Message[' + addr[0] + ':' + str(addr[1]) + '] - ' + data.strip()
                # EXEMPLO DE MSG RECEBIDA: 'X=-30%,Y=-50%'

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
                    ser.write('x')
                    ser.write(';')
                    ser.write(chr(dacX))
                    ser.write('y')
                    ser.write(';')
                    ser.write(chr(dacY))

                    """SALVANDO O HISTORICO DE COMANDOS EM ARQUIVO"""
                    ts = time.time()
                    ano = datetime.datetime.fromtimestamp(ts).strftime('%Y')
                    mes = datetime.datetime.fromtimestamp(ts).strftime('%m')
                    dia = datetime.datetime.fromtimestamp(ts).strftime('%d')
                    hora = datetime.datetime.fromtimestamp(ts).strftime('%H')
                    minutos = datetime.datetime.fromtimestamp(ts).strftime('%M')
                    segundos = datetime.datetime.fromtimestamp(ts).strftime('%S')

                    c.write("IP: " + addr[0] + " Command: " + str(int(X)) + " " + str(int(Y)) + " " + " TS: " + str(ts) + " " + str(ano) + " " + str(
                        mes) + " " + str(dia) + " " + str(hora) + " " + str(minutos) + " " + str(segundos) + "\n")

                if 'RTT' in data:
                    """SALVANDO O HISTORICO RTT EM ARQUIVO"""
                    try:
                        f.write("IP: " + addr[0] + " " + data + "\n")

                    except ValueError:
                        pass


                if 'stop' in data:
                    """FINALIZANDO O TREINO"""
                    print "-------------------------"
                    print "The training has finished"
                    print "-------------------------"

                    f.close()
                    c.close()

                else:
                    print "Message different from pattern: " + data

        except KeyboardInterrupt or ValueError:
            f.close()
            c.close()
            pass


server = Udp_server()
server.run()
