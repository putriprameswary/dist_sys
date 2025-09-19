#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep  8 16:49:40 2024

@author: widhi
"""

from spyne import Application, rpc, ServiceBase, Integer, Double
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication

# Membuat layanan SOAP dengan metode penjumlahan
class CalculatorService(ServiceBase):
    @rpc(Integer, Integer, _returns=Integer)
    def add(ctx, a, b):
        return a + b

    @rpc(Integer, Integer, _returns=Integer)
    def sub(ctx, a, b):
        return a - b

    @rpc(Integer, Integer, _returns=Integer)
    def mul(ctx, a, b):
        return a * b

    @rpc(Integer, Integer, _returns=Integer)
    def div(ctx, a, b):
        # simple integer division; return 0 on division by zero
        try:
            return a // b
        except ZeroDivisionError:
            return 0

    @rpc(Integer, Integer, _returns=Integer)
    def mod(ctx, a, b):
        try:
            return a % b
        except ZeroDivisionError:
            return 0

    @rpc(Integer, Integer, _returns=Double)
    def pow(ctx, a, b):
        # exponentiation; return float to avoid overflow issues
        return float(a) ** float(b)

    @rpc(Integer, Integer, _returns=Double)
    def avg(ctx, a, b):
        return (float(a) + float(b)) / 2.0

# Membuat aplikasi SOAP dengan protokol Soap11
app = Application([CalculatorService],
                  tns='spyne.examples.calculator',
                  in_protocol=Soap11(),
                  out_protocol=Soap11())

# Menjalankan server menggunakan WSGI
if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    wsgi_app = WsgiApplication(app)
    # Bind on all interfaces for container networking
    server = make_server('0.0.0.0', 8000, wsgi_app)
    print("SOAP server listening on http://0.0.0.0:8000 (service DNS: soap-server:8000)")
    server.serve_forever()
