window.addEventListener('DOMContentLoaded', function () {

    sentenceInput = document.getElementById("sentenceInput")
    dataList = document.getElementById("text")
    sentencesList = document.getElementById("sentencesList")
    addSentence = document.getElementById("addSentence")

    sentences = []

    document.querySelector('#sentenceInput').addEventListener('keypress', function (e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            addItem()
        }
    });


    addSentence.addEventListener("click", (e) => {
        addItem()
    })

    function addItem() {
        sentence = sentenceInput.value
        if (sentence !== "") {
            sentences.push(sentence)
            dataList.textContent = JSON.stringify({ "sentences": sentences })
            sentencesList.innerHTML += `
            <div class='p-2 mb-2 block text-item'>
            <span>${sentence}</span>
            <a href="#" style="float:right; margin-right:5px; text-decoration: none;">X</a>
            </div>`
            sentenceInput.value = ""


            items = document.querySelectorAll(".text-item > a")
            items.forEach(i => {
                i.addEventListener("click", e => {
                    // Remove from list
                    sentences.pop(sentences.indexOf(sentence))
                    dataList.textContent = JSON.stringify({ "sentences": sentences })
                    e.target.parentNode.remove()
                    alert("Deleted!")
                })
            })
        }
    }
})