#!/usr/bin/python
# -*- coding: utf-8 -*-

import MySQLdb as mdb

con = mdb.connect('localhost', 'iepw', 'iepw', 'comandos');

with con:

    cur = con.cursor()
    cur.execute("SELECT * FROM comandos_eeg")

    rows = cur.fetchall()

    for row in rows:
        print row