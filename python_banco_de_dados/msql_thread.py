#!/usr/bin/python
# -*- coding: utf-8 -*-

import MySQLdb as mdb
import sys
import socket
import time
from threading import Thread

# variaveis globais
HOST = '127.0.0.1'  # Endereco IP do Servidor
PORT = 4444  # Porta do Servidor
CONECTADO = True
id = "0"
X = "0"
Y = "0"

class com_msql(Thread):
    def __init__(self, num):
        Thread.__init__(self)
        self.num = num

    # METODO PARA LER A BASE DE DADOS E ATUALIZAR A DATA DE RECEBIMENTO
    def read_upd_database(self):
        global CONECTADO
        global id, X, Y
        while True:
            if CONECTADO == True:
                try:
                    self.con = mdb.connect('localhost', 'iepw', 'iepw', 'comandos')  # conecta ao banco de dados
                    with self.con:
                        self.cur_dic = self.con.cursor(mdb.cursors.DictCursor)
                        self.cur_dic.execute("SELECT * FROM comandos_eeg ORDER BY id DESC LIMIT 1")
                        self.rows = self.cur_dic.fetchall()

                        for self.row in self.rows:
                            id = self.row["id"]
                            X = self.row["X"]
                            Y = self.row["Y"]

                        print id, X, Y
                        self.string_id = id
                        print self.string_id

                        if self.string_id == 64:
                            print "igual ao anterior"

                        self.cur = self.con.cursor()
                        self.cur.execute(
                            "UPDATE  `comandos`.`comandos_eeg` SET  `date_received` =  NOW() WHERE  `comandos_eeg`.`id` =%s;" % id)  # atualiza dados na tabela
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


# instanciando objeto msql
conexao_msql = com_msql(1)  # inicia thread msql
conexao_msql.start() #acessa o banco

# lendo dados do banco e salvando em variaveis locais
conexao_msql.read_upd_database()

