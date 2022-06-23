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

    document.querySelector('#deleteAll').addEventListener('click', function (e) {
        dataList.textContent = JSON.stringify({ "sentences": [] })
        sentencesList.innerHTML = ""
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
            </div>`
            sentenceInput.value = ""


            items = document.querySelectorAll(".text-item > a")
            items.forEach(i => {
                i.addEventListener("click", e => {
                    console.log(e.target.textContent)
                    console.log("Sentence to be deleted, ", sentence)
                    // Remove from list
                    const deletedItem = sentences.splice(sentences.indexOf(sentence), 1)
                    dataList.textContent = JSON.stringify({ "sentences": sentences })
                    e.target.parentNode.remove()
                    alert(`Deleted item: ${deletedItem}`)
                })
            })
        }
    }
})