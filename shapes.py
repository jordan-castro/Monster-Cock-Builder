import random
from PIL import ImageDraw


class ShapeBuilder:
    """
    Para dibujar unos shapes en un MonsterCock|Hen
    """
    def __init__(self, image):
        self.image = image
        self.start_x = 291
        self.start_y = 41
        self.end_x = 575
        self.end_y = 415
        self.width, self.height = image.size
        # Cuantos amos dibujado?
        self.drawn = 0
        self.black_list_x = [x for x in range(self.start_x, self.end_x)]
        # El amount para dibujar
        self.amount = random.randint(0, self.width)

    def __decide_shape(self, drawing):
        """
        Decide el shape del monster cock/hen
        """
        decider = random.randint(1, 4)
        if decider == 1:
            self.__square(drawing)
        elif decider == 2:
            self.__triangle(drawing)
        elif decider == 3:
            self.__circle(drawing)
        elif decider == 4:
            self.__rectangle(drawing)

    def __square(self, drawing: ImageDraw):
        """
        Dibuja un square
        """
        drawing.rectagle()

    def __triangle(self, drawing: ImageDraw):
        """
        Dibuja un triangulo
        """

    def __circle(self, drawing: ImageDraw):
        """
        Dibuja un circulo
        """

    def __rectangle(self, drawing: ImageDraw):
        """
        Dibuja un rectangulo.
        """

    def draw(self):
        """
        Dibuja.
        """
        drawing = ImageDraw.Draw(self.image)
        while self.draw <= self.amount:
            self.__decide_shape(drawing)