### Script para customizar los fields de Un monstercock
from generator.utils import bool_from_input, expect_input


def custom_monster_cock():
    """
    Pregunta para los fields custom.

    Returns <dict>
    """
    data = {}
    data['name'] = expect_input("Nombre de cock ", " ")
    data['category'] = expect_input("Categoria de color ", " ")
    data['gradient'] = bool_from_input("Tiene gradiente? ")
    return data