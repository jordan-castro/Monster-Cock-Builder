from enum import Enum
from generator.utils import expect_input


class ChickenType(Enum):
    DETAILED_COCK = 0
    HEN = 1
    CHICK = 2
    SOLONA_COCK = 3    


def ask_for_type()->ChickenType: 
    """
    Pregunta para el tipo de pollo estamos generando.
    
    Returns: <ChickenType>
    """
    c_type = expect_input("Chicken Type: \n(0 => Detailed Cock) \n(1 => Hen) \n(2 => Chick) \n(3 => Soloana Cock) \n[x]: ", 2)
    match c_type:
        case 0:
            return ChickenType.DETAILED_COCK
        case 1:
            return ChickenType.HEN
        case 2:
            return ChickenType.CHICK
        case 3:
            return ChickenType.SOLONA_COCK
        case _:
            raise("No pasaste una forma correcta!")