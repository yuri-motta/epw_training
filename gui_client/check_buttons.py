from Tkinter import *

class Application(Frame):

    def __init__(self,master):
        """Initialize the Frame"""
        Frame.__init__(self,master)
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        """Create widgets for movie type choice"""
        Label(self,text="Choose your favority movie type").grid(row=0,column=0,sticky=W)

        #instructions
        Label(self,text="Select all that apply:").grid(row=1,column=0,sticky=W)

        #commedy check button
        self.comedy = BooleanVar()
        Checkbutton(self, text = "Comedy", variable= self.comedy, command = self.update_text).grid(row=2 , column=0, sticky = W)

        #drama check button
        self.drama = BooleanVar()
        Checkbutton(self, text = "Drama", variable = self.drama, command = self.update_text).grid(row=3 , column=0, sticky = W)

        #romance check button
        self.romance = BooleanVar()
        Checkbutton(self, text = "Romance", variable = self.romance, command = self.update_text).grid(row=4, column=0, stick=W)

        self.result = Text(self,width=40, height = 5, wrap = WORD)
        self.result.grid(row=5, column=0, columnspan =3)

    def update_text(self):
        """Update widget and display favorite movie types"""
        likes = ""

        if self.comedy.get():
            likes += "You like comedy."

        if self.drama.get():
            likes += "You like drama."

        if self.romance.get():
            likes += "You like romance"

        self.result.delete(0.0,END)
        self.result.insert(0.0,likes)

root = Tk()
root.title("Check buttons!")
root.geometry("300x200")
app = Application(root)

root.mainloop()