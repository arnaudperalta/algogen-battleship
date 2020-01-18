import graphic.algogen_graphic as graphic
import core.algogen_core as core


def main():
    # Instanciation du modèle
    model = core.Game()

    # Instanciation de l'interface utilisateur
    app = graphic.App(model)
    app.build()


if __name__ == '__main__':
    main()
