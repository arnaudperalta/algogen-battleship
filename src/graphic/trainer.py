from tkinter import *
from tkinter import ttk
import graphic.options as o
from core.algogen_core import Core
from math import ceil

# Classe héritant de la classe Frame de tkinter

# TODO quand on quitte le trainer il faut nettoyer tout le model car
#  les options peuvent se faire modifier


class Trainer(ttk.Frame):
    """
    Classe héritant de la classe Frame de TKinter qui affichera les
    résultats de l'entrainement des individus concernant l'algorithme
    génétique

    Attributs
    ---------
    model : model
        référence vers une instance de Core
    base_app : base_app
        référence vers le singleton App

    Methodes
    --------
    draw()
        construit dans la fenêtre l'espace où les résultats de
        l'algorithme génétique seront stockés
    back()
        effectue un retour au menu principal
    clear()
        nettoie la fenêtre de tout les items dessinés avant
    fulltrain()
        appel via la classe Core l'exécution d'un entrainement complet
    steptrain()
        appel via la classe Core l'éxecution d'un entrainement pas
        par pas
    printgen()
        affiche les résultats de l'évaluation de la dernière génération
        calculée
    reset()
        Réinitialise la population de la classe Core
    """
    def __init__(self, base_app, model):
        super().__init__(base_app.master)
        self.model = model
        self.base_app = base_app
        root = base_app.master
        self.results = Text(
            self.master,
            width=100,
            height=28,
            bg="black"
        )
        self.results.tag_configure(tagName="Good", foreground="green")
        self.results.tag_configure(tagName="Bad", foreground="red")
        self.results.tag_configure(tagName="Normal", foreground="white")
        self.fulltrain_button = ttk.Button(
            root,
            text="Entrainement complet",
            command=self.fulltrain
        )
        self.steptrain_button = ttk.Button(
            root,
            text="Entrainement pas à pas",
            command=self.steptrain
        )
        self.back_button = ttk.Button(
            root,
            text="Retour",
            command=self.back
        )
        self.reset_button = ttk.Button(
            root,
            text="Réinitialiser",
            command=self.reset
        )

    def draw(self):
        self.results.pack(side=TOP)
        self.fulltrain_button.pack(side=RIGHT, padx=30)
        self.steptrain_button.pack(side=RIGHT, padx=30)
        self.reset_button.pack(side=RIGHT, padx=60)
        self.back_button.pack(side=RIGHT, padx=30)

    def back(self):
        self.clear()
        self.base_app.home_draw()

    def clear(self):
        for widget in self.base_app.master.winfo_children():
            widget.destroy()

    def fulltrain(self):
        n = self.model.pop.generation
        for i in range(n, o.options_nbr_gen):
            self.printgen(self.model.train())
            self.update()

    def steptrain(self):
        if self.model.pop.generation < o.options_nbr_gen:
            self.printgen(self.model.train())
            self.update()

    def printgen(self, tab):
        self.results.insert(
            END,
            "Génération " + str(self.model.pop.generation) + " : ",
            "Normal"
        )
        for i in tab:
            if i[1] < ceil(0.4 * (o.options_grid_size**2)):
                self.results.insert(END, str(i[1]), "Good")
                self.results.insert(END, " | ", "Normal")
            elif i[1] > ceil(0.9 * (o.options_grid_size**2)):
                self.results.insert(END, str(i[1]), "Bad")
                self.results.insert(END, " | ", "Normal")
            else:
                self.results.insert(END, str(i[1]) + " | ", "Normal")
        self.results.insert(END, "\n")
        self.results.see(END)

    def reset(self):
        self.model.clear()
        self.results.insert(END, "Population réinitalisée.\n", "Normal")
        self.results.see(END)
        self.update()
