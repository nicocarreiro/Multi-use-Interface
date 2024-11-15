import tkinter as tk
from tkinter import font as tkfont
from tkinter import *
import subprocess
import os
from multiprocessing import shared_memory
import numpy as np


pages = ["StartPage", "PageOne", "MapEditor"]
externalPrograms = ["", "", "gcc desenha.c -o desenha $(sdl2-config --cflags --libs) -lSDL2 -lm -lrt"]
externalProgramsCompiled = ["./braco", "", "./desenha"]
mapeditor = []

class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Interface Multi-Uso")
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
            # cria um frame para cada pagina, de uma lita de strings
            page_class = globals()[page_name]
            frame = page_class(parent=container, controller=self)
            self.frames[page_name] = frame

            # coloca todos os frames no mesmo lugar
            # a pilha de frames é organizada de acordo com a ordem de inserção
            # mostrando o frame mais recente
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
        Label(self, text="", height=4).pack()
        label = Label(self, text="Interface Multi-Uso", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        Label(self, text="", height=6).pack()
        button1 = Button(self, text="Manipulador", height=5, width=50,
                           command=lambda: controller.show_frame(pages[1]))
        button2 = Button(self, text="Configurações de mapa", height=5, width=50,
                            command=lambda: controller.show_frame(pages[2]))
        button3 = Button(self, text="Fechar programa", height=5, width=50,
                            command=end)
        button1.pack()
        button2.pack()
        button3.pack()


class PageOne(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        Label(self, text="", height=4).pack()
        
        label = Label(self, text="Simulação de manipulador", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        Label(self, text="", height=3).pack()

        temp = [""]

        self.clicked = StringVar()
        self.maps = OptionMenu(self, self.clicked, *temp)
        self.maps.pack()

        self.clickedConfig = StringVar()
        self.clickedConfig.set("") 
        self.scenes = OptionMenu(self, self.clickedConfig, *temp)
        self.scenes.pack()

        Label(self, text="", height=1).pack()

        configbraco = Button(self, text="Rodar simulação", height=4, width=50,
                           command=lambda: programOne("*/saves/cenarios/" + self.clicked.get(), "saves/config/" + self.clickedConfig.get()))
        configbraco.pack()
        runbraco = Button(self, text="Menu de configuração", height=4, width=50,
                           command=self.configMenu)
        runbraco.pack()
        back = Button(self, text="Voltar a pagina inicial", height=4, width=50,
                           command=lambda: controller.show_frame(pages[0]))
        back.pack()


    def updmaps(self):
        menu = self.maps['menu']
        menu.delete(0, 'end')  # Clear existing options
        for option in os.listdir("saves/cenarios"):
            if ("_caminho" not in option):
                menu.add_command(label=option, command=lambda value=option: self.clicked.set(value))
        
        menu = self.scenes['menu']
        menu.delete(0, 'end')  # Clear existing options
        for option in os.listdir("saves/config"):
            menu.add_command(label=option, command=lambda value=option: self.clickedConfig.set(value))


    def configMenu(self):
        def configSave():
            savedConfigs = os.listdir("saves/config")
            if (fileName.get().replace(" ", "") and (fileName.get() != "config")):
                name = fileName.get()
            else:
                name = "config"
            temp = 1
            if (name + ".bin" in savedConfigs):
                for _ in range(len(savedConfigs)):
                    if ((name + str(temp) + ".bin") in savedConfigs):
                        temp+=1
                name += "(" + str(temp) + ")"

            name="saves/config/" + name + ".bin"

            with open(name, "wb") as arquivo:
                njuntas_value = int(textNjuntas.get()) if textNjuntas.get() else 1
                tam_value = int(Tam.get()) if Tam.get() else 1
                pop_value = int(pop.get()) if pop.get() else 1

                arquivo.write(njuntas_value.to_bytes(4, byteorder='little'))
                arquivo.write(tam_value.to_bytes(4, byteorder='little'))
                arquivo.write(pop_value.to_bytes(4, byteorder='little'))
            
            self.updmaps()
            configWindow.destroy()


        def validate_int(P):
            if (P.isdigit() or P == "") and P != "0":
                return True
            else:
                return False

        vcmd = (self.register(validate_int), '%P')



        configWindow = Toplevel(self)
        configWindow.wm_title("config")

        textFileName = Label(configWindow, text="Nome do arquivo").grid(row=0)
        fileName = Entry(configWindow)
        fileName.insert(0,"config")
        fileName.grid(row=0, column=1)
        

        empty = Label(configWindow, text="")
        empty.grid(row=1)

        textNjuntas = Label(configWindow, text="Numero de juntas").grid(row=2)
        textNjuntas = Entry(configWindow, validate="key", validatecommand=vcmd)
        textNjuntas.insert(0,"30")
        textNjuntas.grid(row=2, column=1)


        textTam = Label(configWindow, text="Tamanho do manipulador").grid(row=3)
        Tam = Entry(configWindow, validate="key", validatecommand=vcmd)
        Tam.insert(0,"700")
        Tam.grid(row=3, column=1)


        textPop = Label(configWindow, text="Tamanho de população").grid(row=4)
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
        Label(self, text="", height=4).pack()
        label = Label(self, text="Configurações de mapa", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        Label(self, text="", height=5).pack()

        button = Button(self, text="Editor de mapa", height=3, width=40,
                           command=self.mapEditorWindow)
        button2 = Button(self, text="Voltar a pagina inicial", height=3, width=40,
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
        mapWindow.wm_title("Configurações do mapa")

        brushtxt = Label(mapWindow, width=20, text="Espessura do pincel", anchor='w')
        brushtxt.grid(row=0, column=0, rowspan=2)
        BrushSizeScale = Scale(mapWindow, from_=1, to=10, orient=HORIZONTAL, 
                               command=updater)
        BrushSizeScale.grid(row=0, column=1, rowspan=2)
        button3 = Button(mapWindow, text="Fechar e Salvar",
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

    subprocess.Popen(("./braco " + name + " " + name[:-4] + "_caminho.bin " + "{} {} {}".format(x,y,z)).split())


def end():
    app.quit()

if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()