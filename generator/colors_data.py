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
        
        self.decide()
        self.aura = self.random_bck()
        self.bckg = self.random_bck()
        super().__init__()

    def decide(self):
        """
        Decide los colores del MCK.
        """
        if self.chicken_type == ChickenType.HEN:
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
        self.before = [border, cuerpo, eye, thingy, nose, wing]
        self.after = []

        # Chequea para feet
        if self.feet:
            for f in self.feet:
                self.before.append(f)

        for color in self.before:
            self.after.append(randomifycolor())

    def random_bck(self):
        bckg = randomifycolor()
        # Chequea si el bckg esta en despues
        while bckg in self.after:
            bckg = randomifycolor()

        return bckg