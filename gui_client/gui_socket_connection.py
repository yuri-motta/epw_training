from Tkinter import *
import socket
from threading import Thread

ip = "127.0.0.1"
port = 4444

class Application(Frame):

    def __init__(self, master):
        """Initialize the Frame"""
        Frame.__init__(self, master)
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        """Create two text entries to put IP and PORT of UDP socket connection"""

        global message, ip, port
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

        # message
        Label(self, text="Message:").grid(row=5, column=0, sticky=W)
        self.message = Entry(self)
        self.message.grid(row=6, column=0, sticky=W)

        # send message button
        self.button = Button(self, text="Send message", command=self.send_message)
        self.button.grid(row=9, column=0, sticky=W)


    def send_message(self):
        ip = str(self.ip.get())
        port = int(self.port.get())
        message = str(self.message.get())
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.conn.sendto(message, (ip, port))

root = Tk()
root.title("TEST INTERFACE")
root.geometry("500x500")
app = Application(root)

root.mainloop()

