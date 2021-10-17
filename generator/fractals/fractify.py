import random
from generator.fractals.box_size import BoxSize
from PIL import Image


class FractalBuilder:
    def build(self, box_size: BoxSize, method, radius:int=100, width:int=1, image=None, fill=None, outline=None, size:int=100)-> Image:
        """
        Function para generar los fractals.

        Params:
            - <box_size: BoxSize> El size del box.
            - <method: Methos> El method de generar fractals.
            - <radius: int = 100> El radius, no siempre se usa.
            - <amount: int = 5> Cuantos vecez dibujamos?
            - <minimum: int = 0> El mimimum que podemos tener.
            - <width: int = 0> El size del imagen, no siempro se usa.
            - <image: Image = None> Si quieres usar un imagen que ya existe.
            - <fill = None> Un color.
            - <outline = None> Un color.
            - <size: int=100> El size del vaina
        
        Returns: <Image>
        """
        self.image = image or Image.new('RGB', (box_size.width, box_size.height))
        self.box_size = box_size
        self.method = method
        self.radius = radius
        self.width = width
        self.fill = fill
        self.outline = outline
        self.size = size

        mod = random.randint(1, 6)
        choose_one = random.randint(1, 3)

        if choose_one == 1:
            self.usual(mod)
        elif choose_one == 2:
            self.alot(mod)
        elif choose_one == 3:
            self.random_mod(mod)

        return self.image

    def usual(self, mod):
        for y in range(self.box_size.height):
            if y % mod == 0:
                ycon = y % 20 != 0 or y % 15 != 0
            else:
                ycon = y % 20 != 0 and y % 15 != 0

            if ycon:
                continue
            for x in range(self.box_size.width):
                if x % mod == 0:
                    xcon = x % 20 != 0 or x % 15 != 0
                else:
                    xcon = x % 20 != 0 and x % 15 != 0

                if xcon:
                    continue
                self.method(
                    image=self.image,
                    x1=x,
                    y1=y,
                    x2=x + self.size,
                    y2=y + self.size,
                    amount=1,
                    minimum=0,
                    fill=self.fill,
                    outline=self.outline,
                    width=self.width,
                    radius=self.radius
                )

    def alot(self, mod):
        amount = random.randint(1, 10)

        for i in range(amount):
            mod = random.randint(1, 6)

            for y in range(self.box_size.height):
                if y % mod == 0:
                    ycon = y % 20 != 0 or y % 15 != 0
                else:
                    ycon = y % 20 != 0 and y % 15 != 0

                if ycon:
                    continue
                for x in range(self.box_size.width):
                    if x % mod == 0:
                        xcon = x % 20 != 0 or x % 15 != 0
                    else:
                        xcon = x % 20 != 0 and x % 15 != 0
                    
                    if xcon:
                        continue
                    self.method(
                        image=self.image,
                        x1=x - i * mod,
                        y1=y - i * mod,
                        x2=x + self.size - i * mod,
                        y2=y + self.size - i * mod,
                        amount=1,
                        minimum=0,
                        fill=self.fill,
                        outline=self.outline,
                        width=self.width,
                        radius=self.radius
                    )

    def random_mod(self, mod):
        mods = []
        for i in range(4):
            mods.append(random.randint(10, 20))

        for x in range(self.box_size.width):
            if x % mod == 0:
                xcon = x % mods[0] != 0 or x % mods[1] != 0
            else:
                xcon = x % mods[0] != 0 and x % mods[1] != 0

            if xcon:
                continue

            for y in range(self.box_size.height):
                if y % mod == 0:
                    ycon = y % mods[2] != 0 or y % mods[3] != 0
                else:
                    ycon = y % mods[2] != 0 and y % mods[3] != 0
                
                if ycon:
                    continue
                self.method(
                    image=self.image,
                    x1=x,
                    y1=y,
                    x2=x + self.size,
                    y2=y + self.size,
                    amount=1,
                    minimum=0,
                    fill=self.fill,
                    outline=self.outline,
                    width=self.width,
                    radius=self.radius
                )