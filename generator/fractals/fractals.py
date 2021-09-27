from generator.fractals.box_size import BoxSize
from generator.fractals.crazy_circles import crazy_circles
from generator.fractals.polygon import crazy_polygons
from generator.colors_data import Colors
from generator.attributes.attributes import Attribute
from generator.random_data import randomifycolor
import random


class Fractals:
    def __init__(self, image, fractal_type: Attribute) -> None:
        self.image = image
        self.type = fractal_type

        self.__fractilate__()
    
    def __fractilate__(self):
        """
        Dibjuo los fractals.
        """
        if self.type == Attribute.CRAZY_POLYGONS:
            self.polygons()
        elif self.type == Attribute.CRAZY_CIRCLES:
            self.circles()
        else:
            return

    def polygons(self):
        """
        Dibuja los polygons.
        """
        fill = randomifycolor() \
            if random.randint(0, 1) % 1 == 0 \
            else None

        outline = randomifycolor() \
            if random.randint(0, 1) % 1 == 0 \
            else None

        self.image = crazy_polygons(
            BoxSize(
                self.image.width, 
                self.image.height
            ),
            amount=random.randint(5, 100),
            side=random.randint(3, 9),
            image=self.image,
            fill=fill, 
            outline=outline
        )

    def circles(self):
        """
        Dibuja los circulos.
        """
        self.image = crazy_circles(
            BoxSize(
                self.image.width,
                self.image.height
            ),
            circle_radius=random.randint(10, 100), 
            amount=random.randint(1, 10), 
            width=random.randint(1, 9),
            image = self.image
        )

        # def crazy_circles(self):
        # """
        # Usamos el Crazy Circles function.
        # """
        # # Crea un nuevo canvas con los crazy circles!
        # image = crazy_circles(
        #     BoxSize(
        #         self.image.width, 
        #         self.image.height
        #     ),
        #     circle_radius=random.randint(10, 100), 
        #     amount=random.randint(1, 10), 
        #     width=random.randint(1, 9),
        #     # image=self.image,
        # )

        # # Toma los pixels del imagen
        # pixels = image.getdata()
        # # Cambia los pixels a colores random
        # new_pixels = replace_pixels(pixels, [randomifycolor(), self.colors.bckg], [(0,0,0), (255,255,255)])
        # # Actualiza
        # image.putdata(new_pixels)
        
        # # Gurda el photo y hacemos transparent
        # self.finish()
        # make_transparent(self.output, self.colors.bckg)

        # self.image = Image.open(self.output)
        # self.image = center_image(image, self.image)

        # #Pon el cock en el canvas
        # image.paste(self.image, (0,0), self.image)
        # self.image = image
