#!/usr/bin/python
# -*- coding: utf-8 -*-

import MySQLdb as mdb
import sys
import socket
import time
from threading import Thread


#variaveis globais
HOST = '192.168.100.191'  # Endereco IP do Servidor
PORT = 4444  # Porta do Servidor
CONECTADO = False
id = 0
X = "0"
Y = "0"
id_anterior = 0  # iniciando o id anterior


##### classe socket client
class com_socket(Thread):
    def __init__(self,num):
        Thread.__init__(self)
        self.num = num

    def conecta_com_servidor(self):
        global CONECTADO, tcp

        try:
            self.dest = (HOST, PORT)
            CONECTADO = True
            tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            tcp.connect(self.dest)
            print "Thread conectada com epw_control:  \n"

        except socket.error:
            CONECTADO = False
            print("A conexao com servidor socket falhou.")


    # METODO PARA ENVIAR MENSAGEM SOCKET
    def envia_msg(self):
        global CONECTADO,X, Y, id, id_anterior,tcp

        self.id_atual = id
        print "- id atual: " + str(self.id_atual)
        print "- id anterior: " + str(id_anterior)
        if self.id_atual != id_anterior:
            try:
                id_anterior = self.id_atual
                self.mensagem_enviada = "X;" + X + "%" + ";Y;" + Y + "%" + str('\n')
                tcp.send(self.mensagem_enviada) #envia comando a ser executado
                print('enviado: ' + self.mensagem_enviada)
                time.sleep(3)
                self.mensagem_stop = "X;" + "0" + "%" + ";Y;" + "0" + "%" + str('\n')
                tcp.send(self.mensagem_stop) #envia comando de parada
                print('enviado: ' + self.mensagem_enviada)

            except socket.error:
                print "falha no envio da mensagem ao servidor socket"
                CONECTADO = False

        else:
            print "nenhum dado novo no banco \n"
            time.sleep(1)


    def reconectar(self):
        global CONECTADO

        try:
            self.conecta_com_servidor()
            CONECTADO = True
        except socket.error:
            print("nova tentativa de conexao em 5 segundos \n")
            CONECTADO = False
        time.sleep(3)

##### classe mysql
class com_msql(Thread):
    def __init__(self,num):
        Thread.__init__(self)
        self.num = num

    # METODO PARA LER A BASE DE DADOS E ATUALIZAR A DATA DE RECEBIMENTO
    def read_upd_database(self):
        global id, X, Y
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

                self.cur = self.con.cursor()
                self.cur.execute("UPDATE  `comandos`.`comandos_eeg` SET  `date_received` =  NOW() WHERE  `comandos_eeg`.`id` =%s;" % id)  # atualiza dados na tabela
                time.sleep(0.5)  # intervalo de leitura do banco de dados

        except mdb.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])
            sys.exit(1)

        finally:
            if self.con:
                self.con.close()

# instanciando objeto socket
conexao_socket = com_socket(1)
conexao_socket.conecta_com_servidor()
conexao_msql = com_msql(1) #inicia thread msql


while True:

    if CONECTADO==True:
        try:
            conexao_msql.read_upd_database()
            conexao_socket.envia_msg()
        except:
            socket.error
            CONECTADO==False

    if CONECTADO==False:
        conexao_socket.reconectar()



