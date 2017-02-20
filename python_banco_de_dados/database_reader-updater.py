#!/usr/bin/python
# -*- coding: utf-8 -*-

import MySQLdb as mdb
import sys

try:
    con = mdb.connect('localhost', 'iepw', 'iepw', 'comandos') #connecta ao database

    with con:

        ## LEITURA DO DATABASE / SALVANDO INFORMACOES EM VARIAVEIS LOCAIS
        cur_dic = con.cursor(mdb.cursors.DictCursor)
        cur_dic.execute("SELECT * FROM comandos_eeg ORDER BY id DESC LIMIT 1")

        rows = cur_dic.fetchall()

        for row in rows:
            id = row["id"]
            X = row["X"]
            Y = row["Y"]

        print id, X, Y

        ## ATUALIZA A DATA DE EXECUCAO DO CODIGO NA TABELA
        cur = con.cursor()
        cur.execute("UPDATE  `comandos`.`comandos_eeg` SET  `date_executed` =  NOW() WHERE  `comandos_eeg`.`id` =%s;" %id)# atualiza dados na tabela


except mdb.Error, e:

    print "Error %d: %s" % (e.args[0], e.args[1])
    sys.exit(1)

finally:

    if con:
        con.close()