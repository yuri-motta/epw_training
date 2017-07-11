import serial
from threading import Thread
import socket
import sys

"""ARGUMENTOS DE ENTRADA NA COMMAND LINE"""

# exemplo: python joystick_training_client.py 192.168.1.144 4444

class client_joystick(Thread):

    def __init__(self):
        Thread.__init__(self)
        #local_ip = str(local_ip.get())
        #video_port = str(video_port.get())
        # os.system('ffplay -fflags nobuffer -flags low_delay -framedrop -strict experimental udp://'+ local_ip +':' + video_port)
        # linux_command = 'ffplay -fflags nobuffer -flags low_delay -framedrop -strict experimental udp://'+ local_ip +':' + video_port

    def update_ip_port(self):
        global ip_server, command_port, conn, updated
        #ip_server = str(self.ip_server.get())
        #command_port = int(self.command_port.get())
        conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def run(self):
        global conn, updated, ip_server, command_port
        """INICIA OS VALORES DE X E Y"""
        X = "0"
        Y = "0"

        """CONSTANTES"""
        # PARA X
        valor_central_max_X = 495
        valor_central_min_X = 480
        valor_max_X = 710
        valor_min_X = 290
        max_variacao_posit_X = valor_max_X - valor_central_max_X
        max_variacao_neg_X = valor_central_min_X - valor_min_X

        # PARA Y
        valor_central_max_Y = 535
        valor_central_min_Y = 510
        valor_max_Y = 730
        valor_min_Y = 295
        max_variacao_posit_Y = valor_max_Y - valor_central_max_Y
        max_variacao_neg_Y = valor_central_min_Y - valor_min_Y

        # PORTA SERIAL UTILIZADA
        ser = serial.Serial('/dev/ttyUSB0', 9600)
        f = open("valores_tensao_joystick_v3.dat", "w")
        for i in range(1,1000,1):
            data = ser.readline(5)
            vetor_mensagem = data.split(":", 1)
            if vetor_mensagem[0] == "X":
                X = vetor_mensagem[1]
            if vetor_mensagem[0] == "Y":
                Y = vetor_mensagem[1]

            # mensagem_final = "X:" + X + ",Y:" + Y
            # print mensagem_final
            # print data

            """CONVERSAO DE 10 BITS PARA PROTOCOLO DE MENSAGEM"""
            X = float(X)
            Y = float(Y)

            tensao_X = round(((X / 1023)*5),2) #arredonda com duas casas decimais
            tensao_Y = round(((Y / 1023)*5),2)

            print str(tensao_X) + " " + str(tensao_Y) + "\n"

            f.write(str(tensao_X) + " " + str(tensao_Y) + "\n")
        f.close()



joystick = client_joystick()
joystick.update_ip_port()
joystick.run()