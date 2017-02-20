import json
import urllib2

data = {
        'ids': [12, 3, 4, 5, 6]
}


req = urllib2.Request('http://127.0.0.1/iepw_interface2.php')
req.add_header('Content-Type', 'application/json')
response = urllib2.urlopen(req, json.dumps(data))