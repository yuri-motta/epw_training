#!/usr/bin/python
# -*- coding: utf-8 -*-

import MySQLdb as mdb

con = mdb.connect('localhost', 'iepw', 'iepw', 'comandos');

with con:
    cur = con.cursor()
    cur.execute("INSERT INTO comandos_simples(comandos) VALUES ('X;2%;Y;-33%');")  # insere dados na tabela

    ver = cur.fetchone()  # o fetchone traz os dados de resposta do banco

    print ver
