import {repaint} from "./canvas.js";
import {closePopup, openYourGraphsPopup} from "./your_graphs_popup.js";
import {addVertex} from "./modify_graph_service.js";

const notificationBar = document.getElementById('notification-bar')
const progress = document.getElementById('progress-bar')

const addVertexPopup = document.getElementById('add-vertex-popup')
const addVertexButton = document.getElementById('add-vertex-button')

const addListeners = function () {
    const loadGraphButton = document.getElementById('your-graphs-button')
    if (loadGraphButton) {
        loadGraphButton.addEventListener('click', openYourGraphsPopup)
    }

    if (addVertexButton) {
        addVertexButton.addEventListener('click', addVertex)
    }

    window.addEventListener('click', closeAddVertexPopup)
    window.addEventListener('keydown', function (event) {
        if (event.key === 'Escape') {
            closePopup()
        }
    })

    window.addEventListener('resize', repaint)


    window.onclick = function (event) {
        const popupForms = document.getElementsByClassName('popup-container');
        for (let popup of popupForms)
            if (event.target === popup) {
                popup.style.display = "none";
            }
    }
}

function showNotification(message, color) {
    const notificationMessage = document.getElementById('notification-message');
    notificationMessage.textContent = message;
    progress.style.backgroundColor = color
    notificationBar.style.border = '1px solid ' + color
    notificationBar.classList.add('show')
    notificationBar.style.display = 'block'
    progress.classList.add('active')
    setTimeout(() => {
        notificationBar.classList.remove('show');
        progress.classList.remove('active')
    }, 3300);
}

export function showSuccessMessage(message) {
    showNotification(message, '#4cda15')
}

export function showFailMessage(message) {
    showNotification(message, '#ff0000')
}

export function showAddVertexPopup(xPos, yPos) {
    addVertexPopup.style.left = xPos + 'px'
    addVertexPopup.style.top = yPos + 'px'
    addVertexPopup.style.display = 'block';
}


export function closeAddVertexPopup() {
    addVertexPopup.style.display = 'none';
}

addListeners()
