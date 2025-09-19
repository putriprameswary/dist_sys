#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep  8 14:15:04 2024

@author: widhi
"""

import socket
import os
import sys


def server_program():
    server_socket = socket.socket()
    # Bind to all interfaces so client container can reach it
    base_port = int(os.environ.get('PORT', '4141'))
    bound_port = None
    # try a few ports if the preferred one is already in use
    for attempt in range(base_port, base_port + 5):
        try:
            server_socket.bind(('0.0.0.0', attempt))
            bound_port = attempt
            break
        except OSError as e:
            print(f"Port {attempt} not available: {e}")
            continue

    if bound_port is None:
        print(f"Could not bind to any port in range {base_port}-{base_port+4}. Exiting.")
        sys.exit(1)

    server_socket.listen(1)
    print(f"Upcall server listening on 0.0.0.0:{bound_port} (DNS: upcall-server:{bound_port})")
    conn, address = server_socket.accept()  
    print("Connection from:", address)
    
    # Keep track of the previous message for this connection so that
    # two sequential sends (first message then second message) can be
    # combined into a single 'love' response: '<first> love <second>'.
    prev_msg = None
    while True:
        data = conn.recv(1024).decode()
        if not data:
            break
        data = data.strip()
        print("Received from client:", data)

        # If client sent two messages in one payload separated by '||',
        # insert the word 'love' between them and send that back.
        if '||' in data:
            parts = data.split('||', 1)
            left = parts[0].strip()
            right = parts[1].strip()
            upcall_message = f"{left} love {right}"
            # reset prev_msg after handling a combined payload
            prev_msg = None
        else:
            if prev_msg is None:
                # store the first message and acknowledge receipt
                prev_msg = data
                upcall_message = f"Received: {data}"
            else:
                # we have a previous message; combine with current
                upcall_message = f"{prev_msg} love {data}"
                # reset prev_msg after combining
                prev_msg = None

        conn.send(upcall_message.encode())
    
    conn.close()

if __name__ == '__main__':
    server_program()
