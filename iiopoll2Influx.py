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
	args = parser.parse_args()
#
# Try to establish a DB connection
#
	try:
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

	print('connection to InfluxDB is established', file=sys.stderr)
	print('...waiting for incomming data', file=sys.stderr)

#
# read from stdin and write to InfluxDB
#
	while True:
		try:
			for line in sys.stdin:
				db_client.write_points(line)

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
