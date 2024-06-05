import {addVertexOnCanvas, repaint} from "./canvas.js";
import {closePopup, openYourGraphsPopup} from "./your_graphs_popup.js";
import {createVertexEndpoint} from "./endpoints.js";

const notificationBar = document.getElementById('notification-bar')
const progress = document.getElementById('progress-bar')

const addVertexPopup = document.getElementById('add-vertex-popup')
const addVertexButton = document.getElementById('add-vertex-button')

let newVertex = null
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

export function showAddVertexPopup(xPos, yPos, vertexParams) {
    addVertexPopup.style.left = xPos + 'px'
    addVertexPopup.style.top = yPos + 'px'
    newVertex = vertexParams
    console.log(xPos, yPos)
    console.log(vertexParams)
    addVertexPopup.style.display = 'block';
}


export function closeAddVertexPopup() {
    addVertexPopup.style.display = 'none';
}


async function addVertex() {
    let graphId = newVertex.graphId;
    let x = newVertex.x
    let y = newVertex.y
    await createVertexEndpoint(graphId, x, y)
        .then(response => response.json())
        .then(data => {
            console.log('Added vertex=' + JSON.stringify(data))
            showNotification('Successfully added vertex!', '#4cda15')
            addVertexOnCanvas(data)
        }).catch(error => {
            showNotification('Something went wrong adding vertex!', '#ff0000')
            console.log(error)
        })
}

addListeners()
