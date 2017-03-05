import socket

UDP_IP = "127.0.0.1"
UDP_PORT = 4444

message = "HELLO WORLD!"

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(message, (UDP_IP,UDP_PORT))
