from generator.chicken_type import ChickenType
from PIL import Image
import glob
import os
import webcolors


def clear(chicken_type: ChickenType):
    """
    Hacemos clear a los files.
    """
    if chicken_type ==ChickenType.COCK:
        black = 'cock_base.png'
        find = 'cock'
    elif chicken_type == ChickenType.HEN:
        black = 'hen_base.png'
        find = 'hen'

    # Busca todos
    files = glob.glob('*png')
    # Loop
    for file in files:
        if find in file.lower():
            if file != black:
                os.unlink(file)


def make_transparent(source, color=None):
    """
    Hacemos un photo tener transperencia!
    """
    img = Image.open(source)
    img = img.convert('RGBA')

    pixels = img.getdata()
    new_pixels = []

    color = color or (255,255,255)

    for pixel in pixels:
        if pixel[0] == color[0] and pixel[1] == color[1] and pixel[2] == color[2]:
            new_pixels.append((pixel[0], pixel[1], pixel[2], 0))
        else:
            new_pixels.append(pixel)

    img.putdata(new_pixels)
    img.save(source, "PNG")


def conver_to_3(pixel):
    """
    Converte un tupple de 4 a un tupple de 3

    Returns: <tupple>
    """
    return (pixel[0], pixel[1], pixel[2])


def current_amount():
    """
    Los cocks currentamente.

    Returns: <list>
    """
    files = glob.glob('*.png')

    return files


def rgb_to_name(rgb: tuple[int, int, int]):
    """
    Converte un color de RGB a un Nombre!

    Params:
        - <rgb: tuple[int,int,int]> EL color para convertir.
    
    Returns: <str> 
    """
    # Los colores minimum
    min_colors = {}
    # Loop sobre todos los colores que hay!
    for key, name in webcolors.CSS3_HEX_TO_NAMES.items():
        # Busca en rgb
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        # Math para calcular
        rd = (r_c - rgb[0]) ** 2
        gd = (g_c - rgb[1]) ** 2
        bd = (b_c - rgb[2]) ** 2
        # Los negros
        min_colors[(rd + gd + bd)] = name
    # Regrese el minumum de los keys!
    return min_colors[min(min_colors.keys())]


def ipfs_url(ipfs_hash):
    """
    Regresa un URL con el ipfs hash.

    Params:
        - <ipfs_hash: str> EL hash del archivo ipfs.

    Returns: <str>
    """
    return f'https://ipfs.io/ipfs/{ipfs_hash}'


def replace_pixels(pixels, color_replace: list, color_find: list):
    """
    Cambiamos los pixels a un color especificado.

    Params:
        - <pixels: list[tuple[int,int,int]]> Los pixels
        - <color_replace: list[tuple[int,int,int]]> los colores en RGB que queremos poner.
        - <color_find: list[tuple[int,int,int]]> los colores en RGB que queremos cambiar.

    IMPORTANT:
        - color_replace y color_find debe tener los colores en el mismo index.

    Returns: <list[tuple[int,int,int]]>
    """
    # Los nuevo pixels
    npixels = []
    for pixel in pixels:
        # Cambia a (R,G,B)
        p = conver_to_3(pixel)
        if p in color_find:
            p = color_replace[color_find.index(p)]
        # Ponemos pxel
        npixels.append(p)
    return npixels


def change_size(source, size):
    """
    Cambia el size del imagen.

    Params:
        - <source: str> El imagen para cambiar
        - <size: tuple[int,int]> El size (width, height)
    """
    image = Image.open(source)
    image = image.resize(size, Image.ANTIALIAS)

    image.save(source)


def darken_color(color):
    dark = (
        int(color[0] * 1.2),
        int(color[1] * 1.2),
        int(color[2] * 1.2)
    )

    # Para saber si es negro
    black = (0,0,0)

    # Si los dos son negro entonces regresa blano
    if dark == black and color == black:
        return (255,255,255)

    # Si no? regresa dark
    return dark


if __name__ == "__main__":
    # data = Colors(ChickenType.HEN)
    # for d in data.after:
    #     print(d)
    #     print(rgb_to_name(d))
    #     print()
    # print(rgb_to_name(data))
    # make_transparent('base_art/detailed_cock.png')
    change_size("base_art/FinalCockHR.png", (379, 415))
