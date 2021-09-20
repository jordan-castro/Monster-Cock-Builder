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
        Attribute.MOON_P1,
        # Attribute.MOON_P2,
        # Attribute.MOON_P3,
        # Attribute.MOON_P4,  
        # Attribute.GRADIENT_W
    ]

    gradients = [
        Attribute.GRADIENT_H,
        Attribute.GRADIENT_V,
    ]

    moon_phases = [
        Attribute.MOON_P1,
        # Attribute.MOON_P2,
        # Attribute.MOON_P3,
    ]

    # Ahora dos randoms
    start = random.randint(0, len(possible_attributes))
    end = random.randint(start, len(possible_attributes))
    
    # Chequa si son igual
    if start == end:
        return attributes

    # Hacemos un random shuffle
    random.shuffle(possible_attributes)
    print(possible_attributes)
    attributes = possible_attributes[start:end]

    # Chequea que solo tiene un tipo de Gradient
    if Attribute.GRADIENT_H in attributes or Attribute.GRADIENT_V in attributes or Attribute.GRADIENT_W in attributes:
        only = random.randint(0, len(gradients) - 1)
        for x in gradients:
            try:
                attributes.remove(gradients[x])
            except:
                continue

        attributes.append(gradients[only]) 
        
        if Attribute.NINJA in attributes:
            # No pueden tener ninja si tiene gradient
            attributes.remove(Attribute.NINJA)

        if Attribute.AURA in attributes:
            # No puede tener aura entonces
            attributes.remove(Attribute.AURA)
    
    # Chequea si hay luna!
    if Attribute.MOON_P1 in attributes or Attribute.MOON_P2 in attributes or Attribute.MOON_P3 in attributes:
        only = random.randint(0, len(moon_phases) - 1)
        for x in moon_phases:
            try:
                attributes.remove(moon_phases[x])
            except:
                continue
        attributes.append(only)

        if Attribute.SUN in attributes:
            # Quita el sol si hay
            attributes.remove(Attribute.SUN)

    # Ponemos su generation
    attributes.append(generation)

    print(attributes)

    return attributes