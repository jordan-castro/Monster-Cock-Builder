### Una lista de attributes
from enum import Enum


class Attribute(Enum):
    NINJA = 0
    AURA = 1
    VAMPIRE = 2
    SUN = 3
    STRIPES = 4
    GEN_0 = 5
    GEN_1 = 6
    GEN_2 = 7
    MIRRORED = 8


def convert_attribute_to_string(attribute: Attribute):
    """
    Converte un attribute a su nombre como string.
    
    Ejemplo: Attribute.NINJA: ("background", "Ninja")

    Returns: <str>
    """
    data = []

    if attribute == Attribute.NINJA:
        data = ["background","Ninja"]
    elif attribute == Attribute.AURA:
        data = ["aura", "some_color"]
    elif attribute == Attribute.VAMPIRE:
        data = ["body", "Vampire"]
    elif attribute == Attribute.SUN:
        data = ["background", "Sunny"]
    elif attribute == Attribute.STRIPES:
        data = ["body", "Stripes"]
    elif attribute == Attribute.GEN_0:
        data = ["generation", 0]
    elif attribute == Attribute.GEN_1:
        data = ["generation", 1]
    elif attribute == Attribute.GEN_2:
        data = ["generation", 2]
    elif attribute == Attribute.MIRRORED:
        data = ["direction", "mirrored"]

    return data