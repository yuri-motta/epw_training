# buttons with events

from Tkinter import *

class Application(Frame):

    def __init__(self,master):
        """Initialize the Frame"""
        Frame.__init__(self,master)
        self.grid()
        self.button_clicks = 0  #counts the number of button clicks
        self.create_widgets()

    def create_widgets(self):
        """Create button which displays the number of clicks"""
        self.button = Button(self)
        self.button["text"] = "Total clicks: 0"
        self.button["command"] = self.update_count
        self.button.grid()

    def update_count(self):
        """Increase the clicks count and display the total"""
        self.button_clicks += 1
        self.button["text"] = "Total clicks: " + str(self.button_clicks)

root = Tk()
root.title("Event Buttons")
root.geometry("200x100")

app = Application(root)
root.mainloop()