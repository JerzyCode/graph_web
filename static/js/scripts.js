document.addEventListener('DOMContentLoaded', function () {
    const loadGraphButton = document.getElementById('your-graphs-button')
    if (loadGraphButton) {
        loadGraphButton.addEventListener('click', openYourGraphsPopup)
    }

    window.addEventListener('keydown', function (event) {
        if (event.key === 'Escape') {
            closePopup()
        }
    })

    window.onclick = function (event) {
        const popupForms = document.getElementsByClassName('popup-container');
        for (let popup of popupForms)
            if (event.target === popup) {
                popup.style.display = "none";
            }
    }
});

async function loadGraphPopup() {
    console.log('loadGraphPopup()')
    fetch('/getAllGraphs')
        .then(response => response.text())
        .then(html => {
            console.log('fetchedGraphNames...')
            document.getElementById('popup-container').innerHTML = html;
        })
        .catch(error => console.error('Error loading popup content:', error));
}

function openYourGraphsPopup() {
    loadGraphPopup().catch(error => console.log('cant open popup'))
    document.getElementById('popup-container').style.display = 'block';
}

function closePopup() {
    document.getElementById('popup-container').style.display = 'none';
}

async function onLoadGraph(graph_id) {
    try {
        await window.loadGraphOnCanvas(graph_id);
        closePopup();
    } catch (error) {
        console.error('Error loading graph occurred:', error);
    }
}