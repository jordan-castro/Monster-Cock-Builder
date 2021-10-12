### El "Modelo" para el generacion de un MonsterCock
from PIL import Image
from generator.colors_data import Colors, black_list_pallete
import os


class Tracker:
    def __init__(self) -> None:
        self.id: int = None
        self.name: str = None
        self.path: str = None
        self.colors: Colors = None
        self.image: Image = None

    def reset(self):
        """
        Hacemos un Reset al tracker para empezar denuevo!
        """
        self.id = None
        self.name = None
        self.path = None
        self.colors = None
        self.image = None

    def finalize(self):
        """
        Final, todo esta bien!
        """
        # Hacemos black_list
        black_list_name(self.name)
        # for pallete in self.colors.palletes:
        #     black_list_pallete(self.colors.category, pallete)

    def destroy(self):
        """
        Final, todo no esta bien!
        """
        # Borra el imagen
        print(f"Vamos a destruir {self.name} con path {self.path} y id {self.id}")
        os.unlink(self.path)
        self.reset()


# Un object de tracker!!!
tracker = Tracker()