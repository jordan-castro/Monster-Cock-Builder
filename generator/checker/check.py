### Script para chequea que hay un patron en el monster cock
from PIL import Image
import numpy as np


def is_valid_fractal(image)-> bool:
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
    checker = image.crop((100,100, width, height))
    # Data para el negro
    needed = 100
    rows = []

    pixels = np.array(checker)
    for y in pixels:
        x_pixels = list(map(lambda l: tuple(l), y.tolist()))
        rows.append(
            (len(set(x_pixels)) == 1)
        )

    # Ahora chequeamos si los Falsos son mas de needed (10)
    return rows.count(False) > needed

if __name__ == "__main__":
    image = Image.open('test.png')
    print(is_valid_fractal(image))