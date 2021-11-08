previewDesignBtn = document.getElementById("previewDesign");
designPreview = document.getElementById("designPreview")
form = document.getElementById("generateDesignForm")

window.addEventListener('DOMContentLoaded', function () {
    previewDesignBtn.addEventListener("click", () => {

        designPreview.src = "";
        data = new FormData(form)
        fetch("/preview",
            {
                body: data,
                method: "post"
            }).then((response) => {
                console.log(response);
                response.text().then((data) => {
                    designPreview.src = data;
                    console.log(data);
                });
            });
    })
});