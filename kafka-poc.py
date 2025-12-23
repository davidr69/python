#!/usr/bin/python3

import os
import struct
import datetime
from kafka import KafkaConsumer

KAFKA_BOOTSTRAP_SERVERS = os.environ.get("KAFKA_BOOTSTRAP_SERVERS", "kafka.lavacro.net:9092")
KAFKA_TOPIC_TEST = os.environ.get("KAFKA_TOPIC_TEST", "finances")
KAFKA_API_VERSION = os.environ.get("KAFKA_API_VERSION", "7.3.1")

class MyKafkaObject:
	def __init__(self, payload, number):
		self.payload = payload
		self.number = number

	def __repr__(self):
		return '{"number":"%s","payload":"%s"}' % (self.number, self.payload)

def deserialize_my_object(serialized_data):
	try:
		# Unpack binary data using struct module - https://docs.python.org/3/library/struct.html
		number, string_size = struct.unpack('!qi', serialized_data[:12])
		payload = serialized_data[12:].decode('utf-8')
		return MyKafkaObject(payload=payload, number=datetime.datetime.fromtimestamp(number/1000.0))
	except Exception as e:
		print(f"Error during deserialization: {e}")


consumer = KafkaConsumer(
	KAFKA_TOPIC_TEST,
	bootstrap_servers=[KAFKA_BOOTSTRAP_SERVERS],
	api_version=KAFKA_API_VERSION,
	auto_offset_reset="earliest",
	enable_auto_commit=True
)

for message in consumer:
	print('Waiting ...')
	#print(message.value.decode("utf-8"))
	deserialized = deserialize_my_object(message.value)
	print(f'Object: {deserialized}')
