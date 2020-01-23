// https://developers.google.com/web/updates/2015/03/introduction-to-fetch
// https://github.com/pallets/flask/blob/master/examples/javascript/js_example/templates/fetch.html

// Handle Query submissions
function querySubmit(ev) {
    ev.preventDefault();
    fetch("http://localhost:5000/docs", {
        method: 'POST',
        body: new FormData(this)
    })
    .then(response => {
        return response.json();
    })
    .then(data => {
        console.log("Query: Received data")
        console.log(data)
    })
    .catch(error => {
        console.log("Spell Check: Request failed", error)
    });
}

// Bind form to querySubmit()
var form = document.getElementById('query');
form.addEventListener('submit', querySubmit);

var spellDataList = document.getElementById('spellList');

// Handle Spell check
function spellCheck(ev) {
    //ev.preventDefault();
    console.log("Spell Check trigger")
    var fd = new FormData()
    fd.append('query', ev.target.value)
    fetch("http://localhost:5000/spell", {
        method: 'POST',
        body: fd
    })
    .then(response => {
        return response.json();
    })
    .then(data => {
        while (spellDataList.hasChildNodes()) {
            spellDataList.removeChild(spellDataList.firstChild);
        }
        for(correction of data){
            var option = document.createElement("option")
            option.setAttribute("value", correction)
            spellDataList.appendChild(option)
        }
    })
    .catch(error => {
        console.log("Spell Check: Request failed", error)
    });
    
}

// Bind form to spellCheck()
var inputQuery = document.getElementById('inputQuery');
inputQuery.addEventListener('input', spellCheck);

