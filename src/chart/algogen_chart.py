from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import graphic.options as o
import matplotlib

matplotlib.use("TkAgg")
DEFAULT_POPULATION_GEN = 1


class Chart(ttk.Frame):
    """
    Classe utilisé pour l'affichage de la partie Chart de
    l'interface graphique.

    Attributs
    ---------
    return_app : app
       référence vers l'objet App qui a instancié cette classe
    model : model
        référence vers l'instance singleton de Core

    Methodes
    --------
    build()
        construit le graphique dans l'interface graphique
    return_call()
        méthode callback pour l'affichage du menu
    """

    def __init__(self, app, model):
        super().__init__(None)
        self.return_app = app
        self.model = model

    def build(self):
        """
        Axe X (nb_gen): 1 -> 1000 générations
        Axe Y : (avg_shot) Nombre moyen de tir necessaires
        """
        root = self.master
        if self.model.pop.generation > DEFAULT_POPULATION_GEN:
            self.grid()
            avg_shot = [i for i in self.model.pop.gen_fit_score]
            nb_gen = [i for i in range(len(avg_shot))]
            figure = Figure(figsize=(8, 4), dpi=100)
            ax1 = figure.add_subplot(1, 1, 1)
            ax1.plot(nb_gen, avg_shot)
            ax1.set_title('FITNESS')
            ax1.set_xlabel('Nombre de génération')
            ax1.set_ylabel('Nombre de tir moyen')
            canvas = FigureCanvasTkAgg(figure, root)
            canvas.get_tk_widget()\
                .grid(row=1, column=0, padx=10, pady=10)
            ttk.Button(root, text='Retour', command=self.return_call)\
                .grid(row=0, column=0, sticky=W)
        else:
            Label(root, text="Un entrainement doit avoir été réalisé "
                             "pour afficher les statistiques",
                  font="Helvetica").pack(side=TOP)
            ttk.Button(root, text='Retour', command=self.return_call)\
                .pack(side=BOTTOM)
        root.mainloop()

    def return_call(self):
        """
        Nettoyage des éléments dans la fenêtre et appel l'affichage
        du menu.
        """
        for widget in self.return_app.master.winfo_children():
            widget.destroy()
        self.return_app.home_draw()
