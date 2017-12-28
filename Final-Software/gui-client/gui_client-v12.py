from Tkinter import *
import socket
import subprocess
import time
import threading
from threading import Thread
import datetime
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
        self.instructions = Label(self, text="Wheelchair Training \n Environment", font="bold")
        self.instructions.grid(row=0, column=1, sticky=W)

        #gui icon
        self.gui_icon = Label(self)
        self.wheelchair_img = ImageTk.PhotoImage(file="icons/gui_icon.png")
        self.gui_icon.config(image=self.wheelchair_img)
        self.gui_icon.image = self.wheelchair_img
        self.gui_icon.pack
        self.gui_icon.grid(row=1,column=1, sticky=W)


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

        #instructions
        Label(self, text="Commands").grid(row=0, column=9, sticky=W)

        #UP button
        self.button_up = Button(self, text="UP", command=self.up_command)
        self.up_image = ImageTk.PhotoImage(file="icons/up_button.png")
        self.button_up.config(image=self.up_image)
        self.button_up.image =self.up_image
        self.button_up.pack
        self.button_up.grid(row=1, column =9)

        #DOWN button
        self.button_down = Button(self, text="DOWN", command=self.down_command)
        self.down_image = ImageTk.PhotoImage(file="icons/down_button.png")
        self.button_down.config(image=self.down_image)
        self.button_down.image = self.down_image
        self.button_down.pack
        self.button_down.grid(row=3, column=9)

        #LEFT button
        self.button_left = Button(self, text="LEFT", command=self.left_command)
        self.left_image = ImageTk.PhotoImage(file="icons/left_button.png")
        self.button_left.config(image=self.left_image)
        self.button_left.image = self.left_image
        self.button_left.pack
        self.button_left.grid(row=2, column=8)

        #RIGHT button
        self.button_right = Button(self, text="RIGHT", command=self.right_command)
        self.right_image = ImageTk.PhotoImage(file="icons/right_button.png")
        self.button_right.config(image=self.right_image)
        self.button_right.image = self.right_image
        self.button_right.pack
        self.button_right.grid(row=2,column=10)

        #STOP button
        self.button_stop = Button(self, text="STOP", command=self.stop_command)
        self.stop_image = ImageTk.PhotoImage(file="icons/stop_button.png")
        self.button_stop.config(image=self.stop_image)
        self.button_stop.image = self.stop_image
        self.button_stop.pack
        self.button_stop.grid(row=2, column=9)


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

        video_stream = client_video_stream()
        self.t2 = threading.Thread(target=video_stream.run)
        self.t2.setDaemon(True)
        self.t2.start()

    def stop_training(self):
        global stop_flag

        command = "stop"
        conn.sendto(command, (ip_server, command_port))

        stop_flag = True
        print "Stop training"
        Label(self, text="       Training finished        " + "\n" +"      Thank you!       ").grid(row=7, column=1, sticky=W)


    def up_command(self):
        command = "X=0%,Y=80%"
        if updated==True:
            conn.sendto(command, (ip_server, command_port))
            conn.sendto(command, (ip_server, command_port))
            conn.sendto(command, (ip_server, command_port))
            conn.sendto(command, (ip_server, command_port))
            conn.sendto(command, (ip_server, command_port))

        else:
            Label(self, text="First press Start", fg='red').grid(row=6, column=1, sticky=W)

    def down_command(self):
        command = "X=0%,Y=-80%"
        if updated == True:
            conn.sendto(command, (ip_server, command_port))
            conn.sendto(command, (ip_server, command_port))
            conn.sendto(command, (ip_server, command_port))
            conn.sendto(command, (ip_server, command_port))
            conn.sendto(command, (ip_server, command_port))

        else:
            Label(self, text="First press Start", fg='red').grid(row=6, column=1, sticky=W)

    def left_command(self):
        command = "X=80%,Y=0%"
        if updated == True:
            conn.sendto(command, (ip_server, command_port))
            conn.sendto(command, (ip_server, command_port))
            conn.sendto(command, (ip_server, command_port))
            conn.sendto(command, (ip_server, command_port))
            conn.sendto(command, (ip_server, command_port))


        else:
            Label(self, text="First press Start", fg='red').grid(row=6, column=1, sticky=W)

    def right_command(self):
        command = "X=-83%,Y=0%"
        if updated == True:
            conn.sendto(command, (ip_server, command_port))
            conn.sendto(command, (ip_server, command_port))
            conn.sendto(command, (ip_server, command_port))
            conn.sendto(command, (ip_server, command_port))
            conn.sendto(command, (ip_server, command_port))


        else:
            Label(self, text="First press Start", fg='red').grid(row=6, column=1, sticky=W)

    def stop_command(self):
        command = "X=0%,Y=0%"
        if updated == True:
            conn.sendto(command, (ip_server, command_port))
            conn.sendto(command, (ip_server, command_port))
            conn.sendto(command, (ip_server, command_port))
            conn.sendto(command, (ip_server, command_port))
            conn.sendto(command, (ip_server, command_port))


        else:
            Label(self, text="First press Start", fg='red').grid(row=6, column=1, sticky=W)


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


root = Tk()
root.title("CLIENT GUI")
root.geometry("400x360")
app = Application(root)

root.mainloop()
