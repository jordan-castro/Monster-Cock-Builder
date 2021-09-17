from generator.image_gen import ImageGen
from generator.chicken_type import ChickenType
from generator.utils import clear
import time


def main():
    clear(ChickenType.COCK)
    clear(ChickenType.HEN)
    start = time.time()

    for x in range(25):
        gen = ImageGen(ChickenType.COCK)
        gen2 = ImageGen(ChickenType.HEN)
        gen2.draw()
        gen.draw()

    end = time.time()
    print(f"Tiempo tomado es {int(end - start)}")



# def random_color():
#     return (
#         random.randint(0, 255),
#         random.randint(0, 255),
#         random.randint(0, 255)
#     )


# def generate():
#     border_color = (0, 0, 0)
#     random_border = random_color()

#     body_color = (249, 249, 249)
#     random_body = random_color()

#     eye_color = (64, 0, 64)
#     random_eye = random_color()

#     thingy_color = (186, 69, 69)
#     ranodm_thingy = random_color()

#     nose_color = (255, 174, 201)
#     random_nose = random_color()

#     wing_color = (136, 0, 21)
#     random_wing = random_color()

#     feet_color1 = (255, 127, 39)
#     random_feet_color1 = random_color()

#     feet_color2 = (185, 74, 0)
#     darker_color = (
#         int(random_feet_color1[0] * 0.75),
#         int(random_feet_color1[1] * 0.75),
#         int(random_feet_color1[2] * 0.75),
#     )

#     before = [border_color, body_color, eye_color, thingy_color,
#               nose_color, wing_color, feet_color1, feet_color2]
#     after = [random_border, random_body, random_eye, ranodm_thingy,
#              random_nose, random_wing, random_feet_color1, darker_color]

#     random_bckg = random_color()

#     while random_bckg in after:
#         random_bckg = random_color()

#     image = Image.open("hen_base.png")
#     # Busca los pixels del imagen
#     pixels = image.getdata()
#     new_pxls = []

#     for pixel in pixels:
#         p = (pixel[0], pixel[1], pixel[2])
#         # Chequea si el pixel esta en la lista de colors para escuchar por
#         if p in before:
#             # Busca el index de desupes sobre el anter
#             p = after[before.index(p)]
#         elif p == (255, 255, 255):
#             p = random_bckg

#         new_pxls.append(p)

#     # Crea y guarda el nuevo imagen
#     new_image = Image.new("RGB", image.size)
#     new_image.putdata(new_pxls)

#     # Toma el numero de imagenes
#     amount_of_cocks = glob.glob('*.png')
#     image_path = f"hen_base{len(amount_of_cocks)}.png"

#     mod = len(amount_of_cocks) % 10000
#     res = random.randint(mod, mod + 10)

#     # spot(new_image)

#     if res % 10 == 0:
#         ImageOps.mirror(new_image).save(image_path)
#     else:
#         new_image.save(image_path)


# def spot(image):
#     """
#     Dibuja unos "spots" en el background del MCK.
#     """
#     drawing = ImageDraw.Draw(image)
#     # El sizeo del imagen
#     width, height = image.size
#     amount = random.randint(10, width)
#     drawn = 0
#     # shape = random.randint()

#     # El cuerpo del pollo
#     chicken_body_start_x = 291
#     chicken_body_end_x = 575
#     chicken_x = []
#     for x in range(chicken_body_start_x, chicken_body_end_x):
#         chicken_x.append(x)
    
#     chicken_body_start_y = 41
#     chicken_body_end_y = 415
#     chicken_y = []
#     for y in range(chicken_body_start_y, chicken_body_end_y):
#         chicken_y.append(y)

#     while drawn < amount:
#         x1 = random.randint(0, width)
#         x2 = x1 + 5
#         y1 = random.randint(0, height)
#         y2 = y1 + 5

#         # Para que no se toca el pollo
#         while (x1 in chicken_x or x2 in chicken_x):
#             x1 = random.randint(0, width)
#             x2 = x1 + 5
#         # Decide si tienen color o no
#         has_fill = (random.randint(drawn, amount + 10) % 5 > 0)
#         has_outline = (random.randint(-amount, drawn) % 20 > 1)

#         if has_fill:
#             fill = random_color()
#         else:
#             fill = None
        
#         if has_outline:
#             out = random_color()
#         else:
#             out = None

#         # Solo dibujamos si tiene colores de los dos
#         if has_outline and has_fill:
#             drawing.ellipse((x1,y1,x2,y2), fill=fill, outline=out)
#         drawn += 1



# def clear():
#     pngs = glob.glob("*.png")
#     jpgs = glob.glob("*.jpg")
#     for png in pngs:
#         if not png == "hen_base.png":
#             # Borrar
#             os.unlink(png)
#     for jpg in jpgs:
#         if not jpg == "hen_base.jpg":
#             os.unlink(jpg)


if __name__ == "__main__":
    main()
