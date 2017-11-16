from Tkinter import *
import socket
import subprocess
import time
import threading
from threading import Thread
import datetime


ip = "127.0.0.1"
port = 4444
updated = False

class Application(Frame):

    def __init__(self,master):
        """Initialize the Frame"""
        Frame.__init__(self,master)
        self.grid()
        self.create_widgets()

    def create_widgets(self):

        # instructions
        self.instructions = Label(self, text="WELCOME TO IEPW")
        self.instructions.grid(row=0, column=1, sticky=W)

        # ip entry
        Label(self, text="Command Server IP:").grid(row=1, column=1, sticky=W)
        self.ip_server = Entry(self)
        self.ip_server.grid(row=2, column=1, sticky=W)

        # port entry
        Label(self, text="Command Port:").grid(row=3, column=1, sticky=W)
        self.command_port = Entry(self)
        self.command_port.grid(row=4, column=1, sticky=W)

        # SAVE ip and port button
        self.button_save = Button(self, text="Update", command=self.update_ip_port)
        self.button_save.grid(row=5,column=1, sticky=W)

        #instructions
        Label(self, text="Commands").grid(row=0, column=9, sticky=W)

        #UP button
        self.button_up = Button(self, text="UP", command=self.up_command)
        self.button_up.grid(row=1, column =9)

        #DOWN button
        self.button_down = Button(self, text="DOWN", command=self.down_command)
        self.button_down.grid(row=3, column=9)

        #LEFT button
        self.button_left = Button(self, text="LEFT", command=self.left_command)
        self.button_left.grid(row=2, column=8)

        #RIGHT button
        self.button_right = Button(self, text="RIGHT", command=self.right_command)
        self.button_right.grid(row=2,column=10)

        #STOP button
        self.button_stop = Button(self, text="STOP", command=self.stop_command)
        self.button_stop.grid(row=2, column=9)

        #Selected command
        self.selected_command = Text(self,width=5,height=1, wrap=WORD)
        self.selected_command.grid(row=2,column=11)

        #Update the local ip
        Label(self, text="Please insert your IP:").grid(row=13, column=1, sticky=W)
        self.local_ip = Entry(self)
        self.local_ip.grid(row=14, column=1, sticky=W)


        # Update the local port
        Label(self, text="Video streaming port:").grid(row=16, column=1, sticky=W)
        self.video_port = Entry(self)
        self.video_port.grid(row=17, column=1, sticky=W)

        #VIDEO button
        self.button_start_video = Button(self, text="START VIDEO FEEDBACK", command=self.start_video_feedback)
        self.button_start_video.grid(row=19, column=1)


    def update_ip_port(self):
        global ip_server, command_port, conn, updated
        ip_server = str(self.ip_server.get())
        command_port = int(self.command_port.get())
        conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        Label(self, text="Updated!").grid(row=6, column=0, sticky=W)
        updated = True

        ## thread rtt
        rtt_measure_send =  RTT_sender()
        t1 = threading.Thread(target=rtt_measure_send.run)
        t1.setDaemon(True)
        t1.start()

    def up_command(self):
        command = "X=0%,Y=100%"
        if updated==True:
            conn.sendto(command, (ip_server, command_port))
            self.selected_command.delete(0.0, END)
            self.selected_command.insert(0.0, command)
        else:
            Label(self, text="First update IP and Port").grid(row=6, column=0, sticky=W)

    def down_command(self):
        command = "X=0%,Y=-100%"
        if updated == True:
            conn.sendto(command, (ip_server, command_port))
            self.selected_command.delete(0.0, END)
            self.selected_command.insert(0.0, command)
        else:
            Label(self, text="First update IP and Port").grid(row=6, column=0, sticky=W)

    def left_command(self):
        command = "X=100%,Y=0%"
        if updated == True:
            conn.sendto(command, (ip_server, command_port))
            self.selected_command.delete(0.0, END)
            self.selected_command.insert(0.0, command)
        else:
            Label(self, text="First update IP and Port").grid(row=6, column=0, sticky=W)

    def right_command(self):
        command = "X=-100%,Y=0%"
        if updated == True:
            conn.sendto(command, (ip_server, command_port))
            self.selected_command.delete(0.0, END)
            self.selected_command.insert(0.0, command)
        else:
            Label(self, text="First update IP and Port").grid(row=6, column=0, sticky=W)

    def stop_command(self):
        command = "X=0%,Y=0%"
        if updated == True:
            conn.sendto(command, (ip_server, command_port))
            self.selected_command.delete(0.0, END)
            self.selected_command.insert(0.0, command)
        else:
            Label(self, text="First update IP and Port").grid(row=6, column=0, sticky=W)

    def start_video_feedback(self):
        global  local_ip,video_port
        local_ip = str(self.local_ip.get())
        video_port = str(self.video_port.get())
        #os.system('ffplay -fflags nobuffer -flags low_delay -framedrop -strict experimental udp://'+ local_ip +':' + video_port)
        #linux_command = 'ffplay -fflags nobuffer -flags low_delay -framedrop -strict experimental udp://'+ local_ip +':' + video_port
        url = 'udp://' + local_ip + ":" + video_port
        #subprocess.call(["ffplay","-fflags","nobuffer","-flags","low_delay","-framedrop","-strict","experimental","%s" % url])

        video_stream = client_video_stream()
        video_stream.run()

class client_video_stream(Thread):

    def __init__(self):
        global local_ip, video_port
        Thread.__init__(self)
        #local_ip = str(local_ip.get())
        #video_port = str(video_port.get())
        # os.system('ffplay -fflags nobuffer -flags low_delay -framedrop -strict experimental udp://'+ local_ip +':' + video_port)
        # linux_command = 'ffplay -fflags nobuffer -flags low_delay -framedrop -strict experimental udp://'+ local_ip +':' + video_port
        self.url = 'tcp://' + local_ip + ":" + video_port + "?listen"
    def run(self):
        subprocess.Popen(["ffplay", "-fflags", "nobuffer", "-flags", "low_delay","%s" % self.url])

class RTT_sender(Thread):

    def __init__(self):
        Thread.__init__(self)

    def run(self):
        global ip_server, conn


        while True:
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
            conn.sendto(self.message, (ip_server, command_port))
            time.sleep(1)


root = Tk()
root.title("CLIENT GUI")
root.geometry("500x400")
app = Application(root)

root.mainloop()