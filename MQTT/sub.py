#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep  8 17:49:00 2024

@author: widhi
"""

import paho.mqtt.client as mqtt
import sys

# Gunakan broker lokal dalam docker compose
broker = "mqtt-broker"  # Service name
port = 1883  # Port default untuk MQTT
topic = "sister/temp"

# Callback ketika koneksi berhasil
def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print(f"Berhasil terhubung ke broker MQTT {broker}")
        # Berlangganan topik setelah koneksi berhasil
        client.subscribe(topic)
        print(f"Berlangganan topik: {topic}")
    else:
        print(f"Gagal terhubung ke broker, kode error: {rc}")
        sys.exit(1)

# Callback untuk pesan yang diterima
def on_message(client, userdata, message, properties=None):
    payload = message.payload.decode()
    try:
        import json
        data = json.loads(payload)
        suhu = data.get('suhu')
        lokasi = data.get('lokasi')
        print(f"Diterima: Suhu = {suhu}°C, Lokasi = {lokasi} (Topic: {message.topic})")
    except Exception:
        print(f"Received message: {payload} (Topic: {message.topic})")

# Inisialisasi klien MQTT dengan API versi terbaru
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message

# Menghubungkan ke broker dengan error handling
try:
    print(f"Menghubungkan ke {broker}...")
    client.connect(broker, port, keepalive=60)
except Exception as e:
    print(f"Gagal menghubungkan ke broker: {e}")
    sys.exit(1)

# Menjaga koneksi tetap terbuka
try:
    print("Menunggu pesan... (Tekan Ctrl+C untuk keluar)")
    client.loop_forever()
except KeyboardInterrupt:
    print("\nSubscriber dihentikan.")
    client.disconnect()