from generator.attributes.attribute_builder import AttributesBuilder
from generator.attributes.canvas import get_canvas
from generator.utils import conver_to_3, create_image, current_amount
from generator.attributes.attributes import Attribute
from generator.random_data import randomify, randomifycolor, randomifyflip
from generator.chicken_type import ChickenType
from PIL import Image, ImageOps
from generator.colors_data import Colors


class ImageGen:
    def __init__(self, chicken_type: ChickenType, attributes: list=None):
        self.chicken_type = chicken_type
        self.name = self.decide_name()
        self.color_data = Colors(chicken_type)
        self.attributes = attributes
        self.image = self.open()

    def decide_name(self):
        if self.chicken_type == ChickenType.HEN:
            return "Sexy Hen"
        elif self.chicken_type == ChickenType.COCK:
            return "Monster Cock"
        else:
            return "Chick"

    def draw(self):
        """
        Dibuja un monster cock.
        """
        # Priemero tocamos los colores
        before = self.color_data.before
        after = self.color_data.after
        bckg = self.color_data.bckg

        # Dibuja!
        pixels = self.image.getdata()
        new_pixels = []
        # Loop sobre pixels
        for pixel in pixels:
            p = conver_to_3(pixel)
            # Chequea si tiene que cambiar!
            if p in before:
                p = after[before.index(p)]
            elif p == (255, 255, 255):
                p = bckg

            # Pon el nuevo pixel
            new_pixels.append(p)

        # Crea la imagen
        new_image = Image.new("RGB", self.image.size)
        new_image.putdata(new_pixels)

        number_of = current_amount()

        flip = randomifyflip(len(number_of))

        if flip:
            self.attributes.append(Attribute.MIRRORED)
            new_image = self.flip(new_image)

        # Crea el nombre
        name = f"{self.name} {len(number_of) + 1}"

        # Hacemos los attributos
        builder = AttributesBuilder(new_image, f"{name}.png")
        builder.build(self.chicken_type, self.attributes, self.color_data)

        return name

    def flip(self, image):
        """
        Flip el imagen.

        Params:     
            - <image: Image>
        """
        return ImageOps.mirror(image)

    def open(self):
        """
        Abre el photo de monster cock.

        Returns: <Image>
        """
        if self.chicken_type == ChickenType.HEN:
            # Abre el hen
            return create_image('base_art/hen_only.png', get_canvas(self.attributes), self.attributes, self.color_data)
            # return Image.open("hen_base.png")
        elif self.chicken_type == ChickenType.COCK:
            # Abre el cock
            return create_image('base_art/cock_only.png', get_canvas(self.attributes), self.attributes, self.color_data)
            # return Image.open("cock_base.png")
        else:
            return False
