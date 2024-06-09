import {repaint} from "./canvas.js";
import {closeYourGraphsPopup, openYourGraphsPopup} from "./your_graphs_popup.js";
import {addVertex, deleteEdge, deleteVertex, selectToEdge} from "./modify_graph_service.js";

const notificationBar = document.getElementById('notification-bar')
const progress = document.getElementById('progress-bar')

const addVertexPopup = document.getElementById('add-vertex-popup')
const addVertexButton = document.getElementById('add-vertex-button')

const selectEdgeButton = document.getElementById('select-to-edge-button')

const deleteVertexButton = document.getElementById('delete-vertex-button')

const graphActionsPopup = document.getElementById('graph-actions-popup')

const deleteEdgePopup = document.getElementById('delete-edge-popup')
const deleteEdgeButton = document.getElementById('delete-edge-button')

const createNewGraphShowPopupButton = document.getElementById('create-graph-show-popup-button')

const createGraphPopup = document.getElementById('create-graph-popup')
const createGraphButton = document.getElementById('create-new-graph-button')
const closeCreateGraphPopupButton = document.getElementById('close-create-graph-popup-button')
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

    if (selectEdgeButton) {
        selectEdgeButton.addEventListener('click', selectToEdge)
    }

    if (deleteEdgeButton) {
        deleteEdgeButton.addEventListener('click', deleteEdge)
    }

    if (createNewGraphShowPopupButton) {
        createNewGraphShowPopupButton.addEventListener('click', showCreateGraphPopup)
    }

    if (closeCreateGraphPopupButton) {
        closeCreateGraphPopupButton.addEventListener('click', closeCreateGraphPopup)
    }

    window.addEventListener('click', () => {
        closeAddVertexPopup()
        closeGraphActionsPopup()
        closeDeleteEdgePopup()
    })
    window.addEventListener('keydown', function (event) {
        if (event.key === 'Escape') {
            closeAddVertexPopup()
            closeGraphActionsPopup()
            closeDeleteEdgePopup()
            closeGraphActionsPopup()
            closeCreateGraphPopup()
            closeYourGraphsPopup()
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

export function showDeleteEdgePopup(xPos, yPos) {
    showPopup(deleteEdgePopup, xPos, yPos)
}

export function closeDeleteEdgePopup() {
    closePopup(deleteEdgePopup)
}

function showCreateGraphPopup() {
    document.getElementById('create-graph-popup-container').style.display = 'block';

}

function closeCreateGraphPopup() {
    document.getElementById('create-graph-popup-container').style.display = 'none';
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
