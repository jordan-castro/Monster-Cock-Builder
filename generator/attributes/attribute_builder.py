from generator.colors_data import Color, Colors
from generator.attributes.attributes import Attribute, convert_attribute_to_string
from generator.tracker.tracker import tracker


def build_attributes_json(colors: Colors, attr: list[Attribute]):
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
        # Filteramos los valueos que son repetido
        colors = list(set(colors))
        return '-'.join(colors)

    comb_colors = grab_colors('Comb')
    nose_colors = grab_colors('Beak')
    eye_color = grab_colors('Eye')
    neck_colors = grab_colors('Neck')
    back_color = grab_colors('Back')
    chest_colors = grab_colors('Chest')
    wing_colors = grab_colors('Wing')
    leg_colors = grab_colors('Leg')

    attributes.append(attribute_dict('Comb', create_attr_from_colors(comb_colors)))
    attributes.append(attribute_dict('Beak', create_attr_from_colors(nose_colors)))
    attributes.append(attribute_dict('Eye', create_attr_from_colors(eye_color)))
    attributes.append(attribute_dict('Neck', create_attr_from_colors(neck_colors)))
    attributes.append(attribute_dict('Back', create_attr_from_colors(back_color)))
    attributes.append(attribute_dict('Chest', create_attr_from_colors(chest_colors)))
    attributes.append(attribute_dict('Wing', create_attr_from_colors(wing_colors)))
    attributes.append(attribute_dict('Leg', create_attr_from_colors(leg_colors)))
    # Ahora hacemos overide para los attributos invicos
    for attribute in attr:
        _attr = convert_attribute_to_string(attribute)
        # Chequea si no encontramos algo con los attributos.
        if not _attr:
            continue
        for inner in attributes:
            # Chequea si esta attribu ya existe
            if inner['trait_type'] == _attr[0] and not inner['trait_type'] == "Schema":
                del attributes[attributes.index(inner)]
                break
        attributes.append(attribute_dict(_attr[0], _attr[1]))

    return attributes


# class AttributesBuilder:
#     def __init__(self, image, output) -> None:
#         self.image = image
#         self.output = output
    
#     # def build(self, chicken_type: ChickenType, attributes: list, color_data: Colors):
#     #     """
#     #     Crea la imagen.

#     #     Params:
#     #         - <chicken_type: ChickenType> El tipo de pollo, COCK, HEN, CHICK, ETC.
#     #         - <attributes: list> Lista de attributes. Tambien va en un JSON file.
#     #         - <color_data: Colors> La data de colores para su pollo.
#     #     """
#     #     # Setamos variableos privados
#     #     self.type = chicken_type
#     #     self.attr = attributes
#     #     self.colors = color_data

#     #     # Chequeamos si hay gradient o no

#     #     self.finish()

#     @staticmethod
#     def pretty_attributes(colors: Colors, attr: list[Attribute]):
#         """
#         Crea los attributes para el JSON.

#         Returns: <dict>
#         """
#         attributes = []

#         def grab_colors(value):
#             return filter(
#                 None, 
#                 list(
#                     map(
#                         lambda c: c.value if c.title == value else None, 
#                         colors.colors
#                     )
#                 )
#             )

#         def create_attr_from_colors(colors: list[Color]):
#             # Filteramos los valueos que son repetido
#             colors = list(set(colors))
#             return '-'.join(colors)

#         comb_colors = grab_colors('Comb')
#         nose_colors = grab_colors('Beak')
#         eye_color = grab_colors('Eye')
#         neck_colors = grab_colors('Neck')
#         back_color = grab_colors('Back')
#         chest_colors = grab_colors('Chest')
#         wing_colors = grab_colors('Wing')
#         leg_colors = grab_colors('Leg')

#         attributes.append(attribute_dict('Comb', create_attr_from_colors(comb_colors)))
#         attributes.append(attribute_dict('Beak', create_attr_from_colors(nose_colors)))
#         attributes.append(attribute_dict('Eye', create_attr_from_colors(eye_color)))
#         attributes.append(attribute_dict('Neck', create_attr_from_colors(neck_colors)))
#         attributes.append(attribute_dict('Back', create_attr_from_colors(back_color)))
#         attributes.append(attribute_dict('Chest', create_attr_from_colors(chest_colors)))
#         attributes.append(attribute_dict('Wing', create_attr_from_colors(wing_colors)))
#         attributes.append(attribute_dict('Leg', create_attr_from_colors(leg_colors)))
#         # Ahora hacemos overide para los attributos invicos
#         for attribute in attr:
#             _attr = convert_attribute_to_string(attribute)
#             # Chequea si no encontramos algo con los attributos.
#             if not _attr:
#                 continue
#             for inner in attributes:
#                 # Chequea si esta attribu ya existe
#                 if inner['trait_type'] == _attr[0] and not inner['trait_type'] == "Schema":
#                     del attributes[attributes.index(inner)]
#                     break
#             attributes.append(attribute_dict(_attr[0], _attr[1]))

#         return attributes

#     # def __update_image_pixels__(self, pixels):
#     #     """
#     #     Actualizamos la imagen con nuevo pixels!

#     #     Params: 
#     #         - <pixels: list> Los pixels
#     #     """
#     #     self.image.putdata(pixels)

#     # def __add_new_image__(self, source, xy: tuple[int,int], flip: bool=False):
#     #     """
#     #     Pon un nuevo imagen... Watermark

#     #     Params:
#     #         - <source: str> El imagen para hacer watermark.
#     #         - <xy: tuple[int,int]> El x y, y
#     #         - <flip: bool=False> Deberiamos hacer un flip?
#     #     """
#     #     image = Image.open(source)

#     #     if flip:
#     #         image = ImageOps.flip(image)

#     #     self.image.paste(image, xy, image)

#     # def finish(self):
#     #     """
#     #     Termina creando el imagen.
#     #     """
#     #     self.image.save(self.output, 'PNG')

#     # def ninjafy(self):
#     #     """
#     #     Hacemos el attribo de ninja.
#     #     """
#     #     new_pixels = replace_pixels(self.image, [(25,25,25)], [self.colors.bckg])

#     #     # Cambiamos la data
#     #     self.__update_image_pixels__(new_pixels.getdata())

#     # def add_sun(self):
#     #     """
#     #     Ponemos el sol a la izquierda! Aveces tambien la derecha.
#     #     """
#     #     x = 0
#     #     y = 0

#     #     self.__add_new_image__("base_art/sun.png", (x,y))

#     # def moonify(self, phase: Attribute):
#     #     """
#     #     Ponemos una luna.

#     #     Params:
#     #         - <phase: Attribute> El phase de la luna.
#     #     """
#     #     x = self.image.size[0] - 150
#     #     y = 10

#     #     if phase == Attribute.MOON_P1:
#     #         moon = "moon_p1"
#     #     elif phase == Attribute.MOON_P2:
#     #         moon = "moon_p2"
#     #     elif phase == Attribute.MOON_P3:
#     #         moon = "moon_p3"

#     #     self.__add_new_image__(f"base_art/{moon}.png", (x,y))

#     # def stripefy(self):
#     #     """
#     #     Creamos unos stripes en el cuerpo del monstercock!
#     #     """
#     #     pass


def attribute_dict(trait, value):
    return {'trait_type': trait, 'value': value}