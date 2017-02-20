#!/usr/bin/python
# -*- coding: utf-8 -*-

import MySQLdb as mdb
import sys

try:
    con = mdb.connect('localhost', 'iepw', 'iepw', 'comandos') #connecta ao database


    cur = con.cursor() #criacao de cursor object - usado para acessar os dados do banco
    cur.execute("SELECT * FROM `comandos_eeg`;") #seleciona todos itens da tabela


    ver = cur.fetchall() # o fetchone traz os dados de resposta do banco - 1 linha

    print ver

except mdb.Error, e:

    print "Error %d: %s" % (e.args[0], e.args[1])
    sys.exit(1)

finally:

    if con:
        con.close()
