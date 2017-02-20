#!/usr/bin/python
# -*- coding: utf-8 -*-

import MySQLdb as mdb
import sys

try:
    con = mdb.connect('localhost', 'iepw', 'iepw', 'comandos') #connecta ao database

    with con:
        cur = con.cursor()
        cur.execute("INSERT INTO comandos_eeg(X,Y,date_executed) VALUES ('100','50',NOW());")  # insere dados na tabela

        cur.execute("UPDATE  `comandos`.`comandos_eeg` SET  `date_executed` =  NOW() WHERE  `comandos_eeg`.`id` =55;")# atualiza dados na tabela

        ver = cur.fetchone()  # o fetchone traz os dados de resposta do banco - OBS-O INSERT DO BANCO NÃO TEM RESPOSTA

        print ver

except mdb.Error, e:

    print "Error %d: %s" % (e.args[0], e.args[1])
    sys.exit(1)

finally:

    if con:
        con.close()