from generator.utils import replace_pixels, rgb_to_name
from generator.colors_data import Color, Colors
from generator.chicken_type import ChickenType
from generator.attributes.attributes import Attribute, convert_attribute_to_string
from PIL import Image, ImageOps
from generator.fractals.crazy_circles import crazy_circles
from generator.fractals.box_size import BoxSize


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
            elif attribute == Attribute.MOON_P1 or attribute == Attribute.MOON_P2 or attribute == Attribute.MOON_P3:
                self.moonify(attribute)
            # elif attribute == Attribute.CRAZY_CIRCLES:
            #     self.crazy_circles()

        self.finish()

    @staticmethod
    def pretty_attributes(colors: Colors, attr: list[Attribute]):
        """
        Crea los attributes para el JSON.

        Returns: <dict>
        """
        attributes = []

        def grab_colors(value):
            return filter(
                None, 
                list(
                    map(
                        lambda c: c.value if c.title == value else None, 
                        colors.colors
                    )
                )
            )

        def create_attr_from_colors(colors: list[Color]):
            return '-'.join(colors)

        comb_colors = grab_colors('Comb')
        nose_colors = grab_colors('Nose')
        eye_color = grab_colors('Eye')
        neck_colors = grab_colors('Neck')
        back_color = grab_colors('Back')
        chest_colors = grab_colors('Chest')
        wing_colors = grab_colors('Wing')
        leg_colors = grab_colors('Leg')

        attributes.append(attribute_dict('Comb color', create_attr_from_colors(comb_colors)))
        attributes.append(attribute_dict('Nose color', create_attr_from_colors(nose_colors)))
        attributes.append(attribute_dict('Eye color', create_attr_from_colors(eye_color)))
        attributes.append(attribute_dict('Neck color', create_attr_from_colors(neck_colors)))
        attributes.append(attribute_dict('Back color', create_attr_from_colors(back_color)))
        attributes.append(attribute_dict('Chest color', create_attr_from_colors(chest_colors)))
        attributes.append(attribute_dict('Wing color', create_attr_from_colors(wing_colors)))
        attributes.append(attribute_dict('Leg color', create_attr_from_colors(leg_colors)))
        # Ahora hacemos overide para los attributos invicos
        for attribute in attr:
            _attr = convert_attribute_to_string(attribute)
            # Chequea si no encontramos algo con los attributos.
            if not _attr:
                continue
            # Chequea si estamos haciendo como negro con aura.
            if _attr[0] == "aura":
                _attr[1] = rgb_to_name(colors.aura)
            # Chequea si esta attribu ya existe
            for inner in attributes:
                if inner['trait_type'] == _attr[0]:
                    del attributes[attributes.index(inner)]
                    break
            attributes.append(attribute_dict(_attr[0], _attr[1]))

        return attributes

    def __update_image_pixels__(self, pixels):
        """
        Actualizamos la imagen con nuevo pixels!

        Params: 
            - <pixels: list> Los pixels
        """
        self.image.putdata(pixels)

    def __add_new_image__(self, source, xy: tuple[int,int], flip: bool=False):
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
        self.__update_image_pixels__(new_pixels)

    def add_sun(self):
        """
        Ponemos el sol a la izquierda! Aveces tambien la derecha.
        """
        x = 0
        y = 0

        self.__add_new_image__("base_art/sun.png", (x,y))

    def moonify(self, phase: Attribute):
        """
        Ponemos una luna.

        Params:
            - <phase: Attribute> El phase de la luna.
        """
        x = self.image.size[0] - 150
        y = 10

        if phase == Attribute.MOON_P1:
            moon = "moon_p1"
        elif phase == Attribute.MOON_P2:
            moon = "moon_p2"
        elif phase == Attribute.MOON_P3:
            moon = "moon_p3"

        self.__add_new_image__(f"base_art/{moon}.png", (x,y))

    def stripefy(self):
        """
        Creamos unos stripes en el cuerpo del monstercock!
        """
        pass

    # def crazy_circles(self):
    #     """
    #     Usamos el Crazy Circles function.
    #     """
    #     # Crea un nuevo canvas con los crazy circles!
    #     image = crazy_circles(
    #         BoxSize(
    #             self.image.width, 
    #             self.image.height
    #         ),
    #         circle_radius=random.randint(10, 100), 
    #         amount=random.randint(1, 10), 
    #         width=random.randint(1, 9),
    #         # image=self.image,
    #     )

    #     # Toma los pixels del imagen
    #     pixels = image.getdata()
    #     # Cambia los pixels a colores random
    #     new_pixels = replace_pixels(pixels, [randomifycolor(), self.colors.bckg], [(0,0,0), (255,255,255)])
    #     # Actualiza
    #     image.putdata(new_pixels)
        
    #     # Gurda el photo y hacemos transparent
    #     self.finish()
    #     make_transparent(self.output, self.colors.bckg)

    #     self.image = Image.open(self.output)
    #     self.image = center_image(image, self.image)

    #     #Pon el cock en el canvas
    #     image.paste(self.image, (0,0), self.image)
    #     self.image = image

def attribute_dict(trait, value):
    return {'trait_type': trait, 'value': value}
