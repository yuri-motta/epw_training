#!/usr/bin/python
# -*- coding: utf-8 -*-

import socket
import time
from threading import Thread

global HOST
global PORT

HOST = '127.0.0.1'  # Endereco IP do Servidor
PORT = 4444  # Porta do Servidor

class Conecta_epw_control(Thread):
    def __init__(self,num):
        Thread.__init__(self)
        self.num = num

    def run(self):
        print "Thread iniciada"
        print self.num
        global CONECTADO
        CONECTADO = False

        while CONECTADO==False:
            try:
                tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                dest = (HOST, PORT)
                tcp.connect(dest)
                print "Thread conectada com epw_control:  \n"
                CONECTADO = True

            except socket.error:
                print('Erro','A conexão com servidor epw_control falhou. \n')
                tcp.close()
                time.sleep(1)


conexao_socket = Conecta_epw_control(1)
conexao_socket.start()

# class envia_msg_robotino(object):
#     def __init__(self, message):
#         self.msg = message
#         # self.txt = text
#         if CONECTAROBOTINO == True:
#             try:
#                 SOCKET_ROBO.send(bytes(self.msg))
#
#             except socket.error:
#                 pass
