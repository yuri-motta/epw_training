import json

json_string = '{"first_name": "Yuri", "last_name": "Silva"}'
parsed_json = json.loads(json_string)

print(parsed_json['first_name'])



d = {
    'first_name': 'Yasmin',
    'last_name': 'Motta',
    'titles': ['BDFL','Developer'],
}

print(json.dumps(d))
