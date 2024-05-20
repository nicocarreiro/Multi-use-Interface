import tkinter as tk
from tkinter import * #if you dont import this you need to put .tk before every function

window = tk.Tk()

# Nome da janela
window.title("exemplo")

# .pack() mostra o texto na janela
label = Label(window, text = "texto de exemplo").pack()
# label = Label(window, text = "texto de exemplo")
# label.pack()

# loop principal
window.mainloop()