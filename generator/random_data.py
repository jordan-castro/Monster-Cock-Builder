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
    

def randombool()-> bool:
    """
    Hacemos un bool random.

    Returns: <bool>
    """
    x = random.randint(0, 200)
    return True if x % 2 == 0 else False


def randomifyattributes(generation: Attribute)-> list:
    """
    Creamos unos attributos totalmente random.

    Params:
        - <generation: Attribute> El atributo de su generation.

    Returns: <list>
    """
    # Los attributos para regresar
    attributes = [generation]

    # Los attributos possibles
    possible_attributes = [
        Attribute.GRADIENT_H,
        Attribute.GRADIENT_V,
        # Attribute.NINJA,
        Attribute.CRAZY_CIRCLES,
        Attribute.ROUND_SQUARES,
        Attribute.SQUARES,
        Attribute.STRIPES
    ]

    gradients = [
        Attribute.GRADIENT_H,
        Attribute.GRADIENT_V,
    ]

    moon_phases = [
        Attribute.MOON_P1,
    ]

    attributes = randomifylist(possible_attributes)

    attributes = __can_have_attr__(attributes, gradients)
    attributes = __can_have_attr__(attributes, moon_phases + [Attribute.SUN])

    # Ponemos su generation
    attributes.append(generation)

    return attributes


def randomifylist(list: list)-> list:
    """
    Regresa una forma de la lista random!
    
    Params:
        - <list: list> La lista para hacer random con!

    Returns: <list>
    """
    # Empieza a zero
    start = 0
    end = 0

    # Loop para nunca pueden ser mismo
    while start == end:
        start = random.randint(0, len(list))
        end = random.randint(start, len(list))

    # Hacemos shuffle para mas random
    random.shuffle(list)

    # Regresa con el range
    return list[start:end]


def __can_have_attr__(current_list: list[Attribute], black_list: list[Attribute]):
    """
    Para saber si un lista de attributos puden tener el attributo.

    Params:
        - <current_list: list[Attribute]> Los attributos antes de ser limpiado.
        - <black_list: list[Attribute]> Los attributos que solo pueden tener un pie en la puerta de `current_list`.
    
    Returns: <list>
    """
    attributes = []
    has_foud = False

    # Loop de la lista currentamente
    for attribute in current_list:
        # Chequea si esta en black_list pero que attributes no tiene uno de los black_list
        if attribute in black_list and not has_foud:
            # Solo podemos tener uno!
            only = random.randint(0, len(black_list) - 1)
            for black in black_list:
                index = black_list.index(black)
                # Chequeamos el index es only.
                if index == only:
                    attributes.append(black)
                    has_foud = True
                    break
        elif not attribute in black_list:
            attributes.append(attribute)
        else:
            continue

    return attributes 


if __name__ == "__main__":
    randomifyattributes(Attribute.GEN_0)