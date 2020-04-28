from tkinter import ttk
from tkinter import *
from chart.algogen_chart import Chart
from graphic.board import Board
from graphic.trainer import Trainer
from graphic.options import Options


class App(ttk.Frame):
    """
    Classe héritant de la classe Frame TKinter utilisé pour la création
    de l'interface graphique.
    Cette inferface permettra d'afficher les résultats de
    l'algortihme génétique ainsi qu'un plateau afin de jouer contre
    une intelligence artifcielle issu de cet algorithme.

    Attributs
    ---------
    model : model
       référence vers une instance de Core, qui est un objet permettant
       l'exécution de l'algorithme génétique.

    Methodes
    --------
    get_model()
        retourne le model
    build()
        créer une fenêtre puis appel la construction du menu dans
        celle-ci
    home_draw()
        construit le menu principal du programme dans la frame active
    training_draw()
        évenement déclenché lorsque le bouton Entrainement est appuyé
        Un objet Trainer est instancié ce qui permettra la construction
        et l'exécution de l'entrainement
    play_vs_ia()
        évenement qui affiche un plateau de bataille navale pour jouer
        avec une intelligence artificielle issu de la dernière
        génération calculée
    quit_app()
        évement qui quitte l'application
    chart()
        évenement qui affiche le menu de graphique
    options()
        évenement qui affiche le menu d'options
    clear_frame()
        Nettoie la fenêtre de tout items graphiques
    """
    def __init__(self, model):
        super().__init__(None)
        self.pack()
        self.model = model

    def get_model(self):
        return self.model

    def build(self):
        root = self.master
        root.title('AlgoGen Battleship')
        root.geometry("830x500")
        root.resizable(0, 0)
        self.home_draw()
        root.mainloop()

    def home_draw(self):
        self.clear_frame()
        root = self.master

        title = Label(text="AlgoGen Battleship", font=("Helvetica", 30))
        title.pack()
        # Frame contenant les 5 boutons princpaux du menu
        frame = Frame(root)
        ttk.Button(
            frame,
            text='Entraînement',
            command=self.training_draw,
            width=20).pack()
        ttk.Button(
            frame,
            text='Jouer vs IA Génétique',
            command=self.play_vs_ia,
            width=20).pack()
        ttk.Button(
            frame,
            text='IA vs IA',
            command=self.ia_vs_ia,
            width=20).pack()
        ttk.Button(
            frame,
            text='Statistiques',
            command=self.chart, width=20).pack()
        ttk.Button(
            frame,
            text='Options',
            command=self.options,
            width=20).pack(pady=5)
        ttk.Button(
            frame,
            text='Quitter',
            command=root.destroy,
            width=20).pack(pady=5)
        frame.pack(expand=YES)

        Label(root, text="Arnaud Peralta, Yohann Goffart, "
                         "Louis Pariente - Q1 2020", font="Helvetica")\
            .pack(side=BOTTOM)

    def training_draw(self):
        self.clear_frame()
        trainer = Trainer(self, self.model)
        trainer.draw()

    def play_vs_ia(self):
        self.clear_frame()
        board = Board(self)
        board.draw()

    def ia_vs_ia(self):
        self.clear_frame()
        board = Board(self, human=False)
        board.draw()

    def quit_app(self):
        self.master.quit

    def chart(self):
        self.clear_frame()
        chart = Chart(self, self.model)
        chart.build()

    def options(self):
        self.clear_frame()
        opt = Options(self.master, self)
        opt.build()

    def clear_frame(self):
        for widget in self.master.winfo_children():
            widget.pack_forget()

