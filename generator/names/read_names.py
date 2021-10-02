### Script para sacar todos los nombres del .txt
from generator.chicken_type import ChickenType
import codecs
import random


def scrape_names(chicken_type: ChickenType):
    """
    Hacemos un scrape de los nombres.

    Params:
        - <chicken_type: ChickenType> El tipo de pollo.

    Returns: <list>
    """
    names = []
    gender = 'm' if chicken_type == ChickenType.DETAILED_COCK else "f" 
    # Abre el file
    with codecs.open("names.txt", 'r', 'utf8') as names_file:
        # Lee los linias
        lines = names_file.readlines()
        # Loop por nombres
        for line in lines:
            # Busca la data!
            data = line.split('\t')
            # Chequa por gender
            if 'm' in data[1]:
                names.append(data[0])

    return names


def used_names():
    """
    Regresa una lista de todos los nombres que ya han sido usado.

    Returns: <list>
    """
    with codecs.open('blacklistnames.txt', 'r', 'utf8') as file:
        return file.readlines()


def black_list_name(name: str):
    """
    Ponemos el nombre en blacklistednames.txt

    Params:
        - <name: str> El nombre de blacklist.
    """
    with codecs.open('blacklistnames.txt', 'a', 'utf8') as file:
        file.write(name)
        file.write('\n')


def get_random_name(chicken_id: int, chicken_type: ChickenType):
    """
    Toma el nombre del pollo.

    Params:
        - <chicken_id: int> El id del pollo.
        - <chicken_type: ChickenType> El tipo del pollo.

    Returns: <str>
    """
    names = scrape_names(chicken_type)
    # Busca los nombres que ya han sido usado
    already_used = used_names()

    start = True
    chosen_name = "TOtAlMeNtENomBReRaNddOm"
    while start or chosen_name in already_used:
        # Chequea si esto es el primer 
        if start:
            start = False

        # El index de random
        index = random.randint(0, len(names))
        # Busca el nombre
        chosen_name = names[index]

    # Pon el nombre en blakclist
    black_list_name(chosen_name)

    return chosen_name


if __name__ == "__main__":
    names = scrape_names(ChickenType.DETAILED_COCK)
    index = random.randint(0, len(names))
    print(f"El nombre chosen es {names[index]}")