import socket
import sys
from threading import Thread

HOST = "127.0.0.1"  # Symbolic name meaning all available interfaces
PORT = 4444  # Arbitrary non-privileged port

class Udp_server(Thread):
    def __init__(self):
        global socket_server
        """Create socket server and bind to ip and port"""
        Thread.__init__(self)
        try:
            socket_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            print 'Socket created'
        except socket.error, msg:
            print 'Failed to create socket. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
            sys.exit()

        # Bind socket to local host and port
        try:
            socket_server.bind((HOST, PORT))
        except socket.error, msg:
            print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
            sys.exit()

        print 'Socket bind complete'

    def run(self):
        """receive and send messages"""

        global socket_server

        # now keep talking with the client
        while 1:
            # receive data from client (data, addr)
            d = socket_server.recvfrom(1024)
            data = d[0]
            addr = d[1]

            if not data:
                break

            reply = 'OK...' + data

            socket_server.sendto(reply, addr)
            print 'Message[' + addr[0] + ':' + str(addr[1]) + '] - ' + data.strip()

server = Udp_server()
server.run()