import {deleteGraph} from "./graph_service.js";
import {clearAll} from "./canvas.js";


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

    Array.from(listItem).forEach(item => {
        const graphId = item.getAttribute('graph-data-id');
        const loadGraphButtons = item.getElementsByClassName('link-as-text');
        const deleteGraphButtons = item.getElementsByClassName('delete-graph-button')
        const editGraphButtons = item.getElementsByClassName('edit-graph-button')

        Array.from(loadGraphButtons).forEach(button => {
            setEventListenerLoadGraphButton(button, graphId)
        });

        Array.from(deleteGraphButtons).forEach(button => {
            setEventListenerDeleteGraphButton(button, graphId)
        })

        Array.from(editGraphButtons).forEach(button => {
            setEventListenerEditGraphButton(button, graphId)
        })
    })
}

function setEventListenerLoadGraphButton(button, graphId) {
    button.addEventListener('click', function (event) {
        event.preventDefault();
        onLoadGraph(graphId).then(r => console.log('Loaded Graph with id:' + graphId))
    });
}

function setEventListenerDeleteGraphButton(button, graphId) {
    button.addEventListener('click', function (event) {
        const deletedGraphId = deleteGraph(graphId).then(r => {
            console.log('Deleted graph with id=' + graphId)
            removeItemFromList(graphId)
        })
        if (deletedGraphId === currentLoadedGraphId) {
            clearAll()
            currentLoadedGraphId = null
        }
    });
}

function removeItemFromList(removedGraphId) {
    const listItem = document.getElementsByClassName('graph-item')
    console.log(listItem)
    Array.from(listItem).forEach(item => {
        const graphId = item.getAttribute('graph-data-id');
        if (removedGraphId === graphId) {
            item.remove()
        }
    })
}

function setEventListenerEditGraphButton(button, graphId) {
    button.addEventListener('click', function (event) {
        console.log('edit')
    });
}


async function onLoadGraph(graphId) {
    try {
        await window.loadGraphOnCanvas(graphId);
        currentLoadedGraphId = graphId
        closePopup();
    } catch (error) {
        console.error('Error loading graph occurred:', error);
    }
}

export function closePopup() {
    document.getElementById('popup-container').style.display = 'none';
}