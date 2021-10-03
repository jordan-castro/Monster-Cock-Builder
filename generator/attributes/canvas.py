from generator.attributes.gradients import Gradients
from generator.colors_data import Colors
from generator.attributes.attributes import Attribute
from PIL import Image, ImageDraw
from generator.fractals.fractals import draw_fractal
from generator.utils import center_image


def get_canvas(attributes: list):
    """
    Busca un canvas!!

    Params: 
        - <attributes: list> Lista de attributos.

    Returns: <str>
    """
    base = "base_art/"
    canvas = "canvas_large"
    
    # Loop
    for attribute in attributes:
        pass

    return f"{base}{canvas}.png"


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

    ### Chequa los attributes

    # Gradients
    if Attribute.GRADIENT_V in attributes:
        Gradients(new_image, drawing, color_data, Attribute.GRADIENT_V).draw()
    elif Attribute.GRADIENT_H in attributes:
        Gradients(new_image, drawing, color_data, Attribute.GRADIENT_H).draw()

    if Attribute.CRAZY_CIRCLES in attributes:
        background = draw_fractal(background, Attribute.CRAZY_CIRCLES)
    if Attribute.SQUARES in attributes:
        background = draw_fractal(background, Attribute.SQUARES)
    if Attribute.ROUND_SQUARES in attributes:
        background = draw_fractal(background, Attribute.ROUND_SQUARES)
    if Attribute.STRIPES in attributes:
        background = draw_fractal(background, Attribute.STRIPES)

    # Edita el nuevo imagen
    new_image.paste(background, (0,0))
    new_image = new_image.crop((100,100,new_image.width, new_image.height))

    new_image = center_image(new_image, chicken)
    return new_image