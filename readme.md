# Thumbnails Generator

#### Video Demo: https://youtu.be/y94a_UDVPcg

#### Description:

One template, multiple designs, the idea of the project sparked me when I tried
to create YouTube thumbnails for my playlists, Usually I create the same design
for each episode the only thing that changes, is the title and episode number,
and based on this idea I started this project, it's not yet optimal, but it's
functioning.

##### Project files

This project used multiple programming languages, Python, JavaScript, CSS and
HTML.

Python files: app.py, forms.py and imageGenerator.py

app.py is the main file, it has everything flask related, routes, and the whole
logic.

forms.py only has the form class, because wtflask and flask-wtf were used in
this project to minimize redundancies code on forms validation.

imageGenerator.py has all the code needed to generate the images with the text
using PIL library

template/html files, there is only one html file in templates, I did my best to
make this a SPA, so it required more javascript code than normal.

JavaScript files: there are 4 js files, located in the 'static' folder,
addSentence.js, index.js, previewDesign.js and textConfig.js.

addSentence.js has the logic for adding a new sentence to the data list, it also
override the default action for the enter button.

index.js has all the code for updating the image editor on the right side of the
page based on what the user uploaded.

previewDesign.js has all the logic for submitting a form via Ajax to generate
one design for preview.

textConfig.js has all the code for the text config modal and all the config
needed to keep it in sync as the user changes them.

I also used a couple of external JavaScript code, Bootstrap and cropper.

Bootstrap was used mainly for styling but also their modals came in handy for
the text configuration modal, and used cropper to be able to locate pixels on
the image of the user want the text to placed on.

Styling: there is only one css file in static, 'style.css', Also bootstrap
swatch was used to give it a different look than the default bootstrap.

#### Features

1. Ability to generate multiple images with one design
2. Customizable font size, color and alignment
3. Support for RTL, and LTR languages like Arabic, and English
4. Ability to chose where to add the text
5. Supports multiline text if text box width was less than the text width.
6. Preview button that allows you to look at the design before generating all
   images.

#### Engineering Decisions

- Using Python for the project was one of the best, as PIL library is really
  customizable and helped me achieve all functions needed.
- I decided to have the web app as an SPA, as this is more of an app than a
  normal website, this required more javascript code, but it was anticipated, I
  could've used a frontend language like VueJS or reactJS but I decided to only
  use vanilla javascript to keep the loading speed fast.
- Design could've been better but I'm glad I used bootstrap, because when I
  decided to make it responsive it was east and straightforward.
- Initially the forms were validated on the views, after looking up for a better
  way wtforms seems to be much better and separate the concerns and helps with
  extending the software further though my decision to store the config, data
  list as a JSON into a textarea required a custom validation using schema.
- If I were to develop this further a lot of things would change, and more
  abstraction would've been needed, i.e javascript vanilla might've be a good
  choice for now, but later a frontend framework would be needed.
- A lot of the code in preview route and the generate route is similar and it
  could've been abstracted into it's own function.

### Future vision

1. Add CSV file upload for data list
2. Add Loaders when loading images
3. Supplement multiple demo images
4. Make the landing page image an info graphic of the service
5. Implement a registration and credit system
6. Add custom fonts support
7. Add emailing images feature and process the images on a background worker
