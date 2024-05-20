import tkinter


window = tkinter.Tk()

def printlist():
    print (inputj.get(), inputcomp.get(), inputnumi.get(), inputmut.get())

# Nome da janela
window.title("exemplo")

tkinter.Label(window, text = "numero de juntas").grid(row = 0) 
inputj = tkinter.Entry(window)
inputj.grid(row = 0, column = 1)

tkinter.Label(window, text = "comprimento total").grid(row = 1) 
inputcomp = tkinter.Entry(window)
inputcomp.grid(row = 1, column = 1)

tkinter.Label(window, text = "numero de individuos").grid(row = 2) 
inputnumi = tkinter.Entry(window)
inputnumi.grid(row = 2, column = 1)

tkinter.Label(window, text = "taxa de mutação").grid(row = 3) 
inputmut = tkinter.Entry(window)
inputmut.grid(row = 3, column = 1)


button = tkinter.Button(text = "pronto", command=printlist()).grid(row = 4)
                        
# loop principal
window.mainloop()