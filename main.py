import tkinter as tk
from tkinter import font as tkfont
from tkinter import *
import subprocess
import os
from multiprocessing import shared_memory
import numpy as np
import shutil
import json

# Dados iniciais
data = {
    "randomSeed": 11847429,
    "environment": {
        "placePheromoneRate": 1,
        "pheromoneEvaporationRate": 15
    },
    "anthills": [
        {
            "id": 0,
            "posX": 0.0,
            "posY": 0.006,
            "size": 0.006,
            "antEspecifications": [0],
            "antAmounts": [1000],
            "foodDelivered": 0
        },
        {
            "id": 1,
            "posX": 0.0,
            "posY": 0.0,
            "size": 0.006,
            "antEspecifications": [],
            "antAmounts": [],
            "foodDelivered": 0
        }
    ],
    "foodSources": [
        {
            "id": 0,
            "posX": -0.060,
            "posY": 0.0,
            "size": 0.006,
            "foodAmount": 10000
        },
        {
            "id": 1,
            "posX": 0.060,
            "posY": 0.0,
            "size": 0.006,
            "foodAmount": 10000
        },
        {
            "id": 2,
            "posX": 0.0,
            "posY": -0.06,
            "size": 0.006,
            "foodAmount": 10000
        },
        {
            "id": 3,
            "posX": 0.0,
            "posY": 0.06,
            "size": 0.006,
            "foodAmount": 10000
        }
    ],
    "ants": [
        {
            "antEspecification": 0,
            "nestID": 0,
            "size": 0.002,
            "velocity": 0.0004,
            "state": 0,
            "pheromoneType": 0,
            "placePheromoneIntensity": 60,
            "lifeTime": 1250,
            "viewFrequency": 1,
            "antSensorParameters": [
                {
                    "xCenterAntDistance": 0.004,
                    "yCenterAntDistance": 0.004,
                    "positionAngle": -45,
                    "sensorPixelRadius": 2,
                    "sensorType": 0
                },
                {
                    "xCenterAntDistance": 0.004,
                    "yCenterAntDistance": 0.004,
                    "positionAngle": 45,
                    "sensorPixelRadius": 2,
                    "sensorType": 0
                }
            ]
        }
    ]
}

pages = ["StartPage", "PageOne", "MapEditor"]
externalPrograms = ["COMPILE MESSAGE", "", "gcc desenha.c -o desenha $(sdl2-config --cflags --libs) -lSDL2 -lm -lrt"]
externalProgramsCompiledChecker = ["COMPILED PROGRAM NAME", "", "desenha"]
externalProgramsCompiled = ["RUN MESSAGE", "", "./desenha"]
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
        label = Label(self, text="Hardware Accelerated Ant Colony", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        space = Label(self, text="", height=10)
        space.pack()
        button1 = Button(self, text="Ant Colony Options", height=5, width=50,
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
        def updateAnthill():
            search = int(anthillid[0].get())
            for anthill in data["anthills"]:
                if anthill["id"] == search:
                    anthill["antAmounts"].append(int(anthillamount[0].get()))
        Frame.__init__(self, parent)
        self.controller = controller
        label = Label(self, text="Hardware Accelerated Ant Colony", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        space = Label(self, text="", height=7)
        space.pack()
        savedmaps = os.listdir("saves")
        self.clicked = StringVar(value=savedmaps[0])
        self.maps = OptionMenu(self, self.clicked, *savedmaps)
        self.maps.pack()

        anthillframe = Frame(self)
        anthillframe.pack()
        anthillid = Entry(anthillframe), Label(anthillframe, text="anthillid")
        anthillid[1].pack(side=LEFT)
        anthillid[0].pack(side=RIGHT)

        anthillframe = Frame(self)
        anthillframe.pack()
        anthillamount = Entry(anthillframe), Label(anthillframe, text="anthillamount")
        anthillamount[1].pack(side=LEFT)
        anthillamount[0].pack(side=RIGHT)

        addAnthill = Button(self, text="add anthill", command=updateAnthill)
        addAnthill.pack()
        runbraco = Button(self, text="run ant colony", height=4, width=50,
                           command=lambda: programOne("saves/" + self.clicked.get()))
        runbraco.pack()
        back = Button(self, text="Go to the start page", height=4, width=50,
                           command=lambda: controller.show_frame(pages[0]))
        back.pack()
    def updmaps(self):
            menu = self.maps['menu']
            menu.delete(0, 'end')  # Clear existing options
            for option in os.listdir("saves"):
                menu.add_command(label=option, command=lambda value=option: self.clicked.set(value))



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


        if not os.path.isfile(externalProgramsCompiledChecker[2]):
            os.system(externalPrograms[2])
        program = subprocess.Popen((externalProgramsCompiled[2] + " saves/cenario" + str(len(os.listdir("saves"))) + ".bin").split())
        

def programOne(name):
    with open("dados.json", "w") as arquivo:
        json.dump(data, arquivo, indent=4)
    #subprocess.Popen(externalPrograms[0].split())
    shutil.copy(name, "cenario.bin")
    subprocess.Popen(externalProgramsCompiled[0].split())
    

def end():
    app.quit()

if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()