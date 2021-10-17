# Script para chequea que hay un patron en el monster cock
from PIL import Image, ImageDraw
import numpy as np
import random
from generator.attributes.attributes import Attribute
from generator.attributes.gradients import Gradients
from generator.chicken_type import ChickenType
from generator.colors_data import Colors
from generator.utils import conver_to_3

from generator.tracker.tracker import tracker


def is_valid_fractal(image, needed=100) -> bool:
    """
    Chequea que el imagen tiene unos fractals validos.

    Params:
        - <image: Image> El imagen.

    Returns: <bool>
    """
    # Buscamos el width y height
    # Menos cien porque no queremos esa mierda fea en los corners
    width = image.width - 100
    height = image.height - 100
    # El nuevo imagen con crop
    checker = image.crop((100, 100, width, height))
    # Data para el negro
    rows = []

    pixels = np.array(checker)
    for y in pixels:
        x_pixels = list(map(lambda l: tuple(l), y.tolist()))
        rows.append(
            (len(set(x_pixels)) == 1)
        )

    # Ahora chequeamos si los Falsos son mas de needed (10)
    return rows.count(False) > needed


def check_for_gradient(image, gradients: list[tuple[int, int, int]] = None) -> bool:
    """
    Chequea que el imagen tiene gradient o no.

    Params:
        - <image: Image> El imagen para chequear.
        - <gradients: list(tuple(int,int,int))=None> Lista de colores para los gradients.

    Returns: <bool> 
    """
    # Si gradients son None entonces usamos gradients en tracker.tracker
    gradients = gradients or list(set(tracker.gradients))

    # Los tiempos encontrado
    times_found = 0
    # Minimo para verificar
    needed = 20

    # Los pixels
    pixels = [conver_to_3(i) for i in image.getdata()]

    print(gradients)

    # Para cada color chequea si esta en pixels
    for color in gradients:
        if color in pixels:
            times_found += 1
            if times_found >= needed:
                break

    print(times_found)

    return times_found >= needed


if __name__ == "__main__":
    image = Image.new('RGB', (1900, 1900))
    drawing = ImageDraw.Draw(image)
    Gradients(image, drawing, Colors(ChickenType.DETAILED_COCK),
              Attribute.GRADIENT_V).draw()
    image.show()
    print(check_for_gradient(image, tracker.gradients))
