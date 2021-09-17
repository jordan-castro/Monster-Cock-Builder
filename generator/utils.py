from generator.chicken_type import ChickenType
import glob
import os


def clear(chicken_type: ChickenType):
    """
    Hacemos clear a los files.
    """
    if chicken_type ==ChickenType.COCK:
        black = 'cock_base.png'
        find = 'cock'
    elif chicken_type == ChickenType.HEN:
        black = 'hen_base.png'
        find = 'hen'

    # Busca todos
    files = glob.glob('*png')
    # Loop
    for file in files:
        if find in file:
            if file != black:
                os.unlink(file)