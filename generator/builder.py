from generator.uploader.blockchain_con import Minter
import json
from generator.attributes.attribute_builder import AttributesBuilder
from generator.random_data import randomify, randomifyattributes
from generator.attributes.attributes import Attribute
from generator.image_gen import ImageGen
from generator.chicken_type import ChickenType
from generator.utils import clear, ipfs_url
from generator.uploader.upload import Uploader
import time


def main():
    # clear(ChickenType.COCK)
    # clear(ChickenType.HEN)
    start = time.time()

    data = []
    minter = Minter()

    for x in range(3):
        gen = ImageGen(ChickenType.COCK, randomifyattributes(Attribute.GEN_0))
        mck = gen.draw()
        print(mck)

        # data.append({f'attribute for {mck}': AttributesBuilder.pretty_attributes(gen.color_data, gen.attributes)})

        # uploader = Uploader(
        #     gen.chicken_type, 
        #     mck, 
        #     AttributesBuilder.pretty_attributes(gen.color_data, gen.attributes)
        # )
        # _hash = uploader.upload()
        # data.append({'hash': _hash, 'url': ipfs_url(_hash)})
        # res = minter.mint(_hash)
        # print(f"Resulta para min {_hash} es {res}")


    with open("test.json", "w") as test:
        json.dump(data, test)

    end = time.time()
    print(f"Tiempo tomado es {int(end - start)}")


if __name__ == "__main__":
    main()
