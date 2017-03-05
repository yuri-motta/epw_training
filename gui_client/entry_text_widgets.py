from Tkinter import *

class Application(Frame):

    def __init__(self,master):
        """Initialize the Frame"""
        Frame.__init__(self,master)
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        """create button, text and entry widgets"""
        self.instruction = Label(self, text="Enter the password")
        self.instruction.grid(row = 0, column = 0, columnspan = 2, sticky = W) # W = West

        self.password = Entry(self)
        self.password.grid(row = 1, column = 1, sticky = W)

        self.submit_button = Button(self, text = "Submit", command = self.reveal)
        self.submit_button.grid(row = 2, column = 2, sticky = W)

        self.text = Text(self,width = 35, height = 5, wrap = WORD) #wrap is the type of content
        self.text.grid(row = 3, column = 3, columnspan = 2, sticky = W)

    def reveal(self):
        """Display a message based on password typed in"""
        content = self.password.get()

        if content == "password":
            message = "You have acess to something special"

        else:
            message = "Acess Denied \n"
        self.text.delete(0.0,END)
        self.text.insert(0.0,message)

root = Tk()
root.title("Password")
root.geometry("500x250")
app = Application(root)

root.mainloop()
