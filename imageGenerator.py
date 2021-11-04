from PIL import Image, ImageDraw, ImageFont

import os


def generateThumbnail(folder, filename, text, x, y, textConfig, outname):
    img = Image.open("sample_in.jpg")

    # get an image
    with Image.open(os.path.join(folder, filename)).convert("RGB") as base:
        draw = ImageDraw.Draw(img)

        font = ImageFont.truetype(
            "fonts/Cairo-Regular.ttf", textConfig.get("textSize", 72)
        )

        # draw.text((x, y),"Sample Text",(r,g,b))
        draw.text(
            x,
            y,
            text,
            textConfig.get("textColor", "#000"),
            font=font,
            align=textConfig.get("textAlign", "left"),
        )
        img.save("sample-out.jpg")


if __name__ == "__main__":
    generateThumbnail("generated", "test.jpg", "HOI", 0, 0, {}, "test_2.jpg")
