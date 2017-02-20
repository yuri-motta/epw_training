#!/usr/bin/python
# -*- coding: utf-8 -*-

import MySQLdb as mdb

con = mdb.connect('localhost', 'iepw', 'iepw', 'comandos')


with con:

    cur = con.cursor(mdb.cursors.DictCursor)
    cur.execute("SELECT * FROM comandos_eeg ORDER BY id DESC LIMIT 1")

    rows = cur.fetchall()

    for row in rows:
        id = row["id"]
        X = row["X"]
        Y = row["Y"]


print id,X,Y
