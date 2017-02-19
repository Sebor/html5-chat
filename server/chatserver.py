#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Licence = GPLv3
try:
    import psyco  # Speed Up if avaliable
    psyco.full()
except ImportError:
    pass
# STD Libs
import socket
import threading
import struct
import hashlib
import sys
#
#
#
PORT = 9999 #ESTE ES EL NUMERO DE PUERTO TCP DE ESTE SERVIDOR (>1024, debe ser = en client.html)
#
#
#
print (" Starting Python HTML5 Chat Server on \n " + str(sys.platform) + " with " + str(sys.version))
print (" Using Local Port TCP/" + str(PORT))
def create_handshake_resp(handshake): # Saludo TCP 3 Way
    print (" TCP 3-Way HandShake on Port " + str(PORT) + " in progress...")
    final_line = ""
    lines = handshake.splitlines()
    for line in lines:
        parts = line.partition(": ")
        if parts[0] == "Sec-WebSocket-Key1": # security Key 1
            key1 = parts[2]
        elif parts[0] == "Sec-WebSocket-Key2": # security Key 2
            key2 = parts[2]
        elif parts[0] == "Host":
            host = parts[2]
        elif parts[0] == "Origin":
            origin = parts[2]
        final_line = line
    spaces1 = key1.count(" ")
    spaces2 = key2.count(" ")
    num1 = int("".join([c for c in key1 if c.isdigit()])) / spaces1
    num2 = int("".join([c for c in key2 if c.isdigit()])) / spaces2
    token = hashlib.md5(struct.pack('>II8s', num1, num2, final_line)).digest()
    return ("HTTP/1.1 101 WebSocket Protocol Handshake\r\n"
        "Upgrade: WebSocket\r\n" "Connection: Upgrade\r\n"
        "Sec-WebSocket-Origin: %s\r\n" "Sec-WebSocket-Location: ws://%s/\r\n"
        "\r\n" "%s") % (origin, host, token) # devuelve el Saludo
#
def handle(s, addr): # Maneja datos en trozos de 1024
    data = s.recv(1024)
    s.send(create_handshake_resp(data))
    lock = threading.Lock()
    while 1:
        print (" Waiting Data from " + str(addr) + "...")
        data = s.recv(1024)
        print (" OK!")
        if not data:
            print (" No Data")
            break
        print (" Incoming Chats from " + str(addr) + ' said ' + str(data))
        lock.acquire()
        [conn.send(data) for conn in clients]
        lock.release()
    print (' Client Disconnected:' + str(addr) + ", Bye.")
    lock.acquire()
    clients.remove(s)
    lock.release()
    s.close()
# Start Server
def start_server(): # Inicia el Servo
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('', PORT))
    s.listen(1)
    while 1:
        conn, addr = s.accept()
        print (" Connected from " + str(addr) + ", Hello!")
        clients.append(conn)
        threading.Thread(target = handle, args = (conn, addr)).start()
# Start Chat
if sys.hexversion > 0x02050000: # Python version check
    pass # python version >= 2.5.0, do nothing
else:
    print ("\n ERROR: Python version < 2.5.0\n") # python version under 2.5.0 dont work
    sys.exit(" ERROR: python version under 2.5.0 dont work...\n")
# Lets Rock!
clients = []
start_server()
#
