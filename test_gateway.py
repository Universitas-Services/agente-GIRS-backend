# -*- coding: utf-8 -*-
import urllib.request
import json

url = 'https://gateway-529295899189.us-east1.run.app/api/chat'
query = 'sobre ORDENANZA SOBRE GESTIÓN INTEGRAL DE DESECHOS Y RESIDUOS SÓLIDOS DEL MUNICIPIO SAN CRISTÓBAL dime el articulo 3'
data = json.dumps({'message': query, 'session_id': 'session_test'}).encode('utf-8')
headers = {'Content-Type': 'application/json'}
req = urllib.request.Request(url, data=data, headers=headers)

try:
    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read().decode('utf-8'))
        print(result.get('response', result))
except Exception as e:
    print(f'Error: {e}')
