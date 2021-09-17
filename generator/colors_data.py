from generator.chicken_type import ChickenType
from generator.random_data import randomifycolor


class Colors(object):
    def __init__(self, chicken_type: ChickenType) -> None:
        self.chicken_type = chicken_type
        self.before = []
        self.after = []
        self.border = None
        self.cuerpo = None
        self.eye = None
        self.thingy = None
        self.nose = None
        self.wing = None
        self.feet = None
        super().__init__()

    def decide(self):
        """
        Decide los colores del MCK.
        """
        if self.chicken_type == ChickenType.CHICK:
            border = (0, 0, 0)
            cuerpo = (249, 249, 249)
            eye =    (64, 0, 64)
            thingy = (186, 69, 69)
            nose =   (255, 174, 201)
            wing =   (136, 0, 21)
            feet1 =  (255, 127, 39)
            feet2 =  (185, 74, 0)
            feet =   [feet1, feet2]

        elif self.chicken_type == ChickenType.COCK:
            border = (0, 0, 0)
            cuerpo = (141, 10, 16)
            eye =    (87, 6, 11)
            thingy = (255, 127, 39)
            nose =   (255, 242, 0)
            wing =   (196, 0, 30)
            feet =   []
        else:
            print(f"No tenemos un tip de {self.chicken_type} en este momento")
            exit(0)

        # Pon la data
        self.border = border
        self.cuerpo = cuerpo
        self.eye = eye
        self.thingy = thingy
        self.nose = nose
        self.wing = wing
        self.feet = feet

        # Popula los negros!
        self.before = [border, cuerpo, eye, thingy, nose, wing, feet]
        self.after = []
        for color in self.before:
            self.after.append(randomifycolor)

    def random_bck(self):
        """
        Tira un random background para el negro
        """
        bckg = randomifycolor()
        # Chequea que no esta en cualquier

# class Colors:
#     def __init__(self, chicken_type: ChickenType, ignore=[]):
#         self.decide(chicken_type, ignore)

#     def decide(self, type, ignore=[]):
#         """
#         Decide los colores para el photo.
#         """
#         if type == ChickenType.HEN:
#             # Colores para hen
#             self.before = [(0,0,0), (249, 249, 249), (64, 0, 64), (186, 69, 69),  (255, 174, 201), (136, 0, 21), (255, 127, 39), (185, 74, 0)]
#             # ODER        border,   cuerpo,          eye,         thingy          nariz            wing          feet1           feet2

#         elif type == ChickenType.COCK:
#             # Colores para Cock
#             self.before = [(0,0,0), (141, 10, 16), (87, 6, 11), (255, 127, 39), (255, 242, 0), (196, 0, 30)]

#         # Chequea por ignore
#         for color in ignore:
#             if color in self.before:
#                 # Saca lo!
#                 del self.before[color]

#         self.after = []
#         # Ponemos los colores!!!
#         for color in self.before:
#             self.after.append(randomifycolor())

#     def random_bck(self):
#         bckg = randomifycolor()
#         # Chequea si el bckg esta en despues
#         while bckg in self.after:
#             bckg = randomifycolor()

#         return bckg
