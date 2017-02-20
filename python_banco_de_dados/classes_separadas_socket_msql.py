#!/usr/bin/python
# -*- coding: utf-8 -*-

import MySQLdb as mdb
import sys
import socket
import time
from threading import Thread


#variaveis globais
HOST = '127.0.0.1'  # Endereco IP do Servidor
PORT = 4444  # Porta do Servidor
CONECTADO = False
id = 0
X = "0"
Y = "0"
id_anterior = 0  # iniciando o id anterior
class com_socket(Thread):
    def __init__(self,num):
        Thread.__init__(self)
        self.num = num

    def run(self):
        global CONECTADO, tcp
        print "Thread iniciada"
        print self.num

        while CONECTADO==False:
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
        global CONECTADO, X, Y, id, id_anterior,tcp
        if CONECTADO == True:
            try:
                self.id_atual = id
                print "id atual" + str(self.id_atual)
                print "id anterior" + str(id_anterior)
                if self.id_atual != id_anterior:
                    self.mensagem_enviada = "X;" + X + "%" + ";Y;" + Y + "%" + str('\n')
                    tcp.send(self.mensagem_enviada)
                    print('enviado: ' + self.mensagem_enviada)
                    id_anterior = self.id_atual
                    time.sleep(0.5)
                else:
                    print "nenhum dado novo no banco"
                    time.sleep(1)

            except socket.error:
                tcp.close()

        else:
            print "Socket client nao conectado"
            time.sleep(1)

class com_msql(Thread):
    def __init__(self,num):
        Thread.__init__(self)
        self.num = num

    # METODO PARA LER A BASE DE DADOS E ATUALIZAR A DATA DE RECEBIMENTO
    def read_upd_database(self):
        global CONECTADO
        global id, X, Y
        if CONECTADO==True:
            try:
                self.con = mdb.connect('localhost','iepw','iepw', 'comandos') #conecta ao banco de dados
                with self.con:
                    self.cur_dic=self.con.cursor(mdb.cursors.DictCursor)
                    self.cur_dic.execute("SELECT * FROM comandos_eeg ORDER BY id DESC LIMIT 1")
                    self.rows = self.cur_dic.fetchall()

                    for self.row in self.rows:
                        id = self.row["id"]
                        X = self.row["X"]
                        Y = self.row["Y"]

                    print id, X, Y

                    self.cur = self.con.cursor()
                    self.cur.execute("UPDATE  `comandos`.`comandos_eeg` SET  `date_received` =  NOW() WHERE  `comandos_eeg`.`id` =%s;" % id)  # atualiza dados na tabela
                    time.sleep(0.5)  # intervalo de leitura do banco de dados

            except mdb.Error, e:

                print "Error %d: %s" % (e.args[0], e.args[1])
                sys.exit(1)

            finally:
                if self.con:
                    self.con.close()

        else:
            print "aguardando a conexao com o epw_control para realizar a leitura do banco de dados online"
            time.sleep(1)


# instanciando objeto socket
conexao_socket = com_socket(1)
conexao_msql = com_msql(1) #inicia thread msql
conexao_socket.start() #inicia conexao socket


while True:
    conexao_msql.read_upd_database()
    conexao_socket.envia_msg()
