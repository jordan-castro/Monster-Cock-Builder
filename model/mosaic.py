"""
Create a mosaic of a image with a list of images in a directory.

Usage:
    mosaic.py -p <photo> -d <directory> -t <tile-size> -r <rename> -i <image_size>

    mosaic.py -h | --help
    mosaic.py --version

Options:
    -h --help          Show this screen.
    --version          Show version.
    -p <photo>         The path to the photo to creat a mosaic out of.
    -d <directory>     The directory of the tile images.
    -r <rename>        Rename the file or not. 1 for yes, 0 for no. Default is 1.
    -t <tile-size>     The size of the tile images.
    -i <image_size>    The size of the image, if not passed, then the image size will stay the same.
"""

import glob
from PIL import Image
from scipy import spatial
import numpy as np
import optparse


class Args:
    """
    Class para parse los arguments de la linea de comandos.
    """
    def __init__(self, args, description, version, prog, usage=None):
        self.args = args
        self.description = description
        self.parser = optparse.OptionParser(version=version, prog=prog, usage=usage or self.description)

    def _setup_args_(self):
        """
        Setup los argumentos sobre los args del clase.
        Por ejemplo:
        ```
        args = [
            {
                "name": "path",
                "short": "-p",
                "long": None
            },
            {
                "name": "directory",
                "short": "-d",
                "long": "--directory"
            },
            {
                "name": "width",
                "short": "-x",
                "long": None,
                "type": "int",
                "default": None
            }
        ]
        ```
        """
        for arg in self.args:
            # Chequea que estan los argumentos necesarios
            keys = arg.keys()
            if "name" not in keys:
                raise Exception("Argumento 'name' es requerido.")
            if "short" not in keys:
                raise Exception("Argumento 'short' es requerido.")

            name = arg["name"]
            short = arg["short"]
            long = arg["long"] if "long" in keys else None
            type = arg["type"] if "type" in keys else None
            default = arg["default"] if "default" in keys else None

            # Ponemos el argumento
            self.parser.add_option(short, long, dest=name, type=type, default=default)

    def parse(self):
        """
        Parse los argumentos.

        Returns:
            namedtuple: namedtuple con los argumentos.
        """
        self._setup_args_()
        (options, args) = self.parser.parse_args()
        # Loop los argumentos con optiones
        for arg in self.args:
            # Toma los llaves del dict
            keys = arg.keys()
            if "required" in keys:
                required = arg["required"]
                # Si esta required entonces, chequea que no es None. AKA, que no esta vacio.
                # Usando .__dict__ porque los self.args es un dict.
                if required and options.__dict__[arg["name"]] is None:
                    raise Exception("Argumento '{}' es requerido.".format(arg["name"]))
        
        return options


args = [
    {
        "name": "photo",
        "short": "-p",
        "long": "--photo",
        "required": True
    },
    {
        "name": "directory",
        "short": "-d",
        "long": "--directory",
        "default": "data/mainnet"
    },
    {
        "name": "rename",
        "short": "-r",
        "long": "--rename",
        "default": '0',
        "required": False
    },
    {
        "name": "tile_size",
        "short": "-t",
        "long": "--tile-size",
        "default": '50',
    },
    {
        "name": "image_size",
        "short": "-i",
        "long": "--image-size",
        "default": '0',
    }
]

cmd_args = Args(args, __doc__, version="0.1", prog="mosaic.py")
options = cmd_args.parse()

# Sources and settings
if __name__ == "__main__":
    main_photo_path = options.photo
    tile_photos_path = options.directory
    tile_size = (int(options.tile_size), int(options.tile_size))
    image_size = (int(options.image_size), int(options.image_size))
    if options.rename == '1':
        output_path = main_photo_path.split('.')[0] + '_mosaic_{}.png'.format(tile_size[0])
    else:
        output_path = main_photo_path

    # Get all tiles
    tile_paths = glob.glob(tile_photos_path + '/*.png')[1:]

    # Import and resize all tiles
    tiles = []
    for path in tile_paths:
        tile = Image.open(path)
        tile = tile.resize(tile_size)
        tiles.append(tile)

    # Calculate dominant color
    colors = []
    for tile in tiles:
        mean_color = np.array(tile).mean(axis=0).mean(axis=0)
        colors.append(mean_color)

    # Pixelate (resize) main photo
    main_photo = Image.open(main_photo_path)

    # If image_size is greater than 0 then resize to that
    if image_size[0] > 0:
        main_photo = main_photo.resize(image_size)

    width = int(np.round(main_photo.size[0] / tile_size[0]))
    height = int(np.round(main_photo.size[1] / tile_size[1]))

    resized_photo = main_photo.resize((width, height))

    # Find closest tile photo for every pixel
    tree = spatial.KDTree(colors)
    closest_tiles = np.zeros((width, height), dtype=np.uint32)

    for i in range(width):
        for j in range(height):
            closest = tree.query(resized_photo.getpixel((i, j)))
            closest_tiles[i, j] = closest[1]

    # Create an output image
    output = Image.new('RGB', main_photo.size)

    # Draw tiles
    for i in range(width):
        for j in range(height):
            # Offset of tile
            x, y = i*tile_size[0], j*tile_size[1]
            # Index of tile
            index = closest_tiles[i, j]
            # Draw tile
            output.paste(tiles[index], (x, y))

    # Save output
    output.save(output_path)
