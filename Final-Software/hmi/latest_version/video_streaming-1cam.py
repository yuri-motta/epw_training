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
#ip_command_server = "localhost"
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
        #self.t1.start()

        ## thread video streamin
        video_stream = client_video_stream()
        self.t2 = threading.Thread(target=video_stream.run)
        self.t2.setDaemon(True)
        self.t2.start()

        ## thread joystick
        eye_trk = eye_tracker()
        self.t3 = threading.Thread(target=eye_trk.run)
        self.t3.setDaemon(True)
        #self.t3.start()


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
        print "lol"
        subprocess.Popen(["ffplay", "-fflags", "nobuffer", "-flags", "low_delay","%s" % self.url_webcam])
        #subprocess.Popen(["ffplay", "-fflags", "nobuffer", "-flags", "low_delay", "%s" % self.url_ip_cam])

class RTT_sender(Thread):

    def __init__(self):
        Thread.__init__(self)

    def run(self):
        global ip_command_server, port_command_server,stop_flag

        while stop_flag==False:

            try:
                ping_process = subprocess.Popen(['psping', '-n', '1', ip_command_server], stdout=subprocess.PIPE)
                stdout = ping_process.stdout.read()
                match = re.findall(r'\d*\.\d*', stdout)

                rtt = match[19]

                ts = time.time()
                ano = datetime.datetime.fromtimestamp(ts).strftime('%Y')
                mes = datetime.datetime.fromtimestamp(ts).strftime('%m')
                dia = datetime.datetime.fromtimestamp(ts).strftime('%d')
                hora = datetime.datetime.fromtimestamp(ts).strftime('%H')
                minutos = datetime.datetime.fromtimestamp(ts).strftime('%M')
                segundos = datetime.datetime.fromtimestamp(ts).strftime('%S')

                print "RTT: "
                print(rtt)

                self.message = "RTT: " + rtt + " " + " TS: " + str(ts) + " " + str(ano) + " " + str(mes) + " " + str(dia) + " " + str(hora) + " " + str(minutos) + " " + str(segundos)
                conn.sendto(self.message, (ip_command_server, port_command_server))
                time.sleep(1)

            except:
                print "failed to ping"

class eye_tracker(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):

        self.process_name = "app_eyetracker/eye_tracker_interface-v2.exe"
        subprocess.call([self.process_name])




root = Tk()
root.title("Joystick Interface")
root.geometry("300x200")
app = Application(root)

root.mainloop()