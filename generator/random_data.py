from generator.attributes.attributes import Attribute
import random


def randomify(range=None):
    """
    Crear unos data de random
    """
    return random.randrange(range[0], range[-1])


def randomifycolor():
    """
    Crea un color totalmente random!
    """
    return (
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255)
    )


def randomifyflip(amount_so_far: int)-> bool:
    """
    Deberiamos hacer flip?

    Params:
        - <amount_so_far: int> El numero de monster cocks ahora
    
    Returns: <bool>
    """
    # Chequea si deberiamos hacer flip
    mod = amount_so_far % 1000
    flip = randomify(range(mod, mod + 10)) % 10 == 0
    return flip


def randomifyattributes(generation: Attribute)-> list:
    """
    Creamos unos attributos totalmente random.

    Params:
        - <generation: Attribute> El atributo de su generation.

    Returns: <list>
    """
    # Los attributos para regresar
    attributes = []

    # Los attributos possibles
    possible_attributes = [
        Attribute.GRADIENT_H,
        Attribute.GRADIENT_V,
        Attribute.AURA,
        Attribute.NINJA,
        Attribute.SUN,
        Attribute.MOON,
        # Attribute.GRADIENT_W
    ]

    # Ahora dos randoms
    start = random.randint(0, len(possible_attributes))
    end = random.randint(start, len(possible_attributes))
    
    # Chequa si son igual
    if start == end:
        return attributes

    # Hacemos un random shuffle
    random.shuffle(possible_attributes)
    attributes = possible_attributes[start:end]

    # Chequea que solo tiene un tipo de Gradient
    if Attribute.GRADIENT_H in attributes and Attribute.GRADIENT_V in attributes and Attribute.GRADIENT_W in attributes:
        only = random.randint(0, 2)
        if only == 0:
            attributes.remove(Attribute.GRADIENT_V)
            attributes.remove(Attribute.GRADIENT_W)
        elif only == 1:
            attributes.remove(Attribute.GRADIENT_H)
            attributes.remove(Attribute.GRADIENT_W)
        elif only == 2:
            attributes.remove(Attribute.GRADIENT_H)
            attributes.remove(Attribute.GRADIENT_V)
        # No puede tener aura entonces
        attributes.remove(Attribute.AURA)
    
    # Ponemos su generation
    attributes.append(generation)

    return attributes