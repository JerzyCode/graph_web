import {deleteGraph} from "./graph_service.js";
import {clearAll, loadGraphOnCanvas} from "./canvas.js";
import {showNotification} from "./main.js";


let currentLoadedGraphId;

export function openYourGraphsPopup() {
    loadYourGraphsPopup().catch(() => console.log('cant open popup'))
    document.getElementById('popup-container').style.display = 'block';
}


async function loadYourGraphsPopup() {
    console.log('loadYourGraphsPopup()')
    fetch('/getAllGraphs')
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
        closeButton.addEventListener('click', closePopup)
    }

    const listItem = document.getElementsByClassName('graph-item')
    const confirmDeleteButton = document.getElementById('confirm-delete-button')
    const cancelDeleteButton = document.getElementById('cancel-delete-button')


    Array.from(listItem).forEach(item => {
        const graphId = item.getAttribute('graph-data-id');
        const loadGraphButtons = item.getElementsByClassName('link-as-text');
        const deleteGraphButtons = item.getElementsByClassName('delete-graph-button')
        const editGraphButtons = item.getElementsByClassName('edit-graph-button')

        Array.from(loadGraphButtons).forEach(button => {
            setEventListenerLoadGraphButton(button, graphId)
        });

        Array.from(deleteGraphButtons).forEach(button => {
            setEventListenerDeleteGraphButton(button, confirmDeleteButton, graphId)
        })

        Array.from(editGraphButtons).forEach(button => {
            setEventListenerEditGraphButton(button, graphId)
        })
    })


    if (cancelDeleteButton) {
        setEventListenerCancelDeleteButton(cancelDeleteButton)
    }
}

function setEventListenerLoadGraphButton(button, graphId) {
    button.addEventListener('click', function (event) {
        event.preventDefault();
        onLoadGraph(graphId).then(r => console.log('Loaded Graph with id:' + graphId))
    });
}

async function onLoadGraph(graphId) {
    try {
        await loadGraphOnCanvas(graphId);
        currentLoadedGraphId = graphId
        closePopup();
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
        const deletedGraphId = deleteGraph(graphId).then(r => {
            console.log('Deleted graph with id=' + graphId)
            removeItemFromList(graphId)
            showNotification('Successfully deleted graph!', '#4cda15')
        }).catch(error => {
            showNotification('Something went wrong!', '#ff0000')
            console.log(error)
        })
        closeDeleteConfirmPopup()
        if (deletedGraphId === currentLoadedGraphId) {
            clearAll()
            currentLoadedGraphId = null
        }
    })

}

function setEventListenerCancelDeleteButton(cancelDeleteButton) {
    cancelDeleteButton.addEventListener('click', function () {
        closeDeleteConfirmPopup()
    })
}

function removeItemFromList(removedGraphId) {
    const listItem = document.getElementsByClassName('graph-item')
    Array.from(listItem).forEach(item => {
        const graphId = item.getAttribute('graph-data-id');
        if (removedGraphId === graphId) {
            item.remove()
        }
    })
}

function setEventListenerEditGraphButton(button) {
    button.addEventListener('click', function () {
        console.log('edit')
    });
}


export function closePopup() {
    document.getElementById('popup-container').style.display = 'none';
}

function openDeleteConfirmPopup() {
    document.getElementById('delete-confirm-popup').style.display = 'block'
}


function closeDeleteConfirmPopup() {
    document.getElementById('delete-confirm-popup').style.display = 'none'
}