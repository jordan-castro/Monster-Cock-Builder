import os
from generator.uploader.blockchain_con import Minter
from generator.attributes.attribute_builder import AttributesBuilder
from generator.random_data import randomifyattributes
from generator.attributes.attributes import Attribute
from generator.image_gen import ImageGen
from generator.chicken_type import ChickenType
from generator.uploader.upload import Uploader
import time
import optparse

from generator.utils import read_hashes, save_hash


def generator(amount):
    start = time.time()
    for x in range(amount):
        print(f"Generating --- {x} de {amount}")
        # Abre el class de generation
        gen = ImageGen(ChickenType.DETAILED_COCK, x, randomifyattributes(Attribute.GEN_0))
        mck = gen.draw()
        
        # Uploaderlo
        uploader = Uploader(
            gen.chicken_type,
            mck,
            AttributesBuilder.pretty_attributes(gen.color_data, gen.attributes)
        )
        # Busca hash
        _hash = uploader.upload()
        # Chequea que hash es falso
        if not _hash:
            print(f"Una problema con {mck} borrando...")
            os.unlink(mck + ".png")
            continue
        # Guarda hash
        save_hash(_hash)
    # Busca cuando se termino
    end = time.time()
    print(f"Tiempo tomado para {amount} fue {int(end - start)} segundos")


def minter():
    # Pregunta para su llave
    public = input("Que es tu llave publico ")
    private = input("Que es tu private key ")
    # Crea el minter
    minter = Minter(public, private)
    # Busca los hashes
    hashes = read_hashes()
    # Ahora pon lo en el smart contract
    for _hash in hashes:
        # Busca el current cada vez
        print(f"Currentamente {minter.most_recent()}")

        res = minter.mint(_hash)
        if not res:
            print(f"Suggestion de compiler!!! {_hash}")
            break
        else:
            print(f"Successo!! para hash {_hash}")
        print(f"Currentamente ahora es {minter.most_recent()}")

def main():
    parser = optparse.OptionParser('usage %prog -m' + 'Method')
    parser.add_option('-m', dest='method', type='string', help='specify the method to run.\nmint o generate')

    options, args = parser.parse_args()
    method = options.method

    if not method:
        print("No pasaste un method...")
        exit()
    
    if method.lower() == "generate":
        amount = input("Cuantos vamos a generar? ")
        generator(int(amount))
    elif method.lower() == "mint":
        minter()
    else:
        print(f"El metodo {method} no existe...")
        exit()

if __name__ == "__main__":
    main()