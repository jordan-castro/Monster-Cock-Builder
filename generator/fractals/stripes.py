from PIL import ImageDraw


def draw_stripes(**kwargs):
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
    drawing.line((x1, y1, x2, y2), width=width, fill=outline)

    kwargs['amount'] -= 1

    draw_stripes(**kwargs)