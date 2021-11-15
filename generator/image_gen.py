from generator.attributes.canvas import get_canvas, create_image
from generator.finish import finishing_touches
from generator.utils import replace_pixels
from generator.attributes.attributes import Attribute
from generator.random_data import randomchoice, randomifyflip
from generator.chicken_type import ChickenType
from PIL import ImageOps
from generator.colors_data import Colors
from generator.names.read_names import get_random_name
import generator.tracker.tracker as t


class ImageGen:
    def __init__(self, chicken_type: ChickenType, id: int, attributes: list=None, custom_data: dict=None):
        self.chicken_type = chicken_type
        if custom_data:
            # Chequea si el nombre es random "Significa que queremos nombre random!"
            if custom_data['name'] == "random":
                self.name = get_random_name(id, chicken_type)
            else:
                t.tracker.name = custom_data['name']
                self.name = f"{custom_data['name']}_#{id}"
            if custom_data['gradient']:
                if not Attribute.GRADIENT_V in attributes and not Attribute.GRADIENT_H in attributes: 
                    attributes.append(
                      randomchoice([Attribute.GRADIENT_H, Attribute.GRADIENT_V])
                    )

        else:
            self.name = get_random_name(id, chicken_type)

        self.color_data = Colors(chicken_type, custom_data['category']) if custom_data else Colors(chicken_type)
        t.tracker.colors = self.color_data
        
        self.attributes = attributes
        
        self.id = id
        self.image = self.open()

    def decide_image(self):
        base = "base_art/"
        if self.chicken_type == ChickenType.HEN:
            return f"{base}hen_only.png"
        elif self.chicken_type == ChickenType.DETAILED_COCK:
            return f"{base}FinalCockHR.png"
        elif self.chicken_type == ChickenType.SOLONA_COCK:
            return f"{base}Rooster2_HighRes.png"
        else:
            return "Chick"

    def draw(self):
        """
        Dibuja un monster cock.
        """
        # Priemero tocamos los colores
        before = list(map(lambda c: c.before, self.color_data.colors))
        after = list(map(lambda c: c.after, self.color_data.colors))
        bckg = self.color_data.bckg

        # Dibuja!
        new_image = replace_pixels(self.image, after + [bckg], before + [(255,255,255)])

        flip = randomifyflip(self.id)

        if flip:
            self.attributes.append(Attribute.SUN_RISE_EAST)
            new_image = self.flip(new_image)
        else:
            self.attributes.append(Attribute.SUN_RISE_WEST)

        image_path = f"{self.name}.png"
        # Guarda la imagen ahora
        new_image.save(image_path)

        # ! If you are not james garfield then comment this line out
        # ! It is a user-specific method to track the progress of the generator outside of the app.
        new_image = finishing_touches(image_path)

        # El objecto de tracker para la data
        t.tracker.image = new_image
        t.tracker.id = self.id
        t.tracker.path = image_path

        return self.name

    def flip(self, image):
        """
        Flip el imagen.

        Params:     
            - <image: Image>
        """
        return ImageOps.mirror(image)

    def open(self):
        """
        Abre el photo de monster cock.

        Returns: <Image>
        """
        return create_image(self.decide_image(), get_canvas(self.attributes), self.attributes, self.color_data)