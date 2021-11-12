import sys
import os
import shutil
from pathlib import Path
import uuid
import json
import zipfile
from io import BytesIO

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

from forms import ThumbnailDesignForm

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
            try:
                file = form.imageInput.data
                uploaded_filename = form.imageInput.data.filename
                uploaded_filename = secure_filename(uploaded_filename)
                uploaded_filename = str(uuid.uuid4()) + uploaded_filename
                # Save uploaded image
                Path(UPLOAD_FOLDER).mkdir(parents=True, exist_ok=True)
                file.save(os.path.join(UPLOAD_FOLDER, uploaded_filename))
            except AttributeError:
                default_image = "image.jpg"
                Path(UPLOAD_FOLDER).mkdir(parents=True, exist_ok=True)

                shutil.copyfile(
                    f"static/{default_image}",
                    os.path.join(UPLOAD_FOLDER, default_image),
                )
                uploaded_filename = default_image

            texts = json.loads(form.text.data).get("sentences")

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
                )
                if response:
                    generated_images.append(outname)
                    # Return url to the generated image
                    # return url_for("get_preview", subdirectory=subdirectory, name=outname)
            memory_file = BytesIO()
            with zipfile.ZipFile(memory_file, "w") as zf:
                for filename in generated_images:
                    filepath = os.path.join(directory, filename)
                    data = zipfile.ZipInfo(filepath)
                    data.compress_type = zipfile.ZIP_DEFLATED
                    zf.write(filepath)
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
            try:
                file = form.imageInput.data
                uploaded_filename = form.imageInput.data.filename
                uploaded_filename = secure_filename(uploaded_filename)
                uploaded_filename = str(uuid.uuid4()) + uploaded_filename
                # Save uploaded image
                Path(UPLOAD_FOLDER).mkdir(parents=True, exist_ok=True)
                file.save(os.path.join(UPLOAD_FOLDER, uploaded_filename))
            except AttributeError:
                default_image = "image.jpg"
                Path(UPLOAD_FOLDER).mkdir(parents=True, exist_ok=True)

                shutil.copyfile(
                    f"static/{default_image}",
                    os.path.join(UPLOAD_FOLDER, default_image),
                )
                uploaded_filename = default_image

            texts = json.loads(form.text.data).get("sentences")

            text_cords = json.loads(form.textCords.data)
            x = (text_cords.get("w") / 2) + text_cords.get("x")
            y = (text_cords.get("h") / 2) + text_cords.get("y")
            width = text_cords.get("w")

            textConfig = json.loads(form.textConfig.data)

            subdirectory = str(uuid.uuid4())
            directory = os.path.join(GENERATED_IMAGE_FOLDER, subdirectory)

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
                )
                if response:
                    # Return url to the generated image
                    return url_for(
                        "get_preview", subdirectory=subdirectory, name=outname
                    )


@app.route("/fonts")
def get_fonts():
    fonts = os.listdir("fonts")
    fonts_names = map(lambda x: x.replace("-", " ").split(".")[0], fonts)
    return "<br> ".join(fonts_names)
