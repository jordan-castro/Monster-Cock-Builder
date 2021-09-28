### Script para crear fractals con squares
import random
from generator.fractals.box_size import BoxSize
from PIL import Image, ImageDraw


def draw_squares(**kwargs):
    image = kwargs['image']
    amount = kwargs['amount']
    minimum = kwargs['minimum']
    x1 = kwargs['x1']
    y1 = kwargs['y1']
    x2 = kwargs['x2']
    y2 = kwargs['y2']
    width = kwargs['width']
    outline = kwargs['outline']
    
    if amount < minimum:
        return

    drawing = ImageDraw.Draw(image)
    drawing.rectangle((x1, y1, x2, y2), width=width, outline=outline)

    kwargs['amount'] -= 1

    # Recursion!    
    draw_squares(**kwargs)


def draw_round_squares(**kwargs):
    image = kwargs['image']
    amount = kwargs['amount']
    minimum = kwargs['minimum']
    x1 = kwargs['x1']
    y1 = kwargs['y1']
    x2 = kwargs['x2']
    y2 = kwargs['y2']
    width = kwargs['width']
    radius = kwargs['radius']
    outline = kwargs['outline']

    if amount < minimum:
        return

    drawing = ImageDraw.Draw(image)
    drawing.rounded_rectangle((x1, y1, x2, y2), radius=radius, width=width, outline=outline)

    kwargs['amount'] -= 1

    draw_round_squares(**kwargs)


# if __name__ == "__main__":
#     i = fractify(
#         BoxSize(
#             width=1200,
#             height=1200
#         ),
#         draw_round_squares,
#         size=random.randint(1, 100),
#         amount=random.randint(1, 10),
#         width=random.randint(1, 10),
#         radius=5
#     )

#     i.show()