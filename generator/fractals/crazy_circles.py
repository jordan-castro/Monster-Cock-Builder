from generator.utils import conver_to_3
import random
from generator.fractals.box_size import BoxSize
from PIL import Image, ImageDraw


def crazy_circles(box_size: BoxSize, circle_radius=100, amount=5, minimum=0, width=1, image=None)-> Image:
    """
    Function para dibujar fractals de circulos.

    Params:
        - <box_size: BoxSize> El box de la negro
        - <anount: int = 5> Ceuntos circulos deberiamos dibjuar?
    """
    box_size = BoxSize(width=image.width, height=image.height) if image else box_size

    # Abre un nuevo imagen
    image = image or Image.new('RGB', (box_size.width, box_size.height))

    if amount <= minimum:
        amount += 10

    # Dibuja los circulos
    def draw_circles(image, x1, y1, x2, y2, amount):
        # Si el amount es 0 ya termina pues
        if amount < minimum:
            return

        # Dibuja el circulo       
        drawing = ImageDraw.Draw(image)
        drawing.ellipse(
            (x1, y1, x2, y2),
            width=width,
        )

        # Crea los coordinatos siguientes
        x1 += random.randint(x1, x1+ 200)
        x2 -= random.randint(x1, x1 + 200)
        y1 += random.randint(y1, y1 + 200)
        y2 -= random.randint(y1, y1 + 200)
        # Recursion!!
        draw_circles(image, x1, y1, x2, y2, amount - 1)

    mod = random.randint(1, 6)

    # Para tocar todo el lado
    for y in range(box_size.height):
        con = False
        if y % mod == 0:
            con = y % 20 != 0 or y % 15 != 0 or y % 10 != 0
        else:
            con = y % 20 != 0 and y % 15 != 0

        if con:
            continue
            # if y > 600:
                # break
        for x in range(box_size.width):
            con = False
            if x % mod == 0:
                con = x % 20 != 0 or x % 15 != 0 or x % 10 != 0
            else:
                con = x % 20 != 0 and x % 15 != 0
            
            if con:
                continue
            # Dibuja
            draw_circles(image, x, y, x + circle_radius, y + circle_radius, amount)

    # Hacemos crop
    image = image.crop(box_size.box(105,105))

    all_white = list(map(lambda p: conver_to_3(p) == (255,255,255), image.getdata()))
    while not False in all_white:
        image = crazy_circles(box_size, circle_radius, amount, minimum, width)
        all_white = list(map(lambda p: conver_to_3(p) == (255,255,255), image.getdata()))

    return image


if __name__ == "__main__":
    i = crazy_circles(
        BoxSize(width=1200, height=1200), 
        circle_radius=random.randint(10, 100), 
        amount=random.randint(1, 10), 
        width=random.randint(1, 9)
    )
    
    # pixels = i.getdata()
    # new_pixels = []
    # for p in pixels:
    #     if p == (255,255,255):
    #         new_pixels.append((23,66,100))
    #     else:
    #         new_pixels.append((255,255,255))
    # i.putdata(new_pixels)

    i.show()