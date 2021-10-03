### Script para poner gradients.
from generator.random_data import randomify, randomifycolor
from generator.attributes.attributes import Attribute
from generator.colors_data import Colors


class Point(object):
    def __init__(self, x, y):
        self.x, self.y = x, y

class Rect(object):
    def __init__(self, x1, y1, x2, y2):
        minx, maxx = (x1,x2) if x1 < x2 else (x2,x1)
        miny, maxy = (y1,y2) if y1 < y2 else (y2,y1)
        self.min = Point(minx, miny)
        self.max = Point(maxx, maxy)

    width  = property(lambda self: self.max.x - self.min.x)
    height = property(lambda self: self.max.y - self.min.y)


class Gradients:
    def __init__(self,image, drawing, colors: Colors, gradiant_type: Attribute):
        if gradiant_type not in [Attribute.GRADIENT_W, Attribute.GRADIENT_H, Attribute.GRADIENT_V]:
            # Tiramos error
            raise Exception(f"{gradiant_type} No es un Gradient!")

        self.colors = colors
        self.type = gradiant_type
        self.image = image
        self.drawing = drawing
        # El rectangle
        self.rect = Rect(0, 0, self.image.size[0], self.image.size[1])
        self.__palette__()

    def draw(self):
        """
        Dibjua el gradient.
        """
        if self.type == Attribute.GRADIENT_V:
            self.vertical_gradient()
        elif self.type  == Attribute.GRADIENT_H:
            self.horizontal_gradient()

        return self.color_palette
        
    def __palette__(self):
        """
        Crea el palette.
        """
        amount = randomify(range(0, 5))
        self.color_palette = []

        # Cheqeua se es menos de uno
        if amount <= 1:
            amount = 2

        # Pon los colores
        for x in range(amount):
            self.color_palette.append(randomifycolor())

    def lerp_color(self, min_val, max_val, val):
        """
        Hacemos un lerp de los colores.

        Returns: <tuple[int,int,int]>
        """
        max_index = len(self.color_palette)-1
        delta = max_val - min_val
        if delta == 0:
            delta = 1
        v = float(val-min_val) / delta * max_index
        i1, i2 = int(v), min(int(v)+1, max_index)
        (r1, g1, b1), (r2, g2, b2) = self.color_palette[i1], self.color_palette[i2]
        f = v - i1
        return int(r1 + f*(r2-r1)), int(g1 + f*(g2-g1)), int(b1 + f*(b2-b1))

    def vertical_gradient(self):
        """
        Crea un gradient vertical.
        """
        minval, maxval = 1, len(self.color_palette)
        delta = maxval - minval
        height = float(self.rect.height)  # Cache.
        for y in range(self.rect.min.y, self.rect.max.y+1):
            f = (y - self.rect.min.y) / height
            val = minval + f * delta
            color = self.lerp_color(minval, maxval, val)
            self.drawing.line([(self.rect.min.x, y), (self.rect.max.x, y)], fill=color)
    
    def horizontal_gradient(self):
        """
        Crea un gradient horizontal.
        """
        minval, maxval = 1, len(self.color_palette)
        delta = maxval - minval
        width = float(self.rect.width)  # Cache.
        for x in range(self.rect.min.x, self.rect.max.x+1):
            f = (x - self.rect.min.x) / width
            val = minval + f * delta
            color = self.lerp_color(minval, maxval, val)
            self.drawing.line([(x, self.rect.min.y), (x, self.rect.max.y)], fill=color)
