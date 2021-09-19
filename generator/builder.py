from generator.uploader.blockchain_con import Minter
import json
from generator.attributes.attribute_builder import AttributesBuilder
from generator.random_data import randomify
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

    attributes = [
        Attribute.NINJA,
        Attribute.SUN,
        Attribute.AURA
    ]

    data = []
    minter = Minter()

    for x in range(1):
        first_range = randomify(range(-10, 10))
        second_range = randomify(range(-10, 10))

        if first_range > 0 and second_range > 10:
            ch_attr = attributes[first_range % 3:second_range % 3]
        else:
            ch_attr = []

        gen = ImageGen(ChickenType.COCK, [Attribute.SUN])
        mck = gen.draw()

        # data.append({f'attribute for {mck}': AttributesBuilder.pretty_attributes(gen.color_data, gen.attributes)})

        uploader = Uploader(
            gen.chicken_type, 
            mck, 
            AttributesBuilder.pretty_attributes(gen.color_data, gen.attributes)
        )
        _hash = uploader.upload()
        data.append({'hash': _hash, 'url': ipfs_url(_hash)})
        res = minter.mint(_hash)
        print(f"Resulta para min {_hash} es {res}")


    with open("test.json", "w") as test:
        json.dump(data, test)

    end = time.time()
    print(f"Tiempo tomado es {int(end - start)}")


if __name__ == "__main__":
    main()
