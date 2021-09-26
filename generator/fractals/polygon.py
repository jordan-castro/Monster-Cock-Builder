from generator.attributes.canvas import center_image
import math
from PIL import Image, ImageDraw
from generator.fractals.box_size import BoxSize
from generator.utils import make_transparent
import random
from generator.random_data import randomifycolor


def crazy_polygons(box_size:BoxSize=None, amount=1, side=8, fill=None, outline=None)-> Image:
    """
    Function para crear unos polygonos crazy!

    Params:
        - <box_size: BoxSize = None> El sizio de la caja.
        - <amount: int = 1> El amount de polygons.
        - <side: int = 8> Cuantos sides para el polygon.
        - <fill: tuple[int,int,int] = None> El color para el fill.
        - <outlie: tuple[int,int,int] = None> El color del outline.

    Returns: <Image>
    """
    # Function para recursion!
    def draw_polygon(image, box_size, side, fill, outline):
        # Busca el XY. De verdad tengo ni idea como funciona?
        xy = [
            (
                (math.cos(th) + 1) * (box_size.width),
                (math.sin(th) + 1) * (box_size.height)
            )
            for th in [
                i * (2 * math.pi) / side
                for i in range(side)
            ]
        ]

        # Dibuja!
        drawing = ImageDraw.Draw(image) 
        drawing.polygon(xy, fill, outline)

    # El imagen main
    image = Image.new('RGB', (box_size.width, box_size.height))
    # Una lista de los imagenes para hacer paste
    images = []

    size_difference = random.randint(1, 10)
    print(size_difference)

    # Loop sobre la cuenta
    for i in range(amount):
        # EL width y height se hace mas pequeno cada ves
        width = (box_size.width - (i * size_difference))
        height = (box_size.height - (i * size_difference))

        if width <= 0 or height <= 0:
            break

        # El imagen currentamente para poner solor UN polygon
        img = Image.new('RGB', (width, height))
        # Dibuja!!
        draw_polygon(img, BoxSize(int(width / 2), int(height / 2)), side, fill, outline)
        images.append(img)

    # Ahore creamos el main imagen para regresar
    for img in images:
        # Hacemos transparent
        img = make_transparent(img, (0,0,0), False)
        # CENTRO!!
        image = center_image(image, img)

    return image

if __name__ == "__main__":
    # img = Image.new("RGB", (1200,1200))
    image = crazy_polygons(
        BoxSize(width=1200, height=1200),
        amount=random.randint(2, 100),
        side=random.randint(3, 8),
        fill=randomifycolor(),
        outline=randomifycolor()
    )

    # image2 = crazy_polygons(BoxSize(1000, 1000), side=8)

    # # # # image.show()
    # # # image = Image.new("RGB", (1200, 1200))
    # # # image2 = Image.new("RGB", (600,600))

    # # # crazy_polygons(image, 600, 600, side=3)
    # # # crazy_polygons(image2, 300,300, amount=20, side=3)

    # image2 = make_transparent(image2,(0,0,0) ,save=False)
    # image = center_image(image, image2)
    # image.paste(image2, (int((1200 / 2) - (1000 / 2)), int((1200 / 2) - (1000 / 2))), image2)
    image.show()