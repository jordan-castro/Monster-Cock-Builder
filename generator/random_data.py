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