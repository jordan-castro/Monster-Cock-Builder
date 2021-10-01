from generator.attributes.attribute_builder import AttributesBuilder
from generator.attributes.canvas import get_canvas, create_image
from generator.utils import conver_to_3, current_amount, replace_pixels
from generator.attributes.attributes import Attribute
from generator.random_data import randomifyflip
from generator.chicken_type import ChickenType
from PIL import Image, ImageOps
from generator.colors_data import Colors


class ImageGen:
    def __init__(self, chicken_type: ChickenType, id: int, attributes: list=None):
        self.chicken_type = chicken_type
        self.name = self.decide_name()
        self.color_data = Colors(chicken_type)
        self.attributes = attributes
        self.id = id
        self.image = self.open()

    def decide_name(self):
        if self.chicken_type == ChickenType.HEN:
            return "Sexy Hen"
        elif self.chicken_type == ChickenType.COCK:
            return "Monster Cock"
        elif self.chicken_type == ChickenType.DETAILED_COCK:
            return "Monster Cock"
        else:
            return "Chick"

    def decide_image(self):
        base = "base_art/"
        if self.chicken_type == ChickenType.HEN:
            return f"{base}hen_only.png"
        elif self.chicken_type == ChickenType.COCK:
            return f"{base}cock_only.png"
        elif self.chicken_type == ChickenType.DETAILED_COCK:
            return f"{base}FinalCockHR.png"
        else:
            return "Chick"

    def draw(self):
        """
        Dibuja un monster cock.
        """
        # Priemero tocamos los colores
        before = list(map(lambda c: c.before, self.color_data.colors))
        after = list(map(lambda c: c.after, self.color_data.colors))
        bckg = self.color_data.bckg

        # Dibuja!
        new_image = replace_pixels(self.image, after + [bckg], before + [(255,255,255)])

        flip = randomifyflip(self.id)

        if flip:
            self.attributes.append(Attribute.MIRRORED)
            new_image = self.flip(new_image)

        # Crea el nombre
        name = f"{self.name} {self.id}"

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
        return create_image(self.decide_image(), get_canvas(self.attributes), self.attributes, self.color_data)