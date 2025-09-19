#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep  8 16:52:27 2024

@author: widhi
"""
import argparse
import os
import json
import time
from datetime import datetime
from zeep import Client


def main():
	parser = argparse.ArgumentParser(description='SOAP client CLI for calculator service')
	parser.add_argument('--wsdl', default=os.environ.get('SOAP_WSDL', 'http://soap-server:8000/?wsdl'), help='WSDL URL or env SOAP_WSDL')
	parser.add_argument('--op', choices=['add', 'sub', 'mul', 'div','mod','pow','avg'], default=None, help='Operation (if omitted, client will print combined add+sub sentence)')
	parser.add_argument('--all', action='store_true', help='Run all supported operations')
	parser.add_argument('-a', type=int, default=10)
	parser.add_argument('-b', type=int, default=5)
	parser.add_argument('--repeat', type=int, default=1, help='Repeat each operation N times and report average latency')
	parser.add_argument('--combined', action='store_true', help='Print combined sentence for add and sub in Indonesian')
	parser.add_argument('--json-output', action='store_true', help='Print output as JSON')
	parser.add_argument('--verbose', action='store_true', help='Print verbose output (timestamp, wsdl, latency)')
	args = parser.parse_args()

	client = Client(wsdl=args.wsdl)
	# If user didn't provide --op, --all, or --combined, default to combined sentence
	if args.op is None and not args.all and not args.combined:
		args.combined = True
	try:
		ops = ['add', 'sub', 'mul', 'div', 'mod', 'pow', 'avg']

		def call_one(op_name):
			# call op_name once and return (result, latency_ms)
			start = time.perf_counter()
			if op_name == 'add':
				r = client.service.add(args.a, args.b)
			elif op_name == 'sub':
				r = client.service.sub(args.a, args.b)
			elif op_name == 'mul':
				r = client.service.mul(args.a, args.b)
			elif op_name == 'div':
				r = client.service.div(args.a, args.b)
			elif op_name == 'mod':
				r = client.service.mod(args.a, args.b)
			elif op_name == 'pow':
				r = client.service.pow(args.a, args.b)
			elif op_name == 'avg':
				r = client.service.avg(args.a, args.b)
			else:
				raise ValueError('Unknown op')
			end = time.perf_counter()
			return r, (end - start) * 1000.0

		results = []

		if args.combined:
			# Call add and sub and print combined Indonesian sentence
			# perform repeats and take the last result for display (and avg latency)
			def call_n(op_name):
				total_latency = 0.0
				res_val = None
				for i in range(max(1, args.repeat)):
					r, lat = call_one(op_name)
					total_latency += lat
					res_val = r
				avg_latency = total_latency / max(1, args.repeat)
				return res_val, avg_latency

			add_res, add_lat = call_n('add')
			sub_res, sub_lat = call_n('sub')

			if args.json_output:
				out = {
					'timestamp': datetime.utcnow().isoformat() + 'Z',
					'wsdl': args.wsdl,
					'add': add_res,
					'sub': sub_res,
					'add_latency_ms': add_lat,
					'sub_latency_ms': sub_lat,
					'combined': f"hasil penjumlahan dengan SOAP = {add_res} dan hasil pengurangan dengan SOAP = {sub_res}"
				}
				print(json.dumps(out, indent=2))
			else:
				print(f"hasil penjumlahan dengan SOAP = {add_res} dan hasil pengurangan dengan SOAP = {sub_res}")
			return

		if args.all:
			for op_name in ops:
				total_latency = 0.0
				total_res = 0.0
				res_val = None
				for i in range(max(1, args.repeat)):
					r, lat = call_one(op_name)
					total_latency += lat
					try:
						total_res += float(r)
					except Exception:
						total_res += 0.0
					res_val = r
				avg_latency = total_latency / max(1, args.repeat)
				avg_result = total_res / max(1, args.repeat)
				results.append({'op': op_name, 'a': args.a, 'b': args.b, 'result': res_val, 'avg_result': avg_result, 'latency_ms': avg_latency})
		else:
			total_latency = 0.0
			total_res = 0.0
			res_val = None
			for i in range(max(1, args.repeat)):
				r, lat = call_one(args.op)
				total_latency += lat
				try:
					total_res += float(r)
				except Exception:
					total_res += 0.0
				res_val = r
			avg_latency = total_latency / max(1, args.repeat)
			avg_result = total_res / max(1, args.repeat)
			results.append({'op': args.op, 'a': args.a, 'b': args.b, 'result': res_val, 'avg_result': avg_result, 'latency_ms': avg_latency})

		# Output
		if args.json_output:
			out = {
				'timestamp': datetime.utcnow().isoformat() + 'Z',
				'wsdl': args.wsdl,
				'repeat': args.repeat,
				'results': results,
			}
			print(json.dumps(out, indent=2))
		else:
			if args.verbose:
				print(f"WSDL: {args.wsdl}")
				print(f"Timestamp: {datetime.utcnow().isoformat()}Z")
			for r in results:
				if args.verbose:
					print(f"{r['op']}({r['a']},{r['b']}) = {r['result']}  (avg_result={r['avg_result']}, latency={r['latency_ms']:.2f} ms)")
				else:
					print(f"{r['op']}({r['a']},{r['b']}) = {r['result']}")
	except Exception as e:
		print('SOAP call failed:', e)


if __name__ == '__main__':
	main()

