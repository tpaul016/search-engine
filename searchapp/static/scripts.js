/*
* Inspired by:
* https://developers.google.com/web/updates/2015/03/introduction-to-fetch
* https://github.com/pallets/flask/blob/master/examples/javascript/js_example/templates/fetch.html
* https://dev.to/stephenafamo/how-to-create-an-autocomplete-input-with-plain-javascript
*/

// Bound to the inputQuery input
var spellDataList = document.getElementById('docList');

var divDocList = document.getElementById('docList');

var baseURL = "http://localhost:5000/"

/*
* Handle Query submission
* EventListener for query form
* Posts data and transforms documents to elements that are then
* appended to the docList div 
*/
function querySubmit(ev) {
    ev.preventDefault();
    fetch(baseURL + "docs", {
        method: 'POST',
        body: new FormData(this)
    })
    .then(response => {
        console.log("Query response received")
        return response.json();
    })
    .then(data => {
        // Clear list
        while (divDocList.hasChildNodes()) {
            divDocList.removeChild(divDocList.firstChild);
        }

        data.forEach(doc => {
            newDiv = document.createElement("div")
            newDiv.setAttribute("class", "doc")
            divDocList.appendChild(newDiv)

            aDocId = document.createElement("a")
            aDocId.setAttribute("href", baseURL + "docs/" + doc["docId"])
            aDocId.innerHTML = "DocId: " + doc["docId"]
            newDiv.appendChild(aDocId)

            pExcerpt = document.createElement("p")
            pExcerpt.innerHTML ="Description: " + doc["excerpt"]
            newDiv.appendChild(pExcerpt)

            pScore = document.createElement("p")
            pScore.innerHTML = "Score: " + doc["score"]
            newDiv.appendChild(pScore)
        })
    })
    .catch(error => {
        console.log("Query: Request failed", error)
    });
}

// Bind form to querySubmit()
var form = document.getElementById('query');
form.addEventListener('submit', querySubmit);

var spellDataList = document.getElementById('spellList');

/* 
* Handle Spell check
* EventListener for inputQuery input
* Posts query then transforms returned data to option elements that are appended 
* to a datalist that is bound to the input.
*/
function spellCheck(ev) {
    console.log("Spell Check trigger")
    var fd = new FormData()
    fd.append('query', ev.target.value)
    fetch(baseURL + "spell", {
        method: 'POST',
        body: fd
    })
    .then(response => {
        console.log("Spell Check response received")
        return response.json();
    })
    .then(data => {
        // Clear list
        while (spellDataList.hasChildNodes()) {
            spellDataList.removeChild(spellDataList.firstChild);
        }

        data.forEach(correction => {
            var option = document.createElement("option")
            option.setAttribute("value", correction)
            spellDataList.appendChild(option)
        })
    })
    .catch(error => {
        console.log("Spell Check: Request failed", error)
    });
    
}

// Bind form to spellCheck()
var inputQuery = document.getElementById('inputQuery');
inputQuery.addEventListener('input', spellCheck);

