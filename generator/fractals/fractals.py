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

    print(attribute)

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