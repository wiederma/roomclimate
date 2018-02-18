#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import time
import argparse

json_sample = [
    '''{"location": "wohnzimmer", "temperature": "21650", "sensor": "bme280", "time": "2018-02-18T17:20:15.048173", "host": "the-crowsnest", "pressure": "96.862171875", "humidity_relative": "57.175781250"}''',
    '''{"location": "wohnzimmer", "temperature": "18000", "sensor": "dht11@0", "time": "2018-02-18T17:20:15.088703", "host": "the-crowsnest", "pressure": null, "humidity_relative": "45000"}''',
    '''{"location": "wohnzimmer", "temperature": "21265", "sensor": "htu21", "time": "2018-02-18T17:20:45.650295", "host": "the-crowsnest", "pressure": null, "humidity_relative": "58570"}''',
    '''{"location": "wohnzimmer", "temperature": "21640", "sensor": "bme280", "time": "2018-02-18T17:20:45.728328", "host": "the-crowsnest", "pressure": "96.858878906", "humidity_relative": "57.198242187"}''',
    '''{"location": "wohnzimmer", "temperature": "18000", "sensor": "dht11@0", "time": "2018-02-18T17:20:45.767796", "host": "the-crowsnest", "pressure": null, "humidity_relative": "45000"}''',
    '''{"location": "wohnzimmer", "temperature": "21275", "sensor": "htu21", "time": "2018-02-18T17:21:16.328932", "host": "the-crowsnest", "pressure": null, "humidity_relative": "58540"}''',
    '''{"location": "wohnzimmer", "temperature": "21630", "sensor": "bme280", "time": "2018-02-18T17:21:16.406952", "host": "the-crowsnest", "pressure": "96.858738281", "humidity_relative": "57.174804687"}''',
    '''{"location": "wohnzimmer", "temperature": "18000", "sensor": "dht11@0", "time": "2018-02-18T17:21:16.448306", "host": "the-crowsnest", "pressure": null, "humidity_relative": "44000"}''',
    '''{"location": "wohnzimmer", "temperature": "21265", "sensor": "htu21", "time": "2018-02-18T17:21:46.505107", "host": "the-crowsnest", "pressure": null, "humidity_relative": "58600"}''',
    '''{"location": "wohnzimmer", "temperature": "21630", "sensor": "bme280", "time": "2018-02-18T17:21:46.581781", "host": "the-crowsnest", "pressure": "96.858433593", "humidity_relative": "57.231445312"}''',
    '''{"location": "wohnzimmer", "temperature": "18000", "sensor": "dht11@0", "time": "2018-02-18T17:21:46.617120", "host": "the-crowsnest", "pressure": null, "humidity_relative": "45000"}''',
]

def main():
    parser = argparse.ArgumentParser(
		description='''This application is for testing purposes only! It
        prints a counter every SLEEPTIME interval to std out. SLEEPTIME is by
        default 10 seconds.''',
	)
    parser.add_argument(
        '--sleeptime',
        default=10,
        type=int,
        help='provide sleeptime in seconds'
    )

    args = parser.parse_args()
    counter=0

    while True:
        try:
            print(json_sample[counter%11])
            sys.stdout.flush()
            counter+=1
        except Exception as e:
            print(e, file=sys.stderr)
            continue

        time.sleep(args.sleeptime)

#
# main function
#
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Shutting down', file=sys.stderr)
    except Exception as e:
        print(e)
