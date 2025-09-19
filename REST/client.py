#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep  8 17:05:25 2024

@author: widhi
"""

import requests
import argparse
import sys
import os

BASE = os.environ.get('REST_BASE', 'http://rest-server:5151')

def call(endpoint, a, b):
    try:
        r = requests.get(f"{BASE}/{endpoint}", params={'a': a, 'b': b}, timeout=3)
        if r.status_code == 200:
            data = r.json()
            print(f"{endpoint}({a},{b}) = {data['result']}")
        else:
            print(f"{endpoint} error {r.status_code}: {r.text}")
    except Exception as e:
        print(f"{endpoint} exception: {e}")


def main():
    parser = argparse.ArgumentParser(description="Simple REST client for add/mul endpoints")
    parser.add_argument('--op', choices=['add','mul','both','sub','div'], default='both', help='Operation to invoke')
    parser.add_argument('-a', type=int, default=10)
    parser.add_argument('-b', type=int, default=5)
    args = parser.parse_args()
    if args.op in ('add','both'):
        call('add', args.a, args.b)
    if args.op in ('mul','both'):
        call('mul', args.a, args.b)
    if args.op in ('sub','both'):
        call('sub', args.a, args.b)
    if args.op in ('div','both'):
        call('div', args.a, args.b)


if __name__ == '__main__':
    sys.exit(main())
