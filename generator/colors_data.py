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
        self.feet1 = None
        self.feet2 = None
        self.neck = None
        self.neck_2 = None
        self.head = None
        self.chest = None
        self.tail_1 = None
        self.tail_2 = None

        self.decide()
        self.aura = self.random_bck()
        self.bckg = self.random_bck()
        super().__init__()

    def decide(self):
        """
        Decide los colores del MCK.
        """
        if self.chicken_type == ChickenType.HEN:
            self.border = (0, 0, 0)
            self.cuerpo = (249, 249, 249)
            self.eye =    (64, 0, 64)
            self.thingy = (186, 69, 69)
            self.nose =   (255, 174, 201)
            self.wing =   (136, 0, 21)
            self.feet1 =  (255, 127, 39)
            self.feet2 =  (185, 74, 0)
        elif self.chicken_type == ChickenType.COCK:
            self.border = (0, 0, 0)
            self.cuerpo = (141, 10, 16)
            self.eye =    (87, 6, 11)
            self.thingy = (255, 127, 39)
            self.nose =   (255, 242, 0)
            self.wing =   (196, 0, 30)
        elif self.chicken_type == ChickenType.DETAILED_COCK:
            self.border = None
            self.cuerpo = (46, 2,2)
            self.eye = (15,55,62)
            self.thingy = (204,9,12)
            self.neck = (228, 118, 33)
            self.neck_2 = (250, 211, 160)
            self.head = (186, 72, 12)
            self.nose = (213, 138, 28)
            self.wing = (83, 9, 5)
            self.chest = (18, 53, 60)
            self.tail_1 = (121, 156, 169)
            self.tail_2 = (48, 88, 96)
            self.feet1 = (208, 88, 21)
        else:
            print(f"No tenemos un tip de {self.chicken_type} en este momento")
            exit(0)

        # Pon la data
        self.before = [
            self.border,
            self.cuerpo,
            self.eye,
            self.thingy,
            self.neck,
            self.neck_2,
            self.head,
            self.nose,
            self.wing,
            self.chest, 
            self.tail_1,
            self.tail_2,
            self.feet1,
            self.feet2
        ]
        self.after = []

        self.before = list(filter(None, self.before))

        for color in self.before:
            self.after.append(randomifycolor())

    def random_bck(self):
        bckg = randomifycolor()
        # Chequea si el bckg esta en despues
        while bckg in self.after:
            bckg = randomifycolor()

        return bckg