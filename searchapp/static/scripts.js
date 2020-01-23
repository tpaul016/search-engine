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

// Handle Spell check
function spellCheck () {
    //ev.preventDefault();
    fetch("http://localhost:5000/spell", {
        method: 'POST',
        body: new FormData(this)
    })
    .then(response => {
        return response.json();
    })
    .then(data => {
        console.log("Spell Check: Received data")
        console.log(data)
    })
    .catch(error => {
        console.log("Spell Check: Request failed", error)
    });
}

var spellDataList = document.getElementById('spellList');