#!/usr/bin/python3

import requests

from flask import Flask, Response

app = Flask(__name__)

@app.route('/metrics', methods = ['GET'])
def metrics():
	resp = requests.get('http://nube.lavacro.net:8053/json/v1/server')
	data = resp.json()['qtypes']
	l = ['bind_up 1']

	for qtype, val in data.items():
		l.append(f'bind_incoming_queries_total{{type="{qtype}"}} {val}')
	l.append('\n')
	return Response('\n'.join(l), content_type='text/plain')

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=9119)
