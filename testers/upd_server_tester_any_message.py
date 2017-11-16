import socket
import sys
from threading import Thread



"""DADOS DE CONEXAO"""
HOST = "192.168.1.117"  # Symbolic name meaning all available interfaces
PORT = 4444  # Arbitrary non-privileged port

class Udp_server(Thread):
    def __init__(self):
        global socket_server
        """Create socket server and bind to ip and port"""
        Thread.__init__(self)
        try:
            socket_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            print 'Socket test UDP created'
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

        try:
            while 1:
                # receive data from client (data, addr)
                d = socket_server.recvfrom(256)
                data = str(d[0])
                addr = d[1]

                if not data:
                    break

                print 'Message[' + addr[0] + ':' + str(addr[1]) + '] - ' + data.strip()

        except KeyboardInterrupt:
            pass

server = Udp_server()
server.run()
