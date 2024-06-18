import {repaint} from "./canvas.js";
import {closeYourGraphsPopup, openYourGraphsPopup} from "./your_graphs_popup.js";
import {addVertex, createGraph, deleteEdge, deleteVertex, selectToEdge} from "./modify_graph_service.js";
import {runDfsAlgorithm} from "./algorithm_service.js";

const addVertexPopup = document.getElementById('add-vertex-popup')
const addVertexButton = document.getElementById('add-vertex-button')

const runDfsButton = document.getElementById('dfs-algorithm-button')
const selectEdgeButton = document.getElementById('select-to-edge-button')

const deleteVertexButton = document.getElementById('delete-vertex-button')

const graphActionsPopup = document.getElementById('graph-actions-popup')

const deleteEdgePopup = document.getElementById('delete-edge-popup')
const deleteEdgeButton = document.getElementById('delete-edge-button')

const createNewGraphShowPopupButton = document.getElementById('create-graph-show-popup-button')

const createGraphButton = document.getElementById('create-new-graph-button')
const closeCreateGraphPopupButton = document.getElementById('close-create-graph-popup-button')
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
    if (runDfsButton) {
        runDfsButton.addEventListener('click', runDfsAlgorithm)
    }

    if (createGraphButton) {
        createGraphButton.addEventListener('click', () => {
            const graphNameInput = document.getElementById('graph-name');
            const graphName = graphNameInput.value;
            createGraph(graphName)
        })
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

export function closeCreateGraphPopup() {
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

window.addEventListener('DOMContentLoaded', () => {
    addListeners()
})
