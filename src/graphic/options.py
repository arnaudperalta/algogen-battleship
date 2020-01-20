import json
from tkinter import ttk
from tkinter import IntVar


class Options(ttk.Frame):
    def __init__(self, master=None, app=None):
        with open('./cfg/option.json', 'r') as file:
            data = json.load(file)
        super().__init__(master)
        self.return_app = app
        self.nbr_gen = IntVar()
        self.nbr_gen.set(data["nbr_gen"])
        self.saved_percentage = IntVar()
        self.saved_percentage.set(data["saved_%"])
        self.mutation_chance = IntVar()
        self.mutation_chance.set(data["mut_%"])
        self.grid_size = IntVar()
        self.grid_size.set(data["grid_size"])
        self.ship_number = IntVar()
        self.ship_number.set(data["ship_nbr"])
        file.close()

    def build(self):
        root = self.master
        # Liste d'options
        ttk.Label(root, text="Option de l'algorithme :").grid(row=0, column=1, columnspan=2)
        ttk.Label(root, text='Nombre de génération').grid(row=1, column=1)
        ttk.Entry(root, textvariable=self.nbr_gen).grid(row=1, column=2)
        ttk.Label(root, text='Population conservé (%)').grid(row=2, column=1)
        ttk.Entry(root, textvariable=self.saved_percentage).grid(row=2, column=2)
        ttk.Label(root, text='Chance de mutation (%)').grid(row=3, column=1)
        ttk.Entry(root, textvariable=self.mutation_chance).grid(row=3, column=2)
        ttk.Label(root, text='Option du jeu :').grid(row=4, column=1, columnspan=2)
        ttk.Label(root, text='Taille de la grille').grid(row=5, column=1)
        ttk.Entry(root, textvariable=self.grid_size).grid(row=5, column=2)
        ttk.Label(root, text='Nombre de navire').grid(row=6, column=1)
        ttk.Entry(root, textvariable=self.ship_number).grid(row=6, column=2)
        save_button = ttk.Button(root, text='Sauvegarder', command=self.save_option)
        save_button.grid(row=7, column=1, columnspan=2)
        back_button = ttk.Button(root, text='Retour', command=self.return_call)
        back_button.grid(row=8, column=1, columnspan=2)
        root.grid_columnconfigure((0, 3), weight=1)
        # fin de liste
        root.mainloop()

    def save_option(self):
        data = {"nbr_gen": self.nbr_gen.get(), "saved_%": self.saved_percentage.get(),
                "mut_%": self.mutation_chance.get(), "grid_size": self.grid_size.get(),
                "ship_nbr": self.ship_number.get()}
        print(data)
        with open('./cfg/option.json', 'w') as file:
            json.dump(data, file)
        file.close()

    def return_call(self):
        for widget in self.return_app.master.winfo_children():
            widget.destroy()
        self.return_app.home_draw()