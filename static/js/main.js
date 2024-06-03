import {repaint} from "./canvas.js";
import {closePopup, openYourGraphsPopup} from "./your_graphs_popup.js";

const notificationBar = document.getElementById('notification-bar')
const progress = document.getElementById('progress-bar')

const addListeners = function () {
    const loadGraphButton = document.getElementById('your-graphs-button')
    if (loadGraphButton) {
        loadGraphButton.addEventListener('click', openYourGraphsPopup)
    }

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

export function showNotification(message, color) {
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


addListeners()
