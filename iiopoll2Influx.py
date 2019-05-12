#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Requires python3 package for influxDB to import InfluxDBClient:
sudo apt install python3-influxdb

API documentation for python InfluxDBClient:
https://influxdb-python.readthedocs.io/en/latest/api-documentation.html#

users = db_client.get_list_users()
print (users)

API documentation for influxdb
https://docs.influxdata.com/influxdb/v1.4/introduction/

conntect to command line interface of influxdb:
influx
> show users
> show databases
> use <DATABASE>
> show series
'''

import time
import json
import sys
import argparse
from influxdb import InfluxDBClient

def main():
	parser = argparse.ArgumentParser(
		description='''This application reads json from std in,
		and pushes received data to an InfluxDB''',
	)
	parser.add_argument(
		'--db_name',
		type=str,
		default='',
		help='the name of the InfluxDB data is written to',
	)
	parser.add_argument(
		'--db_host',
		type=str,
		default='localhost',
		help='the host providing the influxdb',
	)
	parser.add_argument(
		'--db_port',
		type=int,
		default=8086,
		help='the port of the influxdb',
	)
	parser.add_argument(
		'--db_user',
		type=str,
		default='',
		help='the user allowed to write to the InfluxDB',
	)
	parser.add_argument(
		'--db_password',
		type=str,
		default='',
		help='the passwort for the specified user to access the InfluxDB',
	)
	parser.add_argument(
		'--testing',
		action='store_true',
		default=False,
		help='enabling testing mode without writing to InfluxDB',
	)
	args = parser.parse_args()
#
# Try to establish a DB connection
#
	if args.testing == True:
		print('testing mode, no DB used ...', file=sys.stderr)
	else:
		print('connection to InfluxDB ...', file=sys.stderr)
		try:
			print('db_host: ' + args.db_host, file=sys.stderr)
			print('db_name: ' + args.db_name, file=sys.stderr)
			db_client = InfluxDBClient(
			args.db_host,
			args.db_port,
			args.db_user,
			args.db_password,
			args.db_name
		)
		except Exception as e:
			print(e, file=sys.stderr)
			raise OSError('connection to InfluxDB cannot be established!')

		print('... connection established', file=sys.stderr)
		print('... waiting for incomming data', file=sys.stderr)

#
# read from stdin and write to InfluxDB
#

# json_body = [
#         {
#             "measurement": "cpu_load_short",
#             "tags": {
#                 "host": "server01",
#                 "region": "us-west"
#             },
#             "time": "2009-11-10T23:00:00Z",
#             "fields": {
#                 "Float_value": 0.64,
#                 "Int_value": 3,
#                 "String_value": "Text",
#                 "Bool_value": True
#             }
#         }
#     ]

# {
# 	"location": "wohnzimmer",
# 	"sensor": "dht11@0",
# 	"host": "the-crowsnest",

# 	"time": "2018-02-18T17:21:46.617120",

# 	"temperature": "18000",
# 	"pressure": null,
# 	"humidity_relative": "45000"
# }

	while True:
		try:
			for line in sys.stdin:
				# json.loads is for loading from strings
				# json.load is for loading form other resources
				data = json.loads(line)
				mymeasurement	= "roomclimate"
				myhost			= data['host']
				mysensor		= data['sensor']
				mylocation		= data['location']
				mytime			= data['time']

				# sensor readings are pushed to database as they are
				# further processing needs to be done by display / grafana

				if data['temperature'] != None:
					mytemperature = int(data['temperature'])
				else:
					# catch edge case, if sensor has no temperature
					mytemperature = 0

				if data['humidity_relative'] != None:
				# BME280 Sensor has humidity_relative data as float
# 2019-02-06: nach update hat der BME280 die Luftfeuchtigkeit im passenden Format, *1000 nun nicht mehr erforderlich
#					if mysensor == 'bme280':
#						myhumidity = int(float(data['humidity_relative'])*1000)
#					else:
					myhumidity = int(data['humidity_relative'])
				else:
					# catch edge case, if sensor has no humidity_relative
					myhumidity = 0

				if data['pressure'] != None:
					# BME280 Sensor has pressure data as float
					if mysensor == 'bme280':
						mypressure = int(float(data['pressure'])*1000)
					else:
						mypressure = int(data['pressure'])
				else:
					# catch edge case, if sensor has no pressure
					mypressure = 0

				json_body = [
					{
						"measurement": mymeasurement,
						"tags": {
							"host": myhost,
							"sensor": mysensor,
							"location": mylocation,
						},
						"time": mytime,
						"fields": {
							"temperature": mytemperature,
							"humidity_relative": myhumidity,
							"pressure": mypressure,
						},
					}
				]

				if args.testing == True:
					print("measurement:"+ mymeasurement, file=sys.stderr)
					print("host:"		+ myhost, file=sys.stderr)
					print("sensor:"		+ mysensor, file=sys.stderr)
					print("location:"	+ mylocation, file=sys.stderr)
					print("time:"		+ mytime, file=sys.stderr)
					print("temperature:"+ str(mytemperature), file=sys.stderr)
					print("humidity_relative:"+ str(myhumidity), file=sys.stderr)
					print("pressure:"	+ str(mypressure), file=sys.stderr)
					print("\n", file=sys.stderr)
					#print(json_body, file=sys.stderr)
				else:
					db_client.write_points(json_body)

		except Exception as e:
			print(e, file=sys.stderr)
			continue

#
# main function
#
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Shutting down iiopoll2influx.py', file=sys.stderr)
    except Exception as e:
        print(e)
