import {createVertexEndpoint, deleteGraphEndpoint} from "./endpoints.js";
import {addVertexOnCanvas, clearAll} from "./canvas.js";
import {showFailMessage, showSuccessMessage} from "./main.js";
import {closeDeleteConfirmPopup, removeItemFromList} from "./your_graphs_popup.js";


export const addVertexParams = {}
export const currentLoadedGraph = {}

export async function addVertex() {
    let graphId = currentLoadedGraph.graphId
    let x = addVertexParams.x
    let y = addVertexParams.y
    await createVertexEndpoint(graphId, x, y)
        .then(vertex => {
            const json = JSON.parse(vertex);
            console.log('Added vertex=' + vertex)
            showSuccessMessage('Successfully added vertex!')
            addVertexOnCanvas(json)
        }).catch(error => {
            showFailMessage('Something went wrong adding vertex!')
            console.log(error)
        })
}


export async function deleteGraph(graphId) {
    deleteGraphEndpoint(graphId).then(r => {
        console.log('Deleted graph with id=' + graphId)
        removeItemFromList(graphId)
        showSuccessMessage('Successfully deleted graph!')
    }).catch(error => {
        showFailMessage('Something went wrong!')
        console.log(error)
    })
    closeDeleteConfirmPopup();

    if (graphId === currentLoadedGraph.graphId) {
        clearAll()
    }
}