import tkinter as tk
from tkinter import font as tkfont
from tkinter import *
import subprocess
import os
from multiprocessing import shared_memory
import numpy as np
import shutil


pages = ["StartPage", "PageOne", "MapEditor"]
externalPrograms = ["", "", "gcc desenha.c -o desenha $(sdl2-config --cflags --libs) -lSDL2 -lm -lrt"]
externalProgramsCompiled = ["./braco", "", "./desenha"]
mapeditor = []

class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.geometry("900x600")

        self.title_font = tkfont.Font(family='Helvetica', size=24, weight="bold", slant="italic")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for page_name in pages:
            # Get the class object from the string name
            page_class = globals()[page_name]
            frame = page_class(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")


        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        if page_name == "PageOne":
            self.frames[page_name].updmaps()
        frame.tkraise()


class StartPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        label = Label(self, text="multi usage interface", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        space = Label(self, text="", height=10)
        space.pack()
        button1 = Button(self, text="braço", height=5, width=50,
                           command=lambda: controller.show_frame(pages[1]))
        button2 = Button(self, text="map settings", height=5, width=50,
                            command=lambda: controller.show_frame(pages[2]))
        button3 = Button(self, text="close program", height=5, width=50,
                            command=end)
        button1.pack()
        button2.pack()
        button3.pack()


class PageOne(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        label = Label(self, text="braço mecanico", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        space = Label(self, text="", height=3)
        space.pack()


        self.clicked = StringVar()
        savedmaps = os.listdir("saves/cenarios")
        self.clicked.set("") 
        self.maps = OptionMenu(self, self.clicked, *savedmaps)
        self.maps.pack()

        self.clickedScene = StringVar()
        savedScenes = os.listdir("saves/config")
        savedScenes.append("")
        self.clickedScene.set("") 
        self.scenes = OptionMenu(self, self.clickedScene, *savedScenes)
        self.scenes.pack()


        configbraco = Button(self, text="rodar braco", height=4, width=50,
                           command=lambda: programOne("saves/cenarios/" + self.clicked.get(), "saves/config/" + self.clickedScene.get()))
        configbraco.pack()
        runbraco = Button(self, text="Config Menu", height=4, width=50,
                           command=self.configMenu)
        runbraco.pack()
        back = Button(self, text="Go to the start page", height=4, width=50,
                           command=lambda: controller.show_frame(pages[0]))
        back.pack()


    def updmaps(self):
        menu = self.maps['menu']
        menu.delete(0, 'end')  # Clear existing options
        for option in os.listdir("saves/cenarios"):
            menu.add_command(label=option, command=lambda value=option: self.clicked.set(value))
        
        menu = self.scenes['menu']
        menu.delete(0, 'end')  # Clear existing options
        for option in os.listdir("saves/config"):
            menu.add_command(label=option, command=lambda value=option: self.clickedScene.set(value))


    def configMenu(self):
        def configSave():
            temp = 0
            for _ in os.listdir("saves/config"):
                temp+=1
            name = "config" + str(temp)
            if (fileName.get().replace(" ", "") and (fileName.get() != "config")):
                name = fileName.get()
                temp = 0

                while os.path.isfile(name + ".bin"):
                    temp+=1
                if temp:
                    name+=str(temp)

            name="saves/config/" + name + ".bin"

            with open(name, "wb") as arquivo:
                njuntas_value = int(textNjuntas.get()) if textNjuntas.get() else 1
                tam_value = int(Tam.get()) if Tam.get() else 1
                pop_value = int(pop.get()) if pop.get() else 1

                arquivo.write(njuntas_value.to_bytes(4, byteorder='little'))
                arquivo.write(tam_value.to_bytes(4, byteorder='little'))
                arquivo.write(pop_value.to_bytes(4, byteorder='little'))



        def validate_int(P):
            if (P.isdigit() or P == "") and P != "0":
                return True
            else:
                return False

        vcmd = (self.register(validate_int), '%P')



        configWindow = Toplevel(self)
        configWindow.wm_title("config")

        textFileName = Label(configWindow, text="File Name").grid(row=0)
        fileName = Entry(configWindow)
        fileName.insert(0,"config")
        fileName.grid(row=0, column=1)
        

        empty = Label(configWindow, text="")
        empty.grid(row=1)

        textNjuntas = Label(configWindow, text="Number of Joints").grid(row=2)
        textNjuntas = Entry(configWindow, validate="key", validatecommand=vcmd)
        textNjuntas.insert(0,"30")
        textNjuntas.grid(row=2, column=1)


        textTam = Label(configWindow, text="Arm length").grid(row=3)
        Tam = Entry(configWindow, validate="key", validatecommand=vcmd)
        Tam.insert(0,"700")
        Tam.grid(row=3, column=1)


        textPop = Label(configWindow, text="Population size").grid(row=4)
        pop = Entry(configWindow, validate="key", validatecommand=vcmd)
        pop.insert(0,"100")
        pop.grid(row=4, column=1)
        

        #textNmutacao = Label(configWindow, text="Starting Mutation").grid(row=5)
        #Nmutacao = Entry(configWindow).grid(row=5, column=1)

        empty2 = Label(configWindow, text="")
        empty2.grid(row=6)

        save = Button(configWindow, text="     Save     ", command=configSave).grid(row=7, columnspan=2)




class MapEditor(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        label = Label(self, text="Map Settings", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = Button(self, text="open map editor",
                           command=self.mapEditorWindow)
        button2 = Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame(pages[0]))
        button.pack()
        button2.pack()
        

    def mapEditorWindow(self):
        def updater(event):
            BrushSize = BrushSizeScale.get()
            array[0] = BrushSize
        def closeMap():
            shm.close()
            shm.unlink()
            mapWindow.destroy()
            program.terminate()

        size = np.int64().nbytes
        shm = shared_memory.SharedMemory(name="posix_shm", create=True, size=size)
        array = np.ndarray((1,), dtype=np.int64, buffer=shm.buf)
        array[0] = 1

        mapWindow = Toplevel(self)
        mapWindow.wm_title("map options")

        brushtxt = Label(mapWindow, width=15, text="brush size", anchor='w')
        brushtxt.grid(row=0, column=0, rowspan=2)
        BrushSizeScale = Scale(mapWindow, from_=1, to=10, orient=HORIZONTAL,
                               command=updater)
        BrushSizeScale.grid(row=0, column=1, rowspan=2)
        button3 = Button(mapWindow, text="close",
                           command=closeMap)
        button3.grid(row=2, columnspan=2)


        if not os.path.isfile(externalProgramsCompiled[2].split()[0][2:]):
            os.system(externalPrograms[2])
        program = subprocess.Popen((externalProgramsCompiled[2] + " saves/cenarios/cenario" + str(len(os.listdir("saves/cenarios"))) + ".bin").split())
        

def programOne(name, config):
    os.system("./a_star " + name)
    with open(config, "rb") as arquivo:
        data = arquivo.read(12)
    x, y, z = (int.from_bytes(data[0:4], byteorder="little")), (int.from_bytes(data[4:8], byteorder="little")), (int.from_bytes(data[8:12], byteorder="little"))

    os.system("./braco " + name + " " + name[:-4] + "_caminho.bin " + "{} {} {}".format(x,y,z))


def end():
    app.quit()

if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()