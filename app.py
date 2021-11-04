import sys
import os
from pathlib import Path
import uuid
import json

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    send_from_directory,
    send_file,
)
from werkzeug.utils import secure_filename

from imageGenerator import generateThumbnail
from helpers import allowed_file

# Config
app = Flask(__name__)
app.config["SECRET_KEY"] = "9ecf977e-cb16-4e6e-91dd-9a1cbb3e9e2b"
app.config["MAX_CONTENT_LENGTH"] = 5 * 1000 * 1000
app.config["TEMPLATES_AUTO_RELOAD"] = True
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

UPLOAD_FOLDER = "uploads"
GENERATED_IMAGE_FOLDER = "generated"

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/generated/<name>")
def download_image(name):
    return send_from_directory(GENERATED_IMAGE_FOLDER, name)


@app.route("/generate", methods=["POST"])
def generate_images():
    if request.method == "POST":
        file = request.files["image"]

        if "image" not in request.files:
            uploaded_filename = "image.jpg"

        if file.filename != "":
            uploaded_filename = file.filename
            uploaded_filename = secure_filename(uploaded_filename)
            uploaded_filename = str(uuid.uuid4()) + uploaded_filename
            # Save uploaded image
            file.save(os.path.join(UPLOAD_FOLDER, uploaded_filename))
        else:
            uploaded_filename = "image.jpg"

        if allowed_file(uploaded_filename, ALLOWED_EXTENSIONS):

            text_cords = request.form.get("textCords", "")
            texts = json.loads(request.form.get("text", "")).get("sentences")
            x = json.loads(text_cords).get("x")
            y = json.loads(text_cords).get("y")
            width = json.loads(text_cords).get("w")
            textConfig = json.loads(request.form.get("textConfig"))

            generated_images = []

            for text in texts:

                # Generate image with text
                outname = text.split()[0].replace(" ", "_") + "_" + uploaded_filename
                directory = os.path.join(str(uuid.uuid4()), GENERATED_IMAGE_FOLDER)

                Path(directory).mkdir(parents=True, exist_ok=True)

                generateThumbnail(
                    UPLOAD_FOLDER,
                    uploaded_filename,
                    text,
                    x,
                    y,
                    width,
                    textConfig,
                    directory,
                    outname,
                )
                generated_images.append(outname)

            # Return url to the image with text
            return url_for("download_image", name=outname)


@app.route("/fonts")
def get_fonts():
    fonts = os.listdir("fonts")
    fonts_names = map(lambda x: x.replace("-", " ").split(".")[0], fonts)
    return "<br> ".join(fonts_names)
