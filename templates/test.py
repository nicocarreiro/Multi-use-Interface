from tkinter import *
import tkinter as tk

class MainWindow(tk.Frame):
    counter = 0
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.button = tk.Button(self, text="Create new hotlink",
                            command=self.create_window)
        self.button.pack(side="top")

    def create_window(self):
        self.counter += 1
        t = tk.Toplevel(self)
        t.wm_title("Create New Hotlink")
        fields = 'Hotlink Name', 'URL'

        def fetch(entries):
            for entry in entries:
                field = entry[0]
                text = entry[1].get()
                print('%s: "%s"' % (field, text))

        def makeform(root, fields):
            entries = []
            for field in fields:
                row = Frame(root)
                lab = Label(row, width=15, text=field, anchor='w')
                ent = Entry(row)
                row.pack(side=TOP, fill=X, padx=5, pady=5)
                lab.pack(side=LEFT)
                ent.pack(side=RIGHT, expand=YES, fill=X)
                entries.append((field, ent))
            return entries

        def button2():
            newButton = tk.Button(root, text=fields[0])

        ents = makeform(t, fields)
        t.bind('<Return>', (lambda event, e=ents: fetch(e)))
        b2 = Button(t, text='Save', command=button2())
        b2.pack(side=LEFT, padx=5, pady=5)

if __name__ == "__main__":
    root = tk.Tk()
    main = MainWindow(root)
    main.pack(side="top", fill="both", expand=True)
    root.mainloop()