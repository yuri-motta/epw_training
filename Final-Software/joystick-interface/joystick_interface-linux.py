from Tkinter import *
import socket
import subprocess
import time
import threading
from threading import Thread
import datetime
import serial
from PIL import ImageTk

""" NOVA VERSAO DA GUI CLIENT"""
""" VERSAO COM VIDEO STREAMING AUTOMATICO"""


""" CONSTANT VARIABLES"""
#ip_command_server = "192.168.1.119"
ip_command_server = "200.129.152.97"
port_command_server = 4444
port_ip_cam = 4445
port_webcam = 4444

"""INITIAL VALUES"""
updated = False
stop_flag = False


class Application(Frame):

    def __init__(self,master):
        """Initialize the Frame"""
        Frame.__init__(self,master)
        self.grid()
        self.create_widgets()

    def create_widgets(self):

        # instructions
        self.instructions = Label(self, text="Wheelchair Training \n Environment \n Joystick control interface", font="bold")
        self.instructions.grid(row=0, column=1, sticky=W)

        # ip entry
        #Label(self, text="Command Server IP: " + ip_command_server).grid(row=6, column=1, sticky=W)

        # port entry
        #Label(self, text="Command Port: " + str(port_command_server)).grid(row=7, column=1, sticky=W)

        # Start training
        self.button_save = Button(self, text="Start wheelchair training", command=self.update_ip_port, bg='#6C8EBF')
        self.button_save.grid(row=5,column=1, sticky=W)

        # Stop training
        self.button_stop = Button(self, text="Stop training", command=self.stop_training, bg='#DF0101')
        self.button_stop.grid(row=6, column=1, sticky=W)


    # start training
    def update_ip_port(self):
        global ip_server, command_port, conn, updated, local_ip, video_port
        ip_server = ip_command_server
        command_port = port_command_server
        conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        Label(self, text="Training started!").grid(row=7, column=1, sticky=W)
        updated = True

        ## thread rtt
        rtt_measure_send = RTT_sender()
        self.t1 = threading.Thread(target=rtt_measure_send.run)
        self.t1.setDaemon(True)
        self.t1.start()

        ## thread video streamin
        video_stream = client_video_stream()
        self.t2 = threading.Thread(target=video_stream.run)
        self.t2.setDaemon(True)
        self.t2.start()

        ## thread joystick
        joystick = joystick_sender()
        self.t3 = threading.Thread(target=joystick.run)
        self.t3.setDaemon(True)
        self.t3.start()

    def stop_training(self):
        global stop_flag

        command = "stop"
        conn.sendto(command, (ip_server, command_port))
        conn.sendto(command, (ip_server, command_port))
        conn.sendto(command, (ip_server, command_port))
        stop_flag = True
        print "Stop training"
        Label(self, text="       Training finished        " + "\n" +"      Thank you!       ").grid(row=7, column=1, sticky=W)


class client_video_stream(Thread):

    def __init__(self):
        Thread.__init__(self)
        #local_ip = str(local_ip.get())
        #video_port = str(video_port.get())
        # os.system('ffplay -fflags nobuffer -flags low_delay -framedrop -strict experimental udp://'+ local_ip +':' + video_port)
        # linux_command = 'ffplay -fflags nobuffer -flags low_delay -framedrop -strict experimental udp://'+ local_ip +':' + video_port
        #self.url = 'tcp://' + local_ip + ":" + video_port + "?listen"

        self.url_webcam = 'http://' + ip_command_server + ':' + str(port_webcam)
        self.url_ip_cam = 'http://'+ ip_command_server + ':' + str(port_ip_cam) + '/img/video.mjpeg'

    def run(self):
        subprocess.Popen(["ffplay", "-fflags", "nobuffer", "-flags", "low_delay","%s" % self.url_webcam])
        subprocess.Popen(["ffplay", "-fflags", "nobuffer", "-flags", "low_delay", "%s" % self.url_ip_cam])

class RTT_sender(Thread):

    def __init__(self):
        Thread.__init__(self)

    def run(self):
        global ip_command_server, port_command_server,stop_flag

        while stop_flag==False:

            try:
                ping_process = subprocess.Popen(['ping', '-c', '1', ip_server], stdout=subprocess.PIPE)
                stdout = ping_process.stdout.read()
                match = re.search(r'\d*\.\d*\/(\d*\.\d*)\/\d*\.\d*\/\d*\.\d*', stdout)
                avg = match.group(1)

                rtt = '{}'.format(avg)

                ts = time.time()
                ano = datetime.datetime.fromtimestamp(ts).strftime('%Y')
                mes = datetime.datetime.fromtimestamp(ts).strftime('%m')
                dia = datetime.datetime.fromtimestamp(ts).strftime('%d')
                hora = datetime.datetime.fromtimestamp(ts).strftime('%H')
                minutos = datetime.datetime.fromtimestamp(ts).strftime('%M')
                segundos = datetime.datetime.fromtimestamp(ts).strftime('%S')

                print(rtt)

                self.message = "RTT: " + rtt + " " + " TS: " + str(ts) + " " + str(ano) + " " + str(mes) + " " + str(dia) + " " + str(hora)+ " "  + str(minutos)+ " "  + str(segundos)
                conn.sendto(self.message, (ip_command_server, port_command_server))
                time.sleep(1)

            except AttributeError:
                print "failed to ping"

class joystick_sender(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        global conn, updated, ip_command_server, port_command_server

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
        ser = serial.Serial('/dev/ttyACM0', 9600)

        try:
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

                """ CONDICAO PARA X,Y FICAREM ENTRE -100 E 100"""
                if X_msg >100:
                    X_msg =100

                if X_msg <-100:
                    X_msg = -100

                if Y_msg > 100:
                    Y_msg = 100

                if Y_msg < -100:
                    Y_msg = -100

                self.command = "X=" + str(X_msg) + "%" + ",Y=" + str(Y_msg) + "%"
                print self.command
                # print data

                """ SALVA O TIMESTAMP EM QUE O COMANDO FOI EXECUTADO"""
                ts = time.time()
                ano = datetime.datetime.fromtimestamp(ts).strftime('%Y')
                mes = datetime.datetime.fromtimestamp(ts).strftime('%m')
                dia = datetime.datetime.fromtimestamp(ts).strftime('%d')
                hora = datetime.datetime.fromtimestamp(ts).strftime('%H')
                minutos = datetime.datetime.fromtimestamp(ts).strftime('%M')
                segundos = datetime.datetime.fromtimestamp(ts).strftime('%S')


                """ENVIO DE MENSAGEM COMANDO VIA SOCKET UDP"""
                conn.sendto(self.command, (ip_command_server, port_command_server))
        except KeyboardInterrupt:
            pass



root = Tk()
root.title("Joystick Interface")
root.geometry("300x200")
app = Application(root)

root.mainloop()