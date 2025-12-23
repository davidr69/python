#!/usr/bin/python3

from prometheus_client import start_http_server, REGISTRY, Counter
import requests

class BindExporter:
	def __init__(self, bind_stats_url):
		self.bind_stats_url = bind_stats_url
		self.qtype_counter = {}

	def collect(self):
		resp = requests.get(self.bind_stats_url)
		json = resp.json()
		data = json['qtypes']

		for qtype, count in data.items():
			if qtype not in self.qtype_counter:
				print(f'{self.qtype_counter}')
				self.qtype_counter[qtype] = Counter(
						'bind_incoming_queries_total', 
						'Total incoming queries per type',
						['type']
				)
				self.qtype_counter[qtype].labels(type=qtype).inc(count)
		for counter in self.qtype_counter.values():
			yield counter


if __name__ == "__main__":
	bind_stats_url = 'http://nube:8053/json/v1/server'

	exporter = BindExporter(bind_stats_url)
	REGISTRY.register(exporter)

	start_http_server(9119)

	print('Started bind exporter')

	while True:
		pass
