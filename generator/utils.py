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


def make_transparent(source, color=None, save=True):
    """
    Hacemos un photo tener transperencia!

    Params:
        - <source: str | Image> El imagen para hacer transparent.
        - <color: tuple[int,int,int] = None> El color para hacer transparent.
        - <sve: bool = True> Deberiamos guardar?
    """
    img = Image.open(source) if type(source) is str else source
    img = img.convert('RGBA')

    pixels = img.getdata()

    color = color or (255,255,255)

    new_pixels = replace_pixels(pixels, [(0,0,0,0)], [color])

    # new_pixels = list(map(lambda p: is_color(p), pixels))

    img.putdata(new_pixels)
    if save:
        img.save(source, "PNG")
    else:
        return img


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
    def is_color(pixel):
        p = conver_to_3(pixel)
        if p in color_find:
            return color_replace[color_find.index(p)]
        else:
            return pixel

    npixels = list(map(lambda p: is_color(p), pixels))

    # for pixel in pixels:
    #     # Cambia a (R,G,B)
    #     p = conver_to_3(pixel)
    #     if p in color_find:
    #         p = color_replace[color_find.index(p)]
    #     # Ponemos pxel
    #     npixels.append(p)
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


def center_image(canvas, center)-> Image:
    """
    Ponemos un imagen `center` en el centro del `canvas`.

    Params:
        - <canvas: Image> El imagen del canvas
        - <center: Image> El imagen para poner en el centro.

    Returns: <Image>
    """
    x = int((canvas.size[0] / 2) - (center.size[0] / 2))
    y = int((canvas.size[1] / 2) - (center.size[1] / 2))
    canvas.paste(center, (x,y), center)
    return canvas


if __name__ == "__main__":
    # data = Colors(ChickenType.HEN)
    # for d in data.after:
    #     print(d)
    #     print(rgb_to_name(d))
    #     print()
    # print(rgb_to_name(data))
    # make_transparent('base_art/detailed_cock.png')
    change_size("base_art/FinalCockHR.png", (379, 415))
