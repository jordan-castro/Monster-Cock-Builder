from generator.attributes.attributes import Attribute


def get_canvas(attributes: list):
    """
    Busca un canvas!!

    Params: 
        - <attributes: list> Lista de attributos.

    Returns: <str>
    """
    base = "base_art/"
    canvas = "canvas"
    # Loop
    for attribute in attributes:
        # if attribute == Attribute.SUN:
        #     canvas = "sun_canvas"
        #     break
        # else:
        pass

    return f"{base}{canvas}.png"