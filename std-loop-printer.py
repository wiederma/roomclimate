#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import time
import argparse

def main():
    parser = argparse.ArgumentParser(
		description='''This application prints a counter every SLEEPTIME
        interval to std out. SLEEPTIME is by default 10 seconds.''',
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
            print(counter)
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
