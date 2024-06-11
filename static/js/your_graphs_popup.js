import {loadGraphOnCanvas} from "./canvas.js";
import {currentLoadedGraph, deleteGraph} from "./modify_graph_service.js";
import {showSuccessMessage} from "./shared.js";


export function openYourGraphsPopup() {
    loadYourGraphsPopup().catch(() => console.log('cant open popup'))
    document.getElementById('popup-container').style.display = 'block';
}


async function loadYourGraphsPopup() {
    console.log('loadYourGraphsPopup()')
    fetch('graph/getAllGraphs')
        .then(response => response.text())
        .then(html => {
            console.log('fetchedGraphNames...')
            document.getElementById('popup-container').innerHTML = html;
            setYourGraphsPopupButtons()
        })
        .catch(error => console.error('Error loading popup content:', error));
}


function setYourGraphsPopupButtons() {
    const closeButton = document.getElementById('closeButton')
    if (closeButton) {
        closeButton.addEventListener('click', closeYourGraphsPopup)
    }

    const listItem = document.getElementsByClassName('graph-item')
    const confirmDeleteButton = document.getElementById('confirm-delete-button')
    const cancelDeleteButton = document.getElementById('cancel-delete-button')


    Array.from(listItem).forEach(item => {
        const graphId = item.getAttribute('graph-data-id');
        const loadGraphButtons = item.getElementsByClassName('link-as-text');
        const deleteGraphButtons = item.getElementsByClassName('delete-graph-button')

        Array.from(loadGraphButtons).forEach(button => {
            setEventListenerLoadGraphButton(button, graphId)
        });

        Array.from(deleteGraphButtons).forEach(deleteGraphButton => {
            setEventListenerDeleteGraphButton(deleteGraphButton, confirmDeleteButton, graphId)
        })

    })


    if (cancelDeleteButton) {
        cancelDeleteButton.addEventListener('click', closeDeleteConfirmPopup)
    }

}

function setEventListenerLoadGraphButton(button, graphId) {
    button.addEventListener('click', function (event) {
        event.preventDefault();
        onLoadGraph(graphId).then(r => {
            showSuccessMessage('Loaded graph!')
        })
    });
}

async function onLoadGraph(graphId) {
    try {
        await loadGraphOnCanvas(graphId);
        currentLoadedGraph.graphId = graphId
        closeYourGraphsPopup();
    } catch (error) {
        console.error('Error loading graph occurred:', error);
    }
}

function setEventListenerDeleteGraphButton(button, confirmDeleteButton, graphId) {
    button.addEventListener('click', function () {
        openDeleteConfirmPopup()
        setEventListenerConfirmDeleteButton(confirmDeleteButton, graphId)
    });
}

function setEventListenerConfirmDeleteButton(confirmDeleteButton, graphId) {
    confirmDeleteButton.addEventListener('click', function () {
        deleteGraph(graphId)
    })
}


export function removeItemFromList(removedGraphId) {
    const listItem = document.getElementsByClassName('graph-item')
    Array.from(listItem).forEach(item => {
        const graphId = item.getAttribute('graph-data-id');
        if (removedGraphId === graphId) {
            item.remove()
        }
    })
}


export function closeYourGraphsPopup() {
    document.getElementById('popup-container').style.display = 'none';
}

function openDeleteConfirmPopup() {
    document.getElementById('delete-confirm-popup').style.display = 'block'
}


export function closeDeleteConfirmPopup() {
    document.getElementById('delete-confirm-popup').style.display = 'none'
}

