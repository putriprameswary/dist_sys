#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep  8 14:16:13 2024

@author: widhi
"""

import socket
import argparse


def client_program(host, port, double_message=None):
    client_socket = socket.socket()
    # Use docker compose service DNS instead of a hardcoded external IP
    client_socket.connect((host, port))

    if double_message:
        # send two messages in one payload separated by '||'
        payload = double_message
        client_socket.send(payload.encode())
        data = client_socket.recv(1024).decode()
        print('Received upcall from server:', data)
        client_socket.close()
        return

    print("Type a message and press Enter to send. Press Enter with empty input to resend the previous message. Type 'bye' to quit.")
    last_message = None
    message = input("Enter message: ")

    while message.lower().strip() != 'bye':
        # If user pressed Enter without typing anything, resend last message
        if message.strip() == '':
            if last_message is None:
                # nothing to resend; prompt again
                print('(no previous message to resend)')
                message = input("Enter message: ")
                continue
            message_to_send = last_message
            print(f"Resending previous message: '{message_to_send}'")
        else:
            message_to_send = message

        # If we have a previous message and the user typed a new one,
        # send them together as a single payload so the server can insert 'love' between them.
        if last_message is not None and message_to_send.strip() != last_message.strip():
            combined = f"{last_message}||{message_to_send}"
            print(f"Sending combined payload: '{combined}'")
            client_socket.send(combined.encode())
        else:
            # normal single-message send (including resends)
            client_socket.send(message_to_send.encode())

        data = client_socket.recv(1024).decode()

        print('Received upcall from server:', data)  # Simulating upcall response

        last_message = message_to_send
        message = input("Enter another message (or press Enter to resend): ")

    client_socket.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Upcall client')
    parser.add_argument('--host', default='upcall-server', help='Server host')
    parser.add_argument('--port', type=int, default=4141, help='Server port')
    parser.add_argument('--double', help='Send two messages separated by "||" as a single payload')
    args = parser.parse_args()
    client_program(args.host, args.port, args.double)
