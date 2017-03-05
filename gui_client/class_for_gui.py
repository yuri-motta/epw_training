# how to use a class with Tkinter

from Tkinter import *

class Application(Frame):
    """ a GUI application with 3 buttons"""
    def __init__(self,master):
        """Initialize the Frame"""
        Frame.__init__(self,master)
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        """ Create the 3 buttons that do nothing"""

        #creates the first button
        self.button1 = Button(self, text="This is the first button")
        self.button1.grid()

        # creates the second button
        self.button2 = Button(self, text="This is the second button")
        self.button2.grid()

        # creates the third button
        self.button3 = Button(self)
        self.button3.grid()
        self.button3["text"]="This is the third button"

#main program

root = Tk()
root.title("Lazy buttons")
root.geometry("200x100")

app = Application(root)

root.mainloop()