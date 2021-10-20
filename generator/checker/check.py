# Script para chequea que hay un patron en el monster cock
from PIL import Image, ImageDraw
import numpy as np
from generator.attributes.attributes import Attribute
from generator.attributes.gradients import Gradients
from generator.chicken_type import ChickenType
from generator.colors_data import Colors
from generator.utils import conver_to_3
from collections import Counter

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
    # Data para la respuesta
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
    gradients = list(set(gradients or tracker.gradients))

    # Minimo para verificar
    needed = len(gradients) / 1.2

    # Los pixels
    pixels = list(set([conver_to_3(i) for i in image.getdata()]))

    # Queremos contar cuantas veces existe el gradient
    counter = Counter(
        list(
            map(
                lambda p: p in gradients, 
                pixels
            )
        )
    )

    # Para ser True tiene que tener mas de el needed
    return counter[True] >= needed


if __name__ == "__main__":
    image = Image.new('RGB', (1900, 1900))
    drawing = ImageDraw.Draw(image)
    Gradients(image, drawing, Colors(ChickenType.DETAILED_COCK),
              Attribute.GRADIENT_V).draw()
    image.show()
    print(check_for_gradient(image, tracker.gradients))
