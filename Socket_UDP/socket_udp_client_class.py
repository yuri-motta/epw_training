import socket
from threading import Thread

UDP_IP = "127.0.0.1"
UDP_PORT = 4444

class socket_client_udp(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send_message(self, message):
        self.sock.sendto(message, (UDP_IP, UDP_PORT))

conn = socket_client_udp()
conn.send_message("iasda")

