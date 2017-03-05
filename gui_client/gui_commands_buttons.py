# buttons with events

from Tkinter import *

class Application(Frame):

    def __init__(self,master):
        """Initialize the Frame"""
        Frame.__init__(self,master)
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        #instructions
        Label(self,text="Click on desired direction").grid(row=0, column =0, sticky = W)
        Label(self, text="Commands").grid(row=1, column=0, sticky=W)

        #UP button
        self.button_up = Button(self, text="UP", command=self.up_command)
        self.button_up.grid(row=2, column =4)

        #DOWN button
        self.button_down = Button(self, text="DOWN", command=self.down_command)
        self.button_down.grid(row=4, column=4)

        #LEFT button
        self.button_left = Button(self, text="LEFT", command=self.left_command)
        self.button_left.grid(row=3, column=3)

        #RIGHT button
        self.button_right = Button(self, text="RIGHT", command=self.right_command)
        self.button_right.grid(row=3,column=5)

        #STOP button
        self.button_stop = Button(self, text="STOP", command=self.stop_command)
        self.button_stop.grid(row=3, column=4)

        #Selected command
        self.selected_command = Text(self,width=10,height=5, wrap=WORD)
        self.selected_command.grid(row=10,column=4,sticky=W)

    def up_command(self):
        command = "UP command selected"
        self.selected_command.delete(0.0, END)
        self.selected_command.insert(0.0, command)

    def down_command(self):
        command = "DOWN command selected"
        self.selected_command.delete(0.0, END)
        self.selected_command.insert(0.0, command)

    def left_command(self):
        command = "LEFT command selected"
        self.selected_command.delete(0.0, END)
        self.selected_command.insert(0.0, command)

    def right_command(self):
        command = "RIGHT command selected"
        self.selected_command.delete(0.0, END)
        self.selected_command.insert(0.0, command)

    def stop_command(self):
        command = "STOP command selected"
        self.selected_command.delete(0.0, END)
        self.selected_command.insert(0.0, command)

root = Tk()
root.title("COMMANDS")
root.geometry("500x300")
app = Application(root)

root.mainloop()