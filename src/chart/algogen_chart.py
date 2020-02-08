from tkinter import *
from tkinter import ttk
from tkinter.ttk import *

import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

matplotlib.use("TkAgg")


class Chart(ttk.Frame):
    def __init__(self, app=None):
        super().__init__(None)
        self.return_app = app
        self.grid()

    def build(self):
        root = self.master
        """
        Axe X (nb_gen): 1 -> 1000 générations
        Axe Y : (avg_shot) Nombre moyen de tir necessaires
        """
        # à faire : Supprimer les 2 lignes suivantes et ajouter les tableaux en argument de la fonction

        nb_gen = [i for i in range(1001)]
        avg_shot = [i for i in nb_gen]
        figure = Figure(figsize=(8, 4), dpi=100)
        ax1 = figure.add_subplot(1, 1, 1)
        ax1.plot(nb_gen, avg_shot)
        ax1.set_title('FITNESS')
        ax1.set_xlabel('Nombre de génération')
        ax1.set_ylabel('Nombre de tir moyen')
        canvas = FigureCanvasTkAgg(figure, root)
        canvas.get_tk_widget().grid(row=1, column=0, padx=10, pady=10)

        """
        figure2 = Figure(figsize=(4, 4), dpi=100)
        figure2.add_subplot(1, 1, 1)
        canvas2 = FigureCanvasTkAgg(figure,root)
        canvas2.get_tk_widget().grid(row=1, column=1, padx= 3)
        """
        ttk.Button(root, text='Retour', command=self.return_call).grid(row=0, column=0, sticky=W)

        root.mainloop()

    def return_call(self):
        for widget in self.return_app.master.winfo_children():
            widget.destroy()
        self.return_app.home_draw()
