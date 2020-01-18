from tkinter import ttk


def home_build(root):
    train_button = ttk.Button(root, text='Entraîner IA Génétique', command=root.quit)
    train_button.pack()
    play_button = ttk.Button(root, text='Jouer vs IA Génétique', command=root.quit)
    play_button.pack()
    ia_button = ttk.Button(root, text='IA vs IA', command=root.quit)
    ia_button.pack()
    options_button = ttk.Button(root, text='Options', command=root.quit)
    options_button.pack()
    quit_button = ttk.Button(root, text='Quitter', command=root.quit)
    quit_button.pack()
    root.mainloop()
