import socket
import time

HOST = '192.168.1.114'  # Endereco IP do Servidor
PORT = 4444  # Porta que o Servidor esta

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
dest = (HOST, PORT)

tcp.connect(dest)


for i in range(0, 101):
    try:

        mensagem_enviada = "X;" +""+ str(i) + "%" + ";Y;" + "" +str(i) + "%" + str('\n')
        #mensagem_enviada = "Y;" + "-" + str(i) + "%"  + str('\n')
        tcp.send(mensagem_enviada)

        print('enviado: ' + mensagem_enviada)
        time.sleep(0.5)

    except socket.error:
        tcp.close()

tcp.close()