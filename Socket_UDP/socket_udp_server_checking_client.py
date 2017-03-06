import socket
import sys
from threading import Thread

HOST = "127.0.0.1"  # Symbolic name meaning all available interfaces
PORT = 4444  # Arbitrary non-privileged port
EPW_connected = False

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

    def check_epw_client(msg):
        """verify if the client is EPW"""
        if msg == "EPW connected":
            return True
        else:
            return False

    def run(self):
        """receive and send udp socket messages"""

        global socket_server, EPW_addr, EPW_connected

        # now keep talking with the client
        while 1:
            # receive data from client (data, addr)
            self.d = socket_server.recvfrom(1024)
            self.data = self.d[0]
            self.addr = self.d[1]

            if not self.data:
                break

            # saves epw address and notify when it is connected
            if self.data == "EPW connected":
                EPW_addr = self.addr
                EPW_connected = True
                print "EPW is now connected"

            # send received messages to EPW, when different from "EPW is connected"
            # ex: x;100%;y:0%
            if (EPW_connected == True) & (self.data != "EPW connected"):
                socket_server.sendto(self.data, EPW_addr)

            #prints the client address and received message
            print 'Message[' + self.addr[0] + ':' + str(self.addr[1]) + '] - ' + self.data.strip()

server = Udp_server()
server.run()