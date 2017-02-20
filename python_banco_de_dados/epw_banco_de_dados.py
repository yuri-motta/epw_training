#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import urllib2


# Coletar dados do servidor para executar na cadeira
req = urllib2.Request('http://127.0.0.1/iepw_interface.php')
req.add_header('Content-Type', 'application/json')
d = {
    'first_name': 'Yuri',
    'last_name': 'Motta',
    'titles': ['BDFL','Developer'],
}
response = urllib2.urlopen(req, json.dumps(d))  # requisição dos dados do banco
response = response.read()

