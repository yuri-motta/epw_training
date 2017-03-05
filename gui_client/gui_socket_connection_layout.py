from Tkinter import *

class Application(Frame):

    def __init__(self,master):
        """Initialize the Frame"""
        Frame.__init__(self,master)
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        """Create two text entries to put IP and PORT of UDP socket connection"""

        #instructions
        self.instructions = Label(self,text="Insert IP and Port of the Socket UDP Server.")
        self.instructions.grid(row=0,column=0,sticky=W)

        #ip entry
        Label(self,text="IP:").grid(row=1,column=0,sticky=W)
        self.ip = Entry(self)
        self.ip.grid(row=2,column=0,sticky=W)

        #port entry
        Label(self, text="Port:").grid(row=3, column=0, sticky=W)
        self.port = Entry(self)
        self.port.grid(row=4, column=0, sticky=W)

        #submit button
        self.submit_button=Button(self, text="Submit",command = self.save_entry)
        self.submit_button.grid(row=5, column=0, sticky=W)


    def save_entry(self):
        ip = self.ip.get()
        port = self.port.get()
        
        # checking the entries
        Label(self, text=str(ip)).grid(row=8, column=0, sticky=W)
        Label(self, text=str(port)).grid(row=9, column=0, sticky=W)

root = Tk()
root.title("TEST INTERFACE")
root.geometry("500x500")
app = Application(root)

root.mainloop()
