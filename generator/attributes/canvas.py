from generator.attributes.gradients import Gradients
from generator.colors_data import Color, Colors
from generator.attributes.attributes import Attribute
from PIL import Image, ImageDraw
from generator.fractals.fractals import Fractals


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
        # if attribute == Attribute.SUN:
        #     canvas = "sun_canvas"
        #     break
        # else:
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

    x = int((background.size[0] / 2) - (chicken.size[0] / 2))
    y = int((background.size[1] / 2) - (chicken.size[1] / 2))

    ### Chequa los attributes

    # Gradients
    if Attribute.GRADIENT_V in attributes:
        Gradients(new_image, drawing, color_data, Attribute.GRADIENT_V).draw()
    elif Attribute.GRADIENT_H in attributes:
        Gradients(new_image, drawing, color_data, Attribute.GRADIENT_H).draw()

    if Attribute.CRAZY_CIRCLES in attributes:
        Fractals(background, Attribute.CRAZY_CIRCLES).fractilate()
    elif Attribute.CRAZY_POLYGONS in attributes:
        Fractals(background, Attribute.CRAZY_POLYGONS).fractilate()

    # Edita el nuevo imagen
    new_image.paste(background, (0,0))
    new_image.paste(chicken, (x,y), chicken)
    return new_image