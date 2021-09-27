from generator.utils import conver_to_3
from generator.fractals.box_size import BoxSize
from generator.fractals.crazy_circles import crazy_circles
from generator.colors_data import Colors
from generator.attributes.attributes import Attribute
from generator.random_data import randomifycolor
import random


class Fractals:
    def __init__(self, image, fractal_type: Attribute) -> None:
        self.image = image
        self.type = fractal_type

    def fractilate(self):
        """
        Dibjuo los fractals.
        """
        if self.type == Attribute.CRAZY_CIRCLES:
            self.circles()
        else:
            return

        return self.image

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
            image = self.image,
            outline=randomifycolor()
        )
        