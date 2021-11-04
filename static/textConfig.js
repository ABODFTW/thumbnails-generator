textConfigJSON = document.getElementById("textConfig")

closeModalbtn = document.getElementById("closeModalbtn")

textSizeRange = document.getElementById("textSize")
textSizeLabel = document.getElementById("textSizeLabel")

textAlignment = document.getElementsByName("alignbtn")
textColor = document.getElementById("color")

textConfig = {
    "textSize": null,
    "textAlign": null,
    "textDir": null,
    "textColor": null,
}

function updateTextConfig() {
    textConfig.textSize = textSizeRange.value
    textConfig.textAlign = document.querySelector('input[name="alignbtn"]:checked').value
    textConfig.textDir = document.querySelector('input[name="dirbtn"]:checked').value
    textConfig.textColor = textColor.value


    textConfigJSON.textContent = JSON.stringify(textConfig)
}

closeModalbtn.addEventListener("click", (e) => {
    updateTextConfig()
})

// Show text size to user
window.addEventListener('DOMContentLoaded', function () {
    updateTextConfig()
    textSizeRange.addEventListener("input", (event) => {
        value = event.target.value;
        textSizeLabel.innerText = value
    })
})

