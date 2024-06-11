import {
    addEdgeEndpoint,
    createGraphEndpoint,
    createVertexEndpoint,
    deleteEdgeEndpoint,
    deleteGraphEndpoint,
    deleteVertexEndpoint
} from "./endpoints.js";
import {
    addEdgeOnCanvas,
    addVertexOnCanvas,
    clearAll,
    deleteEdgeOnCanvas,
    deleteVertexOnCanvas,
    loadGraphOnCanvas,
    markVertexSelected,
    unmarkSelectedVertices
} from "./canvas.js";
import {closeCreateGraphPopup, showFailMessage, showSuccessMessage} from "./graph_panel.js";
import {closeDeleteConfirmPopup, removeItemFromList} from "./your_graphs_popup.js";


export const addVertexParams = {}
export const deleteVertexParams = {}
export const currentLoadedGraph = {}
export const selectedVertexId = {}

export const deleteEdgeParams = {edgeId: null}

export const addEdgeParams = {
    graphId: null,
    vertexInId: null,
    vertexOutId: null
};

export async function addVertex() {
    let graphId = currentLoadedGraph.graphId
    let x = addVertexParams.x
    let y = addVertexParams.y
    await createVertexEndpoint(graphId, x, y)
        .then(vertex => {
            const json = JSON.parse(vertex);
            console.debug('Added vertex=' + vertex)
            showSuccessMessage('Successfully added vertex!')
            addVertexOnCanvas(json)
        }).catch(error => {
            showFailMessage('Something went wrong adding vertex!')
            console.log(error)
        })
}

export async function deleteVertex() {
    let graphId = deleteVertexParams.graphId
    let vertexId = deleteVertexParams.vertexId
    await deleteVertexEndpoint(graphId, vertexId)
        .then(() => {
            console.debug(`Delete vertex: graph_id=${graphId}, vertex_id=${vertexId}`)
            showSuccessMessage('Successfully deleted vertex!')
            deleteVertexOnCanvas(vertexId)
        }).catch(error => {
            showFailMessage('Something went wrong deleting vertex!')
            console.log(error)
        })
}


export async function deleteGraph(graphId) {
    deleteGraphEndpoint(graphId).then(r => {
        console.debug('Deleted graph with id=' + graphId)
        removeItemFromList(graphId)
        showSuccessMessage('Successfully deleted graph!')
    }).catch(error => {
        showFailMessage('Something went wrong deleting graph!')
        console.log(error)
    })
    closeDeleteConfirmPopup();

    if (graphId === currentLoadedGraph.graphId) {
        clearAll()
    }
}

export async function addEdge() {
    let graphId = addEdgeParams.graphId
    let vertexInId = addEdgeParams.vertexInId
    let vertexOutId = addEdgeParams.vertexOutId

    addEdgeEndpoint(graphId, vertexInId, vertexOutId)
        .then(addedEdgeResp => {

            showSuccessMessage('Successfully added edge!')
            addEdgeOnCanvas(JSON.parse(addedEdgeResp))
            console.log('Added edge')
        }).catch(error => {
        showFailMessage('Something went wrong deleting edge!')
        console.log(error)
    })
    resetAddEdgeParams()
    unmarkSelectedVertices()
}

export async function selectToEdge() {
    let vertexId = selectedVertexId.vertexId
    if (addEdgeParams.vertexInId === null) {
        addEdgeParams.vertexInId = vertexId
        markVertexSelected(vertexId)

    } else if (addEdgeParams.vertexOutId === null) {
        addEdgeParams.vertexOutId = vertexId;
        markVertexSelected(vertexId)
        await addEdge()
    }
}

function resetAddEdgeParams() {
    addEdgeParams.vertexInId = null
    addEdgeParams.vertexOutId = null
}

export async function deleteEdge() {
    let edgeId = deleteEdgeParams.edgeId

    deleteEdgeEndpoint(edgeId)
        .then(() => {
            console.debug(`Delete edge: edge_id=${edgeId}`)
            showSuccessMessage('Successfully deleted edge!')
            deleteEdgeOnCanvas(edgeId)
        })
        .catch(error => {
            showFailMessage('Something went wrong deleting edge!')
            console.log(error)
        })
    deleteEdgeParams.edgeId = null
}

export function createGraph(graphName) {

    createGraphEndpoint(graphName)
        .then(graphId => {
            closeCreateGraphPopup()
            loadGraphOnCanvas(graphId)
                .then(() => {
                    currentLoadedGraph.graphId = graphId
                    showSuccessMessage('Successfully created graph!')
                })
        })
        .catch(error => {
            showFailMessage('Something went wrong creating graph!')
            console.log(error)
        })
}