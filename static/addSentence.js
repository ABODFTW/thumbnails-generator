window.addEventListener('DOMContentLoaded', function () {
    sentenceInput = document.getElementById("sentenceInput")
    dataList = document.getElementById("text")
    addSentence = document.getElementById("addSentence")
    sentencesList = document.getElementById("sentencesList")

    sentences = []

    addSentence.addEventListener("click", (e) => {
        sentence = sentenceInput.value
        console.log(sentence)
        sentences.push(sentence)
        dataList.textContent = JSON.stringify({ "sentences": sentences })
        sentencesList.innerHTML += `<div class='item'><span>${sentence}</span></div>`
        sentenceInput.value = ""
    })
})