from generator.utils import darken_color, rgb_to_name
from generator.chicken_type import ChickenType
from generator.random_data import randomifycolor


class Color(object):
    def __init__(self, before, after=None, title=None, value=None) -> None:
        self.before = before
        self.after = after
        self.title = title
        self.value = value

        super().__init__()


class Colors(object):
    def __init__(self, chicken_type: ChickenType) -> None:
        self.chicken_type = chicken_type
        self.colors: list[Color] = []

        self.decide()
        self.aura = self.random_bck()
        self.bckg = self.random_bck()
        super().__init__()

    def decide(self):
        """
        Decide los colores del MCK.
        """
        if self.chicken_type == ChickenType.DETAILED_COCK:
            self.colors.append(Color((148, 31, 61), title='Comb')) # El comb
            self.colors.append(Color((180, 63, 61), title='Comb')) # COMB
            self.colors.append(Color((213, 97, 53), title='Nose')) # NARIZ 
            self.colors.append(Color((237, 129, 53), title='Nose')) # NARIZ
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
            if color.title == "Eye":
                color.after = darken_color(self.random_bck())
            else:
                color.after = self.random_bck()
            color.value = rgb_to_name(color.after)

    def random_bck(self):
        bckg = randomifycolor()
        
        # Los colores de self.after
        colors = list(map(lambda c: c.after, self.colors))
        
        # Chequea si el bckg esta en despues
        while bckg in colors:
            bckg = randomifycolor()

        return bckg