from PIL import Image, ImageDraw, ImageFont

import os


def split_text_to_match_boxsize(draw, text, width, font):
    """
    Paramaters
    text:
    width:
    Returns the same text with line breakers with-in the limits of the width
    """
    words = text.split(" ")
    wrappedtext = []
    line_width = 0
    for word in words:
        word = word + " "
        # word_width = draw.textbbox((0, 0), word, font=font, anchor="mm")[2]
        word_width = round(draw.textlength("Hello", font))
        if (line_width + word_width) > width:
            wrappedtext.append("\n")
            wrappedtext.append(word)
            line_width = 0
        else:
            line_width += word_width
            wrappedtext.append(word)
    return "".join(wrappedtext)


def generateThumbnail(
    folder, filename, text, x, y, width, textConfig, outdirectory, outname, font_path
):
    # get an image
    with Image.open(os.path.join(folder, filename)).convert("RGB") as base:
        draw = ImageDraw.Draw(base)

        font = ImageFont.truetype(
            font_path, int(textConfig.get("textSize", "72"))
        )
        text = split_text_to_match_boxsize(draw, text, width, font)
        draw.text(
            (x, y),
            text,
            fill=textConfig.get("textColor", "#000"),
            font=font,
            anchor="mm",
            align=textConfig.get("textAlign", "left"),
            direction=textConfig.get("textDir", "ltr"),
        )
        base.save(os.path.join(outdirectory, outname), "JPEG")
        return True


if __name__ == "__main__":
    generateThumbnail(
        "uploads",
        "image.jpg",
        "HETE!!\n another line\n sadafa",
        0,
        0,
        {"textSize": 200, "textAlign": "right", "textDir": "rtl"},
        "generated",
        "test_2.jpg",
    )
