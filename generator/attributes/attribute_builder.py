from generator.random_data import randomifyflip
from generator.utils import conver_to_3, current_amount, replace_pixels, rgb_to_name
from generator.colors_data import Colors
from generator.chicken_type import ChickenType
from generator.attributes.attributes import Attribute, convert_attribute_to_string
from PIL import Image, ImageOps


class AttributesBuilder:
    def __init__(self, image, output) -> None:
        self.image = image
        self.output = output
    
    def build(self, chicken_type: ChickenType, attributes: list, color_data: Colors):
        """
        Crea la imagen.

        Params:
            - <chicken_type: ChickenType> El tipo de pollo, COCK, HEN, CHICK, ETC.
            - <attributes: list> Lista de attributes. Tambien va en un JSON file.
            - <color_data: Colors> La data de colores para su pollo.
        """
        # Setamos variableos privados
        self.type = chicken_type
        self.attr = attributes
        self.colors = color_data

        for attribute in attributes:
            if attribute == Attribute.NINJA:
                self.ninjafy()
            elif attribute == Attribute.STRIPES:
                self.stripefy()
            elif attribute == Attribute.SUN:
                self.add_sun()

        self.finish()

    @staticmethod
    def pretty_attributes(colors: Colors, attr: list[Attribute]):
        """
        Crea los attributes para el JSON.

        Returns: <dict>
        """
        attributes = []

        def correct_json(trait, value):
            return {"trait_type": trait, "value": value}

        def correct_color(before):
            return colors.after[colors.before.index(before)]

        # Primero los colores
        attributes.append(correct_json('background', rgb_to_name(colors.bckg)))

        attributes.append(correct_json('eye', rgb_to_name(correct_color(colors.eye))))
        attributes.append(correct_json('body', rgb_to_name(correct_color(colors.cuerpo))))
        attributes.append(correct_json('border', rgb_to_name(correct_color(colors.border))))
        attributes.append(correct_json('comb', rgb_to_name(correct_color(colors.thingy))))
        attributes.append(correct_json('nose', rgb_to_name(correct_color(colors.nose))))
        attributes.append(correct_json('wing', rgb_to_name(correct_color(colors.wing))))

        # Chequeamos para pies
        if colors.feet:
            attributes.append(correct_json('foot', rgb_to_name(colors.feet[0])))
            attributes.append(correct_json('heel', rgb_to_name(colors.feet[1])))

        # Ahora hacemos overide para los attributos invicos
        for attribute in attr:
            _attr = convert_attribute_to_string(attribute)
            # Chequea si estamos haciendo como negro con aura.
            if _attr[0] == "aura":
                _attr[1] = rgb_to_name(colors.aura)
            # Chequea si esta attribu ya existe
            for inner in attributes:
                if inner['trait_type'] == _attr[0]:
                    del attributes[attributes.index(inner)]
                    break
            attributes.append(correct_json(_attr[0], _attr[1]))

        return attributes

    def update_image_pixels(self, pixels):
        """
        Actualizamos la imagen con nuevo pixels!

        Params: 
            - <pixels: list> Los pixels
        """
        self.image.putdata(pixels)

    def add_new_image(self, source, xy: tuple[int,int], flip: bool=False):
        """
        Pon un nuevo imagen... Watermark

        Params:
            - <source: str> El imagen para hacer watermark.
            - <xy: tuple[int,int]> El x y, y
            - <flip: bool=False> Deberiamos hacer un flip?
        """
        image = Image.open(source)

        if flip:
            image = ImageOps.flip(image)

        self.image.paste(image, xy, image)

    def finish(self):
        """
        Termina creando el imagen.
        """
        self.image.save(self.output, 'PNG')

    def ninjafy(self):
        """
        Hacemos el attribo de ninja.
        """
        # Buscamos la data.
        pixels = self.image.getdata()

        new_pixels = replace_pixels(pixels, [(25,25,25)], [self.colors.bckg])

        # Cambiamos la data
        self.update_image_pixels(new_pixels)

    def add_sun(self):
        """
        Ponemos el sol a la izquierda! Aveces tambien la derecha.
        """
        x = 0
        y = 0

        flip = randomifyflip(len(current_amount()))

        # Si flip, entonces cambia el x
        if flip:
            x = self.image.size[0] - 150

        self.add_new_image("base_art/sun.png", (x,y), flip=flip)

    def stripefy(self):
        """
        Creamos unos stripes en el cuerpo del monstercock!
        """
        pass