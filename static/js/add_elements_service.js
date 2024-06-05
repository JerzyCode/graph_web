import {createVertexEndpoint} from "./endpoints.js";
import {addVertexOnCanvas} from "./canvas.js";
import {showFailMessage, showSuccessMessage} from "./main.js";


export const addVertexParams = {}

export async function addVertex() {

    let graphId = addVertexParams.graph_id
    let x = addVertexParams.x
    let y = addVertexParams.y
    await createVertexEndpoint(graphId, x, y)
        .then(vertex => {
            const json = JSON.parse(vertex);
            console.log('Added vertex=' + json)
            showSuccessMessage('Successfully added vertex!')
            addVertexOnCanvas(json)
        }).catch(error => {
            showFailMessage('Something went wrong adding vertex!')
            console.log(error)
        })
}