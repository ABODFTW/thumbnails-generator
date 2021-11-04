from PIL import Image, ImageDraw, ImageFont

import os


def generateThumbnail(folder, filename, text, x, y, textConfig, outdirectory, outname):

    # get an image
    with Image.open(os.path.join(folder, filename)).convert("RGB") as base:
        draw = ImageDraw.Draw(base)

        font = ImageFont.truetype(
            "fonts/Cairo-Regular.ttf", textConfig.get("textSize", 72)
        )

        draw.text(
            (x, y),
            text,
            fill=textConfig.get("textColor", "#000"),
            font=font,
            align=textConfig.get("textAlign", "left"),
            direction=textConfig.get("textDir", "ltr"),
        )
        base.save(os.path.join(outdirectory, outname), "JPEG")


if __name__ == "__main__":
    generateThumbnail(
        "uploads",
        "image.jpg",
        "HETE!!",
        0,
        0,
        {"textSize": 200, "textAlign": "center", "textDir": "rtl"},
        "generated",
        "test_2.jpg",
    )
