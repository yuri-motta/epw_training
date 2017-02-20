#!/usr/bin/python
# -*- coding: utf-8 -*-

import MySQLdb as mdb
import sys
import socket
import time
from threading import Thread

HOST = '127.0.0.1'  # Endereco IP do Servidor
PORT = 4444  # Porta do Servidor

class comunicacao_epw(Thread):
    def __init__(self,num):
        Thread.__init__(self)
        self.num = num

    def run(self):
        print "Thread iniciada"
        print self.num
        global CONECTADO,tcp
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


    # METODO PARA LER A BASE DE DADOS E ATUALIZAR A DATA DE RECEBIMENTO
    def read_upd_database(self):
        global id, X, Y
        try:
            self.con = mdb.connect('localhost','iepw','iepw', 'comandos')

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

        except mdb.Error, e:

            print "Error %d: %s" % (e.args[0], e.args[1])
            sys.exit(1)

        finally:
            if self.con:
                self.con.close()

    # METODO PARA ENVIAR MENSAGEM SOCKET
    def envia_msg(self):
        if CONECTADO == True:
            try:
                self.mensagem_enviada = "X;" + X + "%" + ";Y;" + Y + "%" + str('\n')
                tcp.send(self.mensagem_enviada)
                print('enviado: ' + self.mensagem_enviada)

            except socket.error:
                tcp.close()
            else:
                print "Falha na conexão com o servidor \n"


conexao_socket = comunicacao_epw(1)
conexao_socket.start()
conexao_socket.read_upd_database()
conexao_socket.envia_msg()

