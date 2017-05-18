import serial
from threading import Thread
import socket
import sys

"""ARGUMENTOS DE ENTRADA NA COMMAND LINE"""
ip_server = str(sys.argv[1])
command_port = int(sys.argv[2])

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

        while True:
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

            """PARA X"""
            # valor central de X
            if X >= valor_central_min_X and X <= valor_central_max_X:
                X_msg = 0

            # intervalo positivo de X
            if X > valor_central_max_X:
                X_msg = int(round(((X - valor_central_max_X) / max_variacao_posit_X) * 100))

            # intervalo negativo de X
            if X < valor_central_min_X:
                X_msg = int(round(((X - valor_central_min_X) / max_variacao_neg_X) * 100))

            """PARA Y """
            # valor central de Y
            if Y >= valor_central_min_Y and Y <= valor_central_max_Y:
                Y_msg = 0

            # intervalo positivo de Y
            if Y > valor_central_max_Y:
                Y_msg = int(round(((Y - valor_central_max_Y) / max_variacao_posit_Y) * 100))

            # intervalo negativo de Y
            if Y < valor_central_min_Y:
                Y_msg = int(round(((Y - valor_central_min_Y) / max_variacao_neg_Y) * 100))

            command = "X:" + str(X_msg) + ",Y:" + str(Y_msg)
            print command
            # print data


            """ENVIO DE MENSAGEM COMANDO VIA SOCKET UDP"""
            conn.sendto(command, (ip_server, command_port))

joystick = client_joystick()
joystick.update_ip_port()
joystick.run()