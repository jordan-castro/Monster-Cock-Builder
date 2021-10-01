from generator.checker.check import is_valid_fractal
from generator.fractals.stripes import draw_stripes
from generator.fractals.squares import draw_round_squares, draw_squares
from PIL import Image
from generator.fractals.fractify import FractalBuilder
from generator.fractals.box_size import BoxSize
from generator.fractals.crazy_circles import draw_circles
from generator.attributes.attributes import Attribute
from generator.random_data import randomifycolor
import random


def draw_fractal(image, attribute: Attribute)-> Image:
    """
    Dibuja un fractal.

    Params:
        - <image: Image> El imagen para dibujar por.
        - <attribute: Attribute> El attribute del fractal.

    Returns: <Image>
    """
    start = True
    while not is_valid_fractal(image) or start:
        if start == False:
            print("INVALIDO !!")
        start = False

        radius = random.randint(1, 15)
        size = random.randint(10, 100)
        amount = random.randint(1, 10)
        width = random.randint(1, 9)

        if attribute == Attribute.CRAZY_CIRCLES:
            method = draw_circles
        elif attribute == Attribute.SQUARES:
            method = draw_squares
        elif attribute == Attribute.ROUND_SQUARES:
            method = draw_round_squares
        elif attribute == Attribute.STRIPES:
            method = draw_stripes

        image = FractalBuilder().build(
            BoxSize(
                image.width, 
                image.height
            ),
            method, 
            radius=radius,
            width=width,
            image=image,
            outline=randomifycolor(),
            size=size
        )

    return image


if __name__ == "__main__":
    i = draw_fractal(Image.new('RGB', (1200,1200), 'white'), Attribute.CRAZY_CIRCLES)
    i.show()
    save = input("Guarda imagen? (y/n) ")
    if save == "y" or save == "Y" or save == "Yes" or save == "yes":
        i.save('test.png')
    else:
        print("Palabra")
