import json
import os
import pathlib
import shutil
import sys
import uuid
import zipfile
from io import BytesIO
from pathlib import Path

from flask import (Flask, flash, redirect, render_template, request, send_file,
                   send_from_directory, url_for)
from werkzeug.utils import secure_filename

from forms import ThumbnailDesignForm
from imageGenerator import generateThumbnail

# Config
app = Flask(__name__)
app.config["SECRET_KEY"] = "9ecf977e-cb16-4e6e-91dd-9a1cbb3e9e2b"
app.config["MAX_CONTENT_LENGTH"] = 5 * 1000 * 1000
app.config["TEMPLATES_AUTO_RELOAD"] = True
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

UPLOAD_FOLDER = "uploads"
TMP_FONTS_FOLDER = "tmp_fonts"
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
    form = ThumbnailDesignForm()
    return render_template("index.html", form=form)


@app.route("/generated/<subdirectory>/<name>")
def get_preview(subdirectory, name):
    filename = os.path.join(subdirectory, name)
    return send_from_directory(GENERATED_IMAGE_FOLDER, filename)


@app.route("/generate", methods=["POST"])
def generate_images_zip():
    if request.method == "POST":
        form = ThumbnailDesignForm()

        if form.validate_on_submit():
            Path(UPLOAD_FOLDER).mkdir(parents=True, exist_ok=True)
            Path(TMP_FONTS_FOLDER).mkdir(parents=True, exist_ok=True)


            try:
                print("Uploaded font filename: ")
                print(form.fontFile.data.filename)

                # Save uploaded font file
                font_file = form.fontFile.data
                uploaded_font_filename = form.fontFile.data.filename
                uploaded_font_filename = secure_filename(uploaded_font_filename)
                uploaded_font_filename = str(uuid.uuid4()) + uploaded_font_filename

                uploaded_font_path = os.path.join(TMP_FONTS_FOLDER, uploaded_font_filename)
                # Save uploaded image
                font_file.save(uploaded_font_path)
            except AttributeError:
                uploaded_font_path = "fonts/Cairo-Regular.ttf"

            try:
                file = form.imageInput.data
                uploaded_filename = form.imageInput.data.filename
                uploaded_filename = secure_filename(uploaded_filename)
                uploaded_filename = str(uuid.uuid4()) + uploaded_filename
                # Save uploaded image
                file.save(os.path.join(UPLOAD_FOLDER, uploaded_filename))
            except AttributeError:
                default_image = "image.jpg"

                shutil.copyfile(
                    f"static/{default_image}",
                    os.path.join(UPLOAD_FOLDER, default_image),
                )
                uploaded_filename = default_image

            texts = form.text.data.split("\n")

            texts = [sentence.strip() for sentence in texts]

            text_cords = json.loads(form.textCords.data)
            x = (text_cords.get("w") / 2) + text_cords.get("x")
            y = (text_cords.get("h") / 2) + text_cords.get("y")
            width = text_cords.get("w")

            textConfig = json.loads(form.textConfig.data)

            subdirectory = str(uuid.uuid4())
            directory = os.path.join(GENERATED_IMAGE_FOLDER, subdirectory)

            generated_images = []

            for text in texts:

                # Generate image with text
                outname = text.replace(" ", "_") + "_" + uploaded_filename

                Path(directory).mkdir(parents=True, exist_ok=True)

                response = generateThumbnail(
                    UPLOAD_FOLDER,
                    uploaded_filename,
                    text,
                    x,
                    y,
                    width,
                    textConfig,
                    directory,
                    outname,
                    uploaded_font_path
                )
                if response:
                    generated_images.append(outname)
                    # Return url to the generated image
                    # return url_for("get_preview", subdirectory=subdirectory, name=outname)
            memory_file = BytesIO()
            with zipfile.ZipFile(memory_file, "w") as zf:
                generated_images_folder = pathlib.Path(directory)
                for file_path in generated_images_folder.iterdir():
                    zf.write(file_path, file_path.relative_to(directory))
                # for filename in generated_images:
                #     filepath = os.path.join(directory, filename)
                #     data = zipfile.ZipInfo(filepath)
                #     data.compress_type = zipfile.ZIP_DEFLATED
                #     zf.write(filepath)
            memory_file.seek(0)
            return send_file(
                memory_file,
                attachment_filename="{}.zip".format(subdirectory),
                as_attachment=True,
            )
        else:
            for fieldName, errorMessages in form.errors.items():
                for err in errorMessages:
                    flash(err, "danger")
            return redirect("/")


@app.route("/preview", methods=["POST"])
def preview_image():
    if request.method == "POST":
        form = ThumbnailDesignForm()

        if form.validate_on_submit():

            # Create UPLOAD folder if doesn't exist
            Path(UPLOAD_FOLDER).mkdir(parents=True, exist_ok=True)
            Path(TMP_FONTS_FOLDER).mkdir(parents=True, exist_ok=True)

            try:
                print("Uploaded font filename: ")
                print(form.fontFile.data.filename)

                # Save uploaded font file
                font_file = form.fontFile.data
                uploaded_font_filename = form.fontFile.data.filename
                uploaded_font_filename = secure_filename(uploaded_font_filename)
                uploaded_font_filename = str(uuid.uuid4()) + uploaded_font_filename

                uploaded_font_path = os.path.join(TMP_FONTS_FOLDER, uploaded_font_filename)
                # Save uploaded image
                font_file.save(uploaded_font_path)
            except AttributeError:
                uploaded_font_path = "fonts/Cairo-Regular.ttf"

            try:
                file = form.imageInput.data
                uploaded_filename = form.imageInput.data.filename
                uploaded_filename = secure_filename(uploaded_filename)
                uploaded_filename = str(uuid.uuid4()) + uploaded_filename
                # Save uploaded image
                file.save(os.path.join(UPLOAD_FOLDER, uploaded_filename))
            except AttributeError:
                default_image = "image.jpg"
                # To be able to access the fallback image as if it was uploaded by user
                shutil.copyfile(
                    f"static/{default_image}",
                    os.path.join(UPLOAD_FOLDER, default_image),
                )
                uploaded_filename = default_image

            texts = form.text.data.split("\n")

            texts = [sentence.strip() for sentence in texts]

            text_cords = json.loads(form.textCords.data)
            x = (text_cords.get("w") / 2) + text_cords.get("x")
            y = (text_cords.get("h") / 2) + text_cords.get("y")
            width = text_cords.get("w")

            textConfig = json.loads(form.textConfig.data)

            subdirectory = str(uuid.uuid4())
            directory = os.path.join(GENERATED_IMAGE_FOLDER, subdirectory)
            outname = texts[0].replace(" ", "_") + "_" + uploaded_filename

            Path(directory).mkdir(parents=True, exist_ok=True)

            response = generateThumbnail(
                UPLOAD_FOLDER,
                uploaded_filename,
                texts[0],
                x,
                y,
                width,
                textConfig,
                directory,
                outname,
                uploaded_font_path
            )
            if response:
                # Return url to the generated image
                return url_for("get_preview", subdirectory=subdirectory, name=outname)
        else:
            flash("Invalid form")
            return redirect("/")


@app.route("/fonts")
def get_fonts():
    fonts = os.listdir("fonts")
    fonts_names = map(lambda x: x.replace("-", " ").split(".")[0], fonts)
    return "<br> ".join(fonts_names)
