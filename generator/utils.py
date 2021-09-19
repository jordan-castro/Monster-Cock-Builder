from generator.chicken_type import ChickenType
from generator.colors_data import Colors
from generator.attributes.attributes import Attribute
from generator.random_data import randomifycolor
from PIL import Image, ImageDraw
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


def create_image(source, canvas, attributes: list, color_data: Colors):
    """
    Crea el imagen del monstercock para editar.

    Params:
        - <source: str> El archivo de monster cock | Sexy Hen.
        - <canvas: str> El archivo detras del monstercock | Sexy Hen.
        - <type: ChickenType> El tipo de pollo.
        - <attributes: list> El attribute que tiene este pollo.
        - <color_data: Colors> La data de colors. 

    Return: <Image> 
    """
    # El detras
    background = Image.open(canvas)
    # Un drawing para el canvas!
    drawing = ImageDraw.Draw(background)
    # El pollo
    chicken = Image.open(source)
    
    # El nuevo imagen
    new_image = Image.new('RGBA', background.size, (255,255,255))

    x = int((background.size[0] / 2) - (chicken.size[0] / 2))
    y = int((background.size[1] / 2) - (chicken.size[1] / 2))
    
    # Chequa el attribute
    if Attribute.AURA in attributes:
        x1 = x - 50
        y1 = y - 50
        x2 = x + chicken.size[0] + 50
        y2 = y + chicken.size[1] + 50
        color = color_data.aura
        drawing.ellipse((x1, y1, x2, y2), fill=color, outline=color)

    # Edita el nuevo imagen
    new_image.paste(background, (0,0))
    new_image.paste(chicken, (x,y), chicken)
    return new_image


def make_transparent(source):
    """
    Hacemos un photo tener transperencia!
    """
    img = Image.open(source)
    img = img.convert('RGBA')

    pixels = img.getdata()
    new_pixels = []

    for pixel in pixels:
        if pixel[0] == 255 and pixel[1] == 255 and pixel[2] == 255:
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


if __name__ == "__main__":
    data = Colors(ChickenType.HEN)
    for d in data.after:
        print(d)
        print(rgb_to_name(d))
        print()
    # print(rgb_to_name(data))
    # make_transparent('base_art/sun.png')
