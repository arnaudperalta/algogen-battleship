import json
from tkinter import ttk
from tkinter import IntVar

"""
Variables globales de paramètres :
    options_nbr_gen:
        Nombre de générations que l'entrainement devra calculer
    options_saved_percentage:
        Pourcentage d'invidus conservé après la fitness
    options_mutation_chance:
        Probabilité qu'un gêne d'un individu soit muté
    options_def_gen:
        Nombre de gènes par individu
    options_nbr_idv:
        Nombre d'individu par population
    options_grid_size:
        Taille de la grille de bataille navale
    options_ship_number:
        Nombre de bateaux par grille
"""
options_nbr_gen = 0
options_saved_percentage = 0
options_mutation_chance = 0
options_def_gen = 0
options_nbr_idv = 0
options_grid_size = 0
options_ship_number = 0


class Options(ttk.Frame):
    """
    Classe utilisé pour l'affichage et la gestion des options
    comprenant la lecture et l'écriture dans un fichier.

    Attributs
    ---------
    return_app : app
       référence vers l'objet App qui a instancié cette classe
    nbr_gen & saved_percentage & mutation_chance
    & def_gen & nbr_idv & grid_size & ship_number:
        Variable où sont stockées les entrées utilisateur dans
        l'interface graphique.

    Methodes
    --------
    build()
        construit le menu de paramètrage dans l'interface graphique.
    return_call()
        méthode callback pour l'affichage du menu
    save_option()
        assigne aux variables globales leurs équivalent en variables
        d'entrée utilisateur puis écrit dans cfg/option.json
        les paramètres à sauvegarder.
    """

    def __init__(self, master=None, app=None):
        super().__init__(master)
        self.return_app = app
        self.nbr_gen = IntVar()
        self.saved_percentage = IntVar()
        self.mutation_chance = IntVar()
        self.def_gen = IntVar()
        self.nbr_idv = IntVar()
        self.grid_size = IntVar()
        self.ship_number = IntVar()

    def build(self):
        root = self.master
        global options_nbr_gen
        self.nbr_gen.set(options_nbr_gen)
        global options_saved_percentage
        self.saved_percentage.set(options_saved_percentage)
        global options_mutation_chance
        self.mutation_chance.set(options_mutation_chance)
        global options_def_gen
        self.def_gen.set(options_def_gen)
        global options_nbr_idv
        self.nbr_idv.set(options_nbr_idv)
        global options_grid_size
        self.grid_size.set(options_grid_size)
        global options_ship_number
        self.ship_number.set(options_ship_number)

        # Liste d'options
        ttk.Label(root, text="Option de l'algorithme :")\
            .grid(row=0, column=1, columnspan=2)
        ttk.Label(root, text='Nombre de génération')\
            .grid(row=1, column=1)
        ttk.Entry(root, textvariable=self.nbr_gen)\
            .grid(row=1, column=2)
        ttk.Label(root, text='Population conservé (%)')\
            .grid(row=2, column=1)
        ttk.Entry(root, textvariable=self.saved_percentage)\
            .grid(row=2, column=2)
        ttk.Label(root, text='Chance de mutation (%)')\
            .grid(row=3, column=1)
        ttk.Entry(root, textvariable=self.mutation_chance)\
            .grid(row=3, column=2)
        ttk.Label(root, text='Nombre de gène par défault')\
            .grid(row=4, column=1)
        ttk.Entry(root, textvariable=self.def_gen)\
            .grid(row=4, column=2)
        ttk.Label(root, text="Nombre d'individu")\
            .grid(row=5, column=1)
        ttk.Entry(root, textvariable=self.nbr_idv)\
            .grid(row=5, column=2)
        ttk.Label(root, text='Option du jeu :')\
            .grid(row=6, column=1, columnspan=2)
        ttk.Label(root, text='Taille de la grille')\
            .grid(row=7, column=1)
        ttk.Entry(root, textvariable=self.grid_size)\
            .grid(row=7, column=2)
        ttk.Label(root, text='Nombre de navire')\
            .grid(row=8, column=1)
        ttk.Entry(root, textvariable=self.ship_number)\
            .grid(row=8, column=2)
        save_button = ttk.Button(root, text='Sauvegarder',
                                 command=self.save_option)
        save_button.grid(row=9, column=1, columnspan=2)
        back_button = ttk.Button(root, text='Retour',
                                 command=self.return_call)
        back_button.grid(row=10, column=1, columnspan=2)
        root.grid_columnconfigure((0, 3), weight=1)
        root.mainloop()

    def return_call(self):
        """
        Nettoyage des éléments dans la fenêtre et appel l'affichage
            du menu.
        """
        for widget in self.return_app.master.winfo_children():
            widget.destroy()
        self.return_app.home_draw()

    def save_option(self):
        global options_nbr_gen
        global options_saved_percentage
        global options_mutation_chance
        global options_def_gen
        global options_nbr_idv
        global options_grid_size
        global options_ship_number
        options_nbr_gen = self.nbr_gen.get()
        options_saved_percentage = self.saved_percentage.get()
        options_mutation_chance = self.mutation_chance.get()
        options_def_gen = self.def_gen.get()
        options_nbr_idv = self.nbr_idv.get()
        options_grid_size = self.grid_size.get()
        options_ship_number = self.ship_number.get()
        data = {"nbr_gen": options_nbr_gen, "saved_%": options_saved_percentage,
                "mut_%": options_mutation_chance, "def_gen": options_def_gen,
                "nbr_idv": options_nbr_idv,
                "grid_size": options_grid_size, "ship_nbr": options_ship_number}
        with open('../cfg/option.json', 'w') as file:
            json.dump(data, file)
        file.close()


def init_option():
    """
    Initialise les variables globales de paramètres avec les valeurs
    écrites dans cfg/option.json
    """
    with open('..//cfg/option.json', 'r') as file:
        data = json.load(file)
    global options_nbr_gen
    global options_saved_percentage
    global options_mutation_chance
    global options_def_gen
    global options_nbr_idv
    global options_grid_size
    global options_ship_number
    options_nbr_gen = data["nbr_gen"]
    options_saved_percentage = data["saved_%"]
    options_mutation_chance = data["mut_%"]
    options_def_gen = data["def_gen"]
    options_nbr_idv = data["nbr_idv"]
    options_grid_size = data["grid_size"]
    options_ship_number = data["ship_nbr"]
    file.close()
