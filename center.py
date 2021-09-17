from PIL import Image, ImageDraw


def main():
    # Hacemos center
    center("only.png", "centered_cock.png", (884, 475))


def center(source, output, size):
    image = Image.open(source)
    bckg = Image.new('RGB', size, (255, 255, 255))

    x = int(((bckg.size[0] / 2) - (image.size[0] / 2))) - 25
    y = int((bckg.size[1] / 2) - (image.size[1] / 2))
    
    bckg.paste(image, (x, y))
    bckg.save(output)


if __name__ == "__main__":
    main()
