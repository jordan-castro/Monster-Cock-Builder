import random
from generator.uploader.hidden_globals import PALLETE_LOCATION
from generator.utils import darken_color, rgb_to_name
from generator.chicken_type import ChickenType
from generator.random_data import randomifycolor
import json


def black_list_pallete(category, pallete_index):
    """
    Black list a pallete based on su categoria y index.

    Params:
        - <category: str> El nombre de la categoria.
        - <pallete_index: int> El index del pallete.
    """
    # Busca la data
    data = None
    with open("black_palletes.json", 'r') as file:
        data = file.read()
    # Los palletes en {} format
    palletes = json.loads(data) if data else {}
    # Chequea si la llave existe
    if category in list(palletes.keys()):
        # Pon lo!!!
        palletes[category].append(pallete_index)
    else:
        # Entonces crealo
        palletes[category] = [pallete_index]
    # Escribe lo!
    with open("black_palletes.json", 'w') as file:
        json.dump(palletes, file)


def pallete_black_list(category):
    """
    Regresa el blacklist del pallete. Por su categoria.

    Params: 
        - <category: str> La categoria.

    Returns: <list> 
    """
    with open("black_palletes.json", 'r') as file:
        data = file.read()
        palletes = json.loads(data) if data else {}
        # Ahora buscamos si 'category' existe
        if category in list(palletes.keys()):
            # La lista
            return palletes[category]
        else:
            # Nada negro
            return []


class Color(object):
    def __init__(self, before, after=None, title=None, value=None) -> None:
        self.before = before
        self.after = after
        self.title = title
        self.value = value
        super().__init__()


class Colors(object):
    def __init__(self, chicken_type: ChickenType, category: str=None) -> None:
        self.chicken_type = chicken_type
        self.colors: list[Color] = []
        self.category = category
        self.current_pallete = None
        self.palletes = []
        self.colors_used = []

        self.decide()
        self.aura = self.random_bck()
        self.bckg = self.random_color()
        super().__init__()

    def decide(self):
        """
        Decide los colores del MCK.
        """
        if self.chicken_type == ChickenType.DETAILED_COCK:
            self.colors.append(Color((148, 31, 61), title='Comb')) # El comb
            self.colors.append(Color((180, 63, 61), title='Comb')) # COMB
            self.colors.append(Color((213, 97, 53), title='Beak')) # NARIZ 
            self.colors.append(Color((237, 129, 53), title='Beak')) # NARIZ
            self.colors.append(Color((109, 12, 39), title='Comb')) # El comb por el nariz
            self.colors.append(Color((247, 247, 239), title='Eye')) # OJO
            self.colors.append(Color((213, 97, 53), title='Neck')) # EL NECK primero
            self.colors.append(Color((237, 129, 53), title='Neck')) # El neck siguiente
            self.colors.append(Color((239, 159, 88), title='Back')) # Mucho del cuerpo
            self.colors.append(Color((24, 16, 56), title='Chest')) # El chest negro
            self.colors.append(Color((39, 37, 95), title='Chest')) # El parte del chest
            self.colors.append(Color((56, 64, 116), title='Wing')) # Un parte del wing
            self.colors.append(Color((88, 89, 77), title='Wing')) # Un parte abajo del wing
            self.colors.append(Color((120, 124, 120), title='Wing')) # Otro parte abajo del wing
            self.colors.append(Color((150, 129, 110), title='Leg')) # Leg primero
            self.colors.append(Color((126, 105, 102), title='Leg')) # Leg primero border
            self.colors.append(Color((102, 81, 86), title='Leg')) # Leg siguiente

        for color in self.colors:
            color.after = self.random_color()
            color.value = rgb_to_name(color.after)

    def random_color(self, save=True):
        """
        Buscamos unos palletes random.

        Params:
            - <save: bool = True> Guardar la vaina?
        """
        # Busca de los palletes.json
        with open(PALLETE_LOCATION, 'r') as p_file:
            data = json.load(p_file)

            # Chequea que no hay una categoria
            if not self.category:
                # Busca los keys
                keys = list(data.keys())
                # Para recordar los tiempos que hacemos loop
                times_looped = 0
                while 1:
                    times_looped += 1
                    # Un random
                    index = random.randint(0, len(keys) - 1)
                    self.category = keys[index]
                    # Chequea si ya hemos usado este categoria completamente ya!
                    already_used = pallete_black_list(self.category)
                    if len(already_used) == len(data[self.category]):
                        print(f"Ya hemos usado todos los colores de categoria {self.category}. Debes poner mas.")
                        # Chequea si ya hemos tocado a todos los llaves!
                        if times_looped == len(keys):
                            self.category = None
                            return self.random_color()
                    else:
                        break

            # Chequea si ya hemos usado todo (4 colores hex) de un pallete
            if len(self.colors_used) % 4:
                self.current_pallete = None

            # Si no hay un pallete
            if not self.current_pallete:
                # El index del pallete
                while 1:
                    pallete_index = random.randint(0, len(data[self.category]) - 1)
                    pallete = data[self.category][str(pallete_index)]
                    # Chequea que es un nuevo pallete
                    already_used = pallete_black_list(self.category)
                    # Chequea si ya hemos usado el pallete
                    if not pallete in self.palletes and not pallete_index in already_used:
                        if save:
                            self.palletes.append(pallete)
                        self.current_pallete = pallete
                        # # Black list
                        # black_list_pallete(self.category, pallete_index)
                        break
            else:
                # El pallete es el current_pallete
                pallete = self.current_pallete

            for i in range(4):
                index = random.randint(0, len(pallete) - 1)
                h_color = pallete[index]
                # Converte a RGB
                rgb_color = tuple(int(h_color[i:i+2], 16) for i in (0, 2, 4))
                # Chequea que es nuevo colore
                if not rgb_color in self.current_colors and not rgb_color in self.colors_used:
                    self.colors_used.append(rgb_color)
                    return rgb_color
            # Si toquemos aqui queremos repetir todo el processo!
            return self.random_color()

    @property
    def current_colors(self):
        """
        Busca los colores currentamente.

        Returns: <list>
        """
        return list(map(lambda c: c.after, self.colors))

    def random_bck(self):
        bckg = randomifycolor()
        
        # Los colores de self.after
        colors = self.current_colors
        
        # Chequea si el bckg esta en despues
        while bckg in colors:
            bckg = randomifycolor()

        return bckg