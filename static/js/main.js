import {repaint} from "./canvas.js";
import {openYourGraphsPopup} from "./your_graphs_popup.js";
import {addVertex, deleteVertex} from "./modify_graph_service.js";

const notificationBar = document.getElementById('notification-bar')
const progress = document.getElementById('progress-bar')

const addVertexPopup = document.getElementById('add-vertex-popup')
const addVertexButton = document.getElementById('add-vertex-button')

const deleteVertexButton = document.getElementById('delete-vertex-button')

const graphActionsPopup = document.getElementById('graph-actions-popup')

let isShowedNotification = false
const addListeners = function () {
    const loadGraphButton = document.getElementById('your-graphs-button')
    if (loadGraphButton) {
        loadGraphButton.addEventListener('click', openYourGraphsPopup)
    }

    if (addVertexButton) {
        addVertexButton.addEventListener('click', addVertex)
    }

    if (deleteVertexButton) {
        deleteVertexButton.addEventListener('click', deleteVertex)
    }

    window.addEventListener('click', () => {
        closeAddVertexPopup()
        closeGraphActionsPopup()
    })
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
    if (isShowedNotification) {
        return
    }
    setNotificationBarVisible(message, color)
    setTimeout(() => {
        setNotificationBarInvisible()
    }, 1500);
}

function setNotificationBarVisible(message, color) {
    isShowedNotification = true
    const notificationMessage = document.getElementById('notification-message');
    notificationMessage.textContent = message;
    progress.style.backgroundColor = color
    notificationBar.style.border = '1px solid ' + color
    notificationBar.classList.add('show')
    notificationBar.style.display = 'block'
    progress.classList.add('active')
}

function setNotificationBarInvisible() {
    notificationBar.classList.remove('show');
    progress.classList.remove('active')
    isShowedNotification = false
}

export function showSuccessMessage(message) {
    showNotification(message, '#4cda15')
}

export function showFailMessage(message) {
    showNotification(message, '#ff0000')
}


export function showAddVertexPopup(xPos, yPos) {
    showPopup(addVertexPopup, xPos, yPos)
}


export function closeAddVertexPopup() {
    closePopup(addVertexPopup)
}

export function showGraphActionsPopup(xPos, yPos) {
    showPopup(graphActionsPopup, xPos, yPos)
}


export function closeGraphActionsPopup() {
    closePopup(graphActionsPopup)
}


function showPopup(popup, xPos, yPos) {
    popup.style.left = xPos + 'px'
    popup.style.top = yPos + 'px'
    popup.style.display = 'block';
}

function closePopup(popup) {
    popup.style.display = 'none';
}

addListeners()
