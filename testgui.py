from guizero import App,Box,  Text, TextBox
import tkinter


gui = App(height = 300, width = 500)

box = Box(gui, grid = [0,0])

#textmsg = Text(gui, text = 'enter mass to transfer', grid = [1,0])
text_box = TextBox(gui, grid = [1,2])
text_box.tk.place(x =200, y= 100)
#text_box.tk.pack(padx = 5, pady=10,side = tkinter.LEFT)
text = Text(gui, text = 'Micro mol')
text.tk.place(x =275, y= 100)
#text.tk.pack(padx=5, pady =20,side =tkinter.LEFT )
gui.display()
