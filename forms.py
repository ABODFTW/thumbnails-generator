import json

from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField, FileRequired

# Schema
from schema import And, Schema
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, ValidationError

textCords_Schema = Schema({"x": int, "y": int, "w": int, "h": int})
textConfig_Schema = Schema(
    {
        "textSize": And(str, lambda n: 8 <= int(n) <= 256 and n.isdigit()),
        "textColor": str,
        "textDir": lambda i: i in ["rtl", "ltr"],
        "textAlign": lambda i: i in ["left", "center", "right"],
    }
)
text_Schema = Schema(And({"sentences": [str]}, lambda a: len(a.get("sentences")) > 0))


class ThumbnailDesignForm(FlaskForm):
    # Image upload
    imageInput = FileField(
        "Design Template",
        validators=[
            FileAllowed(["png", "jpg", "jpeg"], "Images only!"),
        ],
    )
    fontFile = FileField(
        "Font file (Optional)",
        validators=[
            FileAllowed(["ttf"], "TTF fonts only!"),
        ],
    )
    # Json object with x,y and w
    textCords = TextAreaField(validators=[DataRequired()])
    # A JSON object for text config
    textConfig = TextAreaField(validators=[DataRequired()])
    # A JSON objects {"sentences": []}
    text = TextAreaField(validators=[DataRequired()])

    def validate_textCords(form, field):
        cords = json.loads(field.data)

        if textCords_Schema.is_valid(cords):
            textCords_Schema.validate(cords)
            return 123
        else:
            raise ValidationError("Text cords field has invalid data.")

    def validate_textConfig(form, field):
        config = json.loads(field.data)

        if textConfig_Schema.is_valid(config):
            textConfig_Schema.validate(config)
        else:
            raise ValidationError("Text Config field has invalid data.")

    # def validate_text(form, field):
    #     text = json.loads(field.data)

    #     if text_Schema.is_valid(text):
    #         text_Schema.validate(text)
    #     else:
    #         raise ValidationError("Text field has invalid data.")
