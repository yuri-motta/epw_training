from Tkinter import *
import socket

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
        self.instructions = Label(self, text="Insert IP and Port of the Socket UDP Server.")
        self.instructions.grid(row=0, column=0, sticky=W)

        # ip entry
        Label(self, text="IP:").grid(row=1, column=0, sticky=W)
        self.ip = Entry(self)
        self.ip.grid(row=2, column=0, sticky=W)

        # port entry
        Label(self, text="Port:").grid(row=3, column=0, sticky=W)
        self.port = Entry(self)
        self.port.grid(row=4, column=0, sticky=W)

        # SAVE ip and port button
        self.button_save = Button(self, text="Update IP and Port.", command=self.update_ip_port)
        self.button_save.grid(row=5,column=0, sticky=W)

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


    def update_ip_port(self):
        global ip, port, conn, updated
        ip = str(self.ip.get())
        port = int(self.port.get())
        conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        Label(self, text="Updated!").grid(row=6, column=0, sticky=W)
        updated = True

    def up_command(self):
        command = "UP command selected"
        if updated==True:
            conn.sendto(command, (ip, port))
            self.selected_command.delete(0.0, END)
            self.selected_command.insert(0.0, command)
        else:
            Label(self, text="First update IP and Port").grid(row=6, column=0, sticky=W)

    def down_command(self):
        command = "DOWN command selected"
        if updated == True:
            conn.sendto(command, (ip, port))
            self.selected_command.delete(0.0, END)
            self.selected_command.insert(0.0, command)
        else:
            Label(self, text="First update IP and Port").grid(row=6, column=0, sticky=W)

    def left_command(self):
        command = "LEFT command selected"
        if updated == True:
            conn.sendto(command, (ip, port))
            self.selected_command.delete(0.0, END)
            self.selected_command.insert(0.0, command)
        else:
            Label(self, text="First update IP and Port").grid(row=6, column=0, sticky=W)

    def right_command(self):
        command = "RIGHT command selected"
        if updated == True:
            conn.sendto(command, (ip, port))
            self.selected_command.delete(0.0, END)
            self.selected_command.insert(0.0, command)
        else:
            Label(self, text="First update IP and Port").grid(row=6, column=0, sticky=W)

    def stop_command(self):
        command = "STOP command selected"
        if updated == True:
            conn.sendto(command, (ip, port))
            self.selected_command.delete(0.0, END)
            self.selected_command.insert(0.0, command)
        else:
            Label(self, text="First update IP and Port").grid(row=6, column=0, sticky=W)

root = Tk()
root.title("COMMANDS")
root.geometry("800x400")
app = Application(root)

root.mainloop()