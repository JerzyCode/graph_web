document.addEventListener('DOMContentLoaded', function () {
    const loadGraphButton = document.getElementById('your-graphs-button')

    if (loadGraphButton) {
        loadGraphButton.addEventListener('click', openYourGraphsPopup)
    }

});

function loadGraphPopup() {
    fetch('/getAllGraphs')
        .then(response => response.text())
        .then(html => {
            document.getElementById('popup-container').innerHTML = html;
        })
        .catch(error => console.error('Error loading popup content:', error));
}

function openYourGraphsPopup() {
    loadGraphPopup()
    document.getElementById('popup-container').style.display = 'block';
}

function closePopup() {
    document.getElementById('popup-container').style.display = 'none';
}


window.onclick = function (event) {
    const popupForms = document.getElementsByClassName('popup-container');
    for (let popup of popupForms)
        if (event.target === popup) {
            popup.style.display = "none";
        }
}