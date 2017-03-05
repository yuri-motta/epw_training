from Tkinter import *

#create a window
root = Tk()

#modify the window
root.title("Buttons!")
root.geometry("200x100")

#cria o frame
app = Frame(root)
app.grid()

#cria o button
button1 = Button(app, text="This is a button!") #primeira forma de colocar texto no button
button1.grid()

button2 = Button(app)
button2.grid()
button2.configure(text ="This will show text!") #segunda forma de colocar texto no button

button3 = Button(app)
button3.grid()
button3["text"] = "This will show as well"

#main
root.mainloop()
