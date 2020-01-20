from tkinter import ttk

class Options(ttk.Frame):
    def __init__(self, master=None, app=None):
        super().__init__(master)
        self.return_app = app

    def build(self):
        root = self.master
        # Liste d'options
        ttk.Label(root, text="Option de l'algorithme :").grid(row=0, column=0, columnspan=2)
        ttk.Label(root, text='Nombre de génération').grid(row=1, column=0)
        nbr_gen = ttk.Entry(root)
        nbr_gen.grid(row=1, column=1)
        ttk.Label(root, text='Population conservé (%)').grid(row=2, column=0)
        saved_percentage = ttk.Entry(root)
        saved_percentage.grid(row=2, column=1)
        ttk.Label(root, text='Chance de mutation (%)').grid(row=3, column=0)
        mutation_chance = ttk.Entry(root)
        mutation_chance.grid(row=3, column=1)
        ttk.Label(root, text='Option du jeu :').grid(row=4, column=0, columnspan=2)
        ttk.Label(root, text='Taille de la grille').grid(row=5, column=0)
        grid_size = ttk.Entry(root)
        grid_size.grid(row=5, column=1)
        ttk.Label(root, text='Nombre de navire').grid(row=6, column=0)
        ship_number = ttk.Entry(root)
        ship_number.grid(row=6, column=1)
        save_button = ttk.Button(root, text='Sauvegarder', command=self.save_option)
        save_button.grid(row=7, column=0, columnspan=2)
        back_button = ttk.Button(root, text='Retour', command=self.return_call)
        back_button.grid(row=8, column=0, columnspan=2)
        # fin de liste
        root.mainloop()

    def save_option(self):
        root = self.master
        root.destroy()

    def return_call(self):
        for widget in self.return_app.master.winfo_children():
            widget.destroy()
        self.return_app.home_draw()
