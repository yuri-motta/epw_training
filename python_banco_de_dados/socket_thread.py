# -*- coding: utf-8 -*-

import MySQLdb as mdb
import sys
import socket
import time
from threading import Thread

# variaveis globais
HOST = '127.0.0.1'  # Endereco IP do Servidor
PORT = 4444  # Porta do Servidor
CONECTADO = False
id = "0"
X = "0"
Y = "0"


class com_socket(Thread):
    def __init__(self, num):
        Thread.__init__(self)
        self.num = num

    def run(self):
        global CONECTADO, tcp
        print "Thread iniciada"
        print self.num

        while CONECTADO == False:
            try:
                tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                dest = (HOST, PORT)
                tcp.connect(dest)
                print "Thread conectada com epw_control:  \n"
                CONECTADO = True

            except socket.error:
                print("A conexao com servidor socket falhou.")
                tcp.close()
                time.sleep(1)

    # METODO PARA ENVIAR MENSAGEM SOCKET
    def envia_msg(self):
        print "loop socket"
        global CONECTADO, X, Y, id, tcp
        while True:
            if CONECTADO == True:
                try:
                    self.id_atual = id

                    self.mensagem_enviada = "X;" + X + "%" + ";Y;" + Y + "%" + str('\n')
                    tcp.send(self.mensagem_enviada)
                    print('enviado: ' + self.mensagem_enviada)
                    self.id_anterior = self.id_atual
                    time.sleep(0.5)

                except socket.error:
                    tcp.close()

            else:
                print "Socket client nao conectado"
                time.sleep(1)



# instanciando objeto socket
conexao_socket = com_socket(1)
conexao_socket.start()  # inicia thread
conexao_socket.envia_msg()
