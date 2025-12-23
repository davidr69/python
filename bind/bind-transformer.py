#!/usr/bin/python3

import requests

from flask import Flask

app = Flask(__name__)

def wrap(endpoint):
	resp = requests.get(endpoint)
	data = str(resp.content)
	lines = data.split('\\n')
	lf = '\n'

	new_resp = f'{lines[0]}{lf}{lines[1]}{lf}<isc><bind>{lines[2]}</bind></isc>{lf}'
	return new_resp


@app.route('/xml/v3/server', methods = ['GET'])
def server():
	return wrap('http://127.0.0.1:8053')


@app.route('/xml/v3/status', methods = ['GET'])
def status():
	return wrap('http://127.0.0.1:8053/xml/v3/status')


@app.route('/xml/v3/zones', methods = ['GET'])
def zones():
        return wrap('http://127.0.0.1:8053/xml/v3/zones')


@app.route('/xml/v3/tasks', methods = ['GET'])
def tasks():
        return wrap('http://127.0.0.1:8053/xml/v3/tasks')

if __name__ == '__main__':
	app.run(host='127.0.0.1', port=8054)
