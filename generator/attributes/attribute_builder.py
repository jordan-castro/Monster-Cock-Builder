from generator.colors_data import Color, Colors
from generator.attributes.attributes import Attribute, convert_attribute_to_string
from generator.tracker.tracker import tracker


def build_attributes_json(colors: Colors, attr: list[Attribute]):
    """
    Crea los attributes para el JSON.

    Returns: <dict>
    """
    attributes = []

    # Toma los colores
    def grab_colors(value):
        return filter(
            None, # Quitamos los None
            list(
                map(
                    lambda c: c.value if c.title == value else None, # Solo queremos el value 
                    colors.colors
                )
            )
        )

    def create_attr_from_colors(colors: list[Color]):
        # Filteramos los valueos que son repetido
        colors = list(set(colors))
        return '-'.join(colors)

    # Busca los colores
    comb_colors = grab_colors('Comb')
    nose_colors = grab_colors('Beak')
    eye_color = grab_colors('Eye')
    neck_colors = grab_colors('Neck')
    back_color = grab_colors('Back')
    chest_colors = grab_colors('Chest')
    wing_colors = grab_colors('Wing')
    leg_colors = grab_colors('Leg')

    # Pon en los attributos 
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


def attribute_dict(trait, value):
    return {'trait_type': trait, 'value': value}