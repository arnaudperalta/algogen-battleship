import json
from algogen_graphic import App
from algogen_core import Core
import options as o


def main():
    """
    Fonction main du programme
    On initialise ici :
        - la configuration du programme
        - une instance de la classe Core
        - une instance de la classe App
        - la construction de l'interface graphique
    """
    # Enregistrement des options en mémoire
    o.init_option()
    # Instanciation du modèle
    model = Core()

    # Instanciation de l'interface utilisateur
    app = App(model)
    # Construction de l'interface graphique
    app.build()


if __name__ == '__main__':
    main()
