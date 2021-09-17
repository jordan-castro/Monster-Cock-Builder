from generator.attributes.attributes import Attribute
from generator.random_data import randomify
from generator.chicken_type import ChickenType
from PIL import Image, ImageOps
from generator.colors_data import Colors
from glob import glob


class ImageGen:
    def __init__(self, chicken_type: ChickenType, attribute: Attribute=None):
        self.chicken_type = chicken_type
        self.image = self.open()
        self.name = self.decide_name()
        self.color_data = Colors(chicken_type)
        self.attribute = attribute

    def decide_name(self):
        if self.chicken_type == ChickenType.HEN:
            return "hen"
        elif self.chicken_type == ChickenType.COCK:
            return "cock"
        else:
            return "chick"

    def draw(self):
        """
        Dibuja un monster cock.
        """
        # Priemero tocamos los colores
        before = self.color_data.before
        after = self.color_data.after
        bckg = self.color_data.random_bck()

        # Dibuja!
        pixels = self.image.getdata()
        new_pixels = []
        # Loop sobre pixels
        for pixel in pixels:
            p = self.conver_to_3(pixel)
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

        number_of = glob('*.png')

        # Chequea si deberiamos hacer flip
        mod = len(number_of) % 1000
        flip = randomify(range(mod, mod + 10)) % 10 == 0

        if flip:
            new_image = self.flip(new_image)

        new_image.save(f'{self.name} ({len(number_of) + 1}).png')

    def conver_to_3(self, pixel):
        """
        Converte un tupple de 4 a un tupple de 3

        Returns: <tupple>
        """
        return (pixel[0], pixel[1], pixel[2])

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
            return Image.open("hen_base.png")
        elif self.chicken_type == ChickenType.COCK:
            # Abre el cock
            return Image.open("cock_base.png")
        else:
            return False
