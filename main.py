import tkinter as tk
from tkinter import font as tkfont
from tkinter import *
import subprocess
from os import *
from multiprocessing import shared_memory
import numpy as np

pages = ["StartPage", "PageOne", "MapEditor"]
externalPrograms = ["", "", "gcc desenha.c -o desenha $(sdl2-config --cflags --libs) -lSDL2 -lm -lrt"]
externalProgramsCompiled = ["./braco", "", "./desenha cenario.bin"]
mapeditor = []

class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

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
        frame.tkraise()


class StartPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        label = Label(self, text="multi usage interface", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button1 = Button(self, text="braço", height=2, width=11,
                           command=lambda: controller.show_frame(pages[1]))
        button2 = Button(self, text="map settings", height=2, width=11,
                            command=lambda: controller.show_frame(pages[2]))
        button3 = Button(self, text="close program", height=2, width=11,
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
        runbraco = Button(self, text="rodar braco",
                           command=programOne)
        runbraco.pack()
        back = Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame(pages[0]))
        back.pack()



class MapEditor(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        label = Label(self, text="This is page 2", font=controller.title_font)
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


        if not path.isfile(externalProgramsCompiled[2].split()[0][2:]):
            system(externalPrograms[2])
        program = subprocess.Popen(externalProgramsCompiled[2].split())
        

def programOne():
    #subprocess.Popen(externalPrograms[0].split())
    subprocess.Popen(externalProgramsCompiled[0].split())


def end():
    app.quit()

if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()