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
    needed = 10
    rows = []

    pixels = np.array(checker)
    for y in pixels:
        x_pixels = list(map(lambda l: tuple(l), y.tolist()))
        rows.append(
            (len(set(x_pixels)) == 1)
        )

    # replace = color_replace[color_find.index(color)]
    # red, green, blue = data[:,:,0], data[:,:,1], data[:,:,2]
    # mask = (red == color[0]) & (green == color[1]) & (blue == color[2])
    # data[:,:,:3][mask] = [replace[0], replace[1], replace[2]] 


    # for y in range(checker.height):
    #     # Un array para tomar todos los pixels en el X
    #     x_pixels = []
    #     for x in range(checker.width):
    #         # Buscamos el pixel
    #         pixel = checker.getpixel((y,x))
    #         # Ponemos el pixel 
    #         x_pixels.append(pixel)
        
    #     # Chequea que todo en x_pixels es igual
    #     rows.append(
    #         (len(set(x_pixels)) == 1)
    #     )


    # print(rows)

    # Ahora chequeamos si los Falsos son mas de needed (10)
    return rows.count(False) > needed

if __name__ == "__main__":
    image = Image.open('test.png')
    print(is_valid_fractal(image))