#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep  8 17:02:45 2024

@author: widhi
"""

import os
from flask import Flask, request, jsonify

# Inisialisasi aplikasi Flask
app = Flask(__name__)


@app.route('/add', methods=['GET'])
def add_numbers():
    try:
        a = int(request.args.get('a'))
        b = int(request.args.get('b'))
        return jsonify({'result': a + b})
    except (TypeError, ValueError):
        return jsonify({'error': 'Invalid input'}), 400


@app.route('/sub', methods=['GET'])
def sub_numbers():
    try:
        a = int(request.args.get('a'))
        b = int(request.args.get('b'))
        return jsonify({'result': a - b})
    except (TypeError, ValueError):
        return jsonify({'error': 'Invalid input'}), 400


@app.route('/mul', methods=['GET'])
def mul_numbers():
    try:
        a = int(request.args.get('a'))
        b = int(request.args.get('b'))
        return jsonify({'result': a * b})
    except (TypeError, ValueError):
        return jsonify({'error': 'Invalid input'}), 400


@app.route('/div', methods=['GET'])
def div_numbers():
    try:
        a = int(request.args.get('a'))
        b = int(request.args.get('b'))
        if b == 0:
            return jsonify({'error': 'Division by zero'}), 400
        return jsonify({'result': a / b})
    except (TypeError, ValueError):
        return jsonify({'error': 'Invalid input'}), 400


@app.route('/calc', methods=['POST'])
def calc():
    """Generic calculator endpoint. Accepts JSON body: {"op": "add|sub|mul|div", "a": <num>, "b": <num>}"""
    data = request.get_json(silent=True)
    if not data:
        return jsonify({'error': 'JSON body required'}), 400

    op = data.get('op')
    a = data.get('a')
    b = data.get('b')
    try:
        a = float(a)
        b = float(b)
    except (TypeError, ValueError):
        return jsonify({'error': 'Invalid input'}), 400

    if op == 'add':
        res = a + b
    elif op == 'sub':
        res = a - b
    elif op == 'mul':
        res = a * b
    elif op == 'div':
        if b == 0:
            return jsonify({'error': 'Division by zero'}), 400
        res = a / b
    elif op == 'mod':
        # modulo operation
        if b == 0:
            return jsonify({'error': 'Division by zero'}), 400
        res = a % b
    elif op == 'pow':
        # exponentiation
        res = a ** b
    else:
        return jsonify({'error': 'Unknown operation'}), 400

    return jsonify({'result': res})


if __name__ == '__main__':
    # Read PORT from environment to allow container/host mapping flexibility
    port = int(os.environ.get('PORT', '5151'))
    print(f"Starting REST server on 0.0.0.0:{port} (debug=True)")
    # Bind to 0.0.0.0 so container port mapping works externally
    app.run(debug=True, host='0.0.0.0', port=port)
