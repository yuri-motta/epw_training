import socket
import time
import sys


"""ARGUMENTOS DE ENTRADA NA COMMAND LINE"""
ip_server = str(sys.argv[1]) #ARGUMENTO 1 = IP SERVIDOR
command_port = int(sys.argv[2]) #ARGUMENTO 2 = PORTA

# ip_server = str(self.ip_server.get())
# command_port = int(self.command_port.get())
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
dest = (ip_server, command_port)
tcp.connect(dest)

for i in range(-100, 101):
        try:
            mensagem_enviada = "X=" +""+ str(i) + "%" + ",Y=" + "" +str(i) + "%" + str('\n')
            #mensagem_enviada = "Y;" + "-" + str(i) + "%"  + str('\n')
            tcp.send(mensagem_enviada)
            print('enviado: ' + mensagem_enviada)
            time.sleep(0.05)

        except socket.error:
            tcp.close()
tcp.close()