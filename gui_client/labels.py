#fist labels
from Tkinter import *

#create the window
root = Tk()

#modify the window
root.title("Labeler")
root.geometry("200x50")

#cria o frame
app = Frame(root)
app.grid() # coloca na tela o objeto criado

label = Label(app, text="This is a label!")
label.grid() # coloca na tela o objeto criado

#main loop
root.mainloop()