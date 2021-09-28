import random
from PIL import ImageDraw


# Dibuja los circulos
def draw_circles(**kwargs):
    image = kwargs['image']
    x1 = kwargs['x1']
    y1 = kwargs['y1']
    x2 = kwargs['x2']
    y2 = kwargs['y2']
    amount = kwargs['amount']
    minimum = kwargs['minimum']
    fill = kwargs['fill']
    outline = kwargs['outline']
    width = kwargs['width']

    # Si el amount es 0 ya termina pues
    if amount < minimum:
        return

    # Dibuja el circulo       
    drawing = ImageDraw.Draw(image)
    drawing.ellipse(
        (x1, y1, x2, y2),
        width=width,
        fill=fill,
        outline=outline
    )

    # Crea los coordinatos siguientes
    x1 += random.randint(x1, x1 + 200)
    x2 -= random.randint(x1, x1 + 200)
    y1 += random.randint(y1, y1 + 200)
    y2 -= random.randint(y1, y1 + 200)
    # Recursion!!
    draw_circles(
        image=image,
        x1=x1,
        y1=y1,
        x2=x2,
        y2=y2,
        amount=amount - 1,
        minimum=minimum,
        fill=fill,
        outline=outline,
        width=width
    )


# if __name__ == "__main__":
#     size = BoxSize(1200, 1200)
#     radius=random.randint(10, 100)
#     # amount=random.randint(1, 20)
#     width=random.randint(1, 9)
    
#     i = fractify(
#         BoxSize(width=1200, height=1200), 
#         draw_circles,
#         radius=radius, 
#         amount=1, 
#         width=width
#     )
#     # pixels = i.getdata()
#     # new_pixels = []
#     # for p in pixels:
#     #     if p == (255,255,255):
#     #         new_pixels.append((23,66,100))
#     #     else:
#     #         new_pixels.append((255,255,255))
#     # i.putdata(new_pixels)

#     i.show()