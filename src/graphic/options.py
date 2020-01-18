from tkinter import ttk


class Options(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()

    def build(self):
        root = self.master
        qb = ttk.Button(root, text='Quitter', command=root.quit)
        qb.pack()
        root.mainloop()
