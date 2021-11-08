img = document.getElementById("design")
imgInput = document.getElementById("imageInput")


// Setting up selecting on image
window.addEventListener('DOMContentLoaded', function () {
    const textCords = document.querySelector('#textCords');
    const cropper = new Cropper(img, {
        viewMode: 3,
        zoomable: false,

        crop: function (event) {
            let width = event.detail.width;
            let height = event.detail.height;

            cropper.setData({
                width: width,
                height: height,
            });
        },
    });

    // Add event listener to load the image once selected on the file input
    imgInput.onchange = evt => {
        const [file] = imgInput.files
        // limit files to 5mb
        if (file.size > 5242880) {
            alert("File is too big!")
            evt.target.value = ""
            cropper.replace("/static/image.jpg")
        };

        if (file && evt.target.value) {
            cropper.replace(URL.createObjectURL(file));
        }
    }
    // Update textarea that will be submitted to the server
    ["ready", "cropmove"].forEach(evt =>
        img.addEventListener(evt, (e) => {
            let content = cropper.getData(true)
            console.log(content)
            content = JSON.stringify({
                "x": content.x,
                "y": content.y,
                "w": content.width,
                "h": content.height
            })
            textCords.textContent = content

        })
    );
});