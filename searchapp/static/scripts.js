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

var currentCorpus = ''
var expanText = ''

/*
* Handle Query submission
* EventListener for query form
* Posts data and transforms documents to elements that are then
* appended to the docList div 
*/
function querySubmit(ev) {
    ev.preventDefault();
    currentCorpus = document.getElementById('coursesButton').checked ? 'courses/' : 'reuters/'
    fetch(baseURL + "docs", {
        method: 'POST',
        body: new FormData(this)
    })
    .then(response => {
        console.log("Query response received")
        return response.json();
    })
    .then(data => {
        // Handle the Global Query Expansion div and text
        expanText = data.expans 
        document.getElementById("globExpText").innerHTML = expanText
        document.getElementById("globExpDiv").style.display = "block"
        
        // Clear list
        while (divDocList.hasChildNodes()) {
            divDocList.removeChild(divDocList.firstChild);
        }

        data.docs.forEach(doc => {
            newDiv = document.createElement("div")
            newDiv.setAttribute("class", "doc")
            divDocList.appendChild(newDiv)

            aDocId = document.createElement("a")
            aDocId.setAttribute("href", baseURL + "docs/" + currentCorpus + doc["docId"])
            aDocId.innerHTML = "DocId: " + doc["docId"]
            newDiv.appendChild(aDocId)

            pExcerpt = document.createElement("p")
            pExcerpt.innerHTML ="Description: " + doc["excerpt"]
            newDiv.appendChild(pExcerpt)

            pScore = document.createElement("p")
            pScore.innerHTML = "Score: " + doc["score"]
            newDiv.appendChild(pScore)

            dRelevant = document.createElement("input");
            dRelevant.className = "relevantDocs";
            dRelevant.setAttribute("type", "checkbox");
            dRelevant.setAttribute("value", doc['docId']);
            dRelevant.setAttribute("onclick", "handleRelevanceFeedback(this)");
            newDiv.appendChild(dRelevant);

            newDiv.insertAdjacentHTML('beforeend', "Document is <strong>relevant</strong> to query<br>")

            dNonRelevant = document.createElement("input");
            dNonRelevant.className = "nonRelevantDocs";
            dNonRelevant.setAttribute("type", "checkbox");
            dNonRelevant.setAttribute("value", doc['docId']);
            dNonRelevant.setAttribute("onclick", "handleRelevanceFeedback(this)");
            newDiv.appendChild(dNonRelevant);

            newDiv.insertAdjacentHTML('beforeend', "Document is <strong>non-relevant</strong> to query<br>")
        })
    })
    .catch(error => {
        console.log("Query: Request failed", error)
    });
}

function handleRelevanceFeedback(event) {
    let checked = event.checked;
    let docId = event.value;
    let type = event.className;

    fetch(baseURL + "relevance?query=" + inputQuery.value + "&docId=" + docId + "&checked=" + checked + "&type=" + type, {
        method: 'PUT',
    })
    .then(response => {
        console.log("Query response received")
        return response.json();
    })
    .catch(error => {
        console.log("Query: Request failed", error)
    });
}

// Handle the button for the Global Query Expansion
function handleReplaceButton(event) {
    document.getElementById('inputQuery').value = expanText
}

var replaceButton = document.getElementById('replaceButton');
replaceButton.addEventListener('click', handleReplaceButton);

// Bind form to querySubmit()
var form = document.getElementById('query');
form.addEventListener('submit', querySubmit);

var spellDataList = document.getElementById('spellList');

// Bind form to spellCheck()
let inputQuery = document.getElementById('inputQuery');
inputQuery.addEventListener('input', spellCheck);
let spellTitle = document.getElementById('spellTitle');

window.addEventListener("load", () => {
    let input = document.getElementById('inputQuery');
    input.addEventListener("input", (event) => {
        spellCheck(event);
    });

    window.spellCheckRequests = new XMLHttpRequest();
});

/*
* Handle Spell check
* EventListener for inputQuery input
* Posts query then transforms returned data to option elements that are appended
* to a datalist that is bound to the input.
*/
function spellCheck(event) {
    let input = event.target;
    let spellList = document.getElementById('spellList');
    let min_chars = 1;
    let model = document.getElementById('boolButton').checked ? 'bool' : 'vsm'
    let corpus = document.getElementById('coursesButton').checked ? 'courses' : 'reuters'

    if (input.value.length < min_chars) {
        window.spellCheckRequests.abort();
        spellTitle.style.display = "none";
        spellList.innerHTML = '';
    }
    else {
        spellTitle.style.display = "block";
        window.spellCheckRequests.abort();
        window.spellCheckRequests.onreadystatechange = () => {
            if (window.spellCheckRequests.readyState == 4 && window.spellCheckRequests.status == 200) {
                let response = JSON.parse(window.spellCheckRequests.responseText);
                spellList.innerHTML = '';

                if (response.length == 0) spellTitle.style.display = "none";

                response.forEach( item => {
                    console.log(item);
                    let option = document.createElement('li');
                    let text = document.createTextNode(item);
                    option.appendChild(text);
                    option.addEventListener("click", () => {
                        inputQuery.value = option.innerHTML;
                    });
                    spellList.appendChild(option);
                });
            }
        };
        window.spellCheckRequests.open('GET', '/spell?query=' + input.value + '&model=' + model + '&corpus=' + corpus, true);
        window.spellCheckRequests.send();
    }
}
