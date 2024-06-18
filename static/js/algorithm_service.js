import {runBfsAlgorithmEndpoint, runDfsAlgorithmEndpoint} from "./endpoints.js";
import {colorGraphAlgorithm} from "./canvas.js";
import {currentLoadedGraph} from "./modify_graph_service.js";
import {showFailMessage} from "./shared.js";

export async function runDfsAlgorithm() {
    let graphId = currentLoadedGraph.graphId
    console.log("Running DFS for graph with id=" + graphId)
    try {
        let objectsToColor = await runDfsAlgorithmEndpoint(graphId)
        await colorGraphAlgorithm(objectsToColor)
    } catch (error) {
        showFailMessage('Something went wrong running DFS!')
    }
}

export async function runBfsAlgorithm() {
    let graphId = currentLoadedGraph.graphId
    console.log("Running DFS for graph with id=" + graphId)
    try {
        let objectsToColor = await runBfsAlgorithmEndpoint(graphId)
        await colorGraphAlgorithm(objectsToColor)
    } catch (error) {
        showFailMessage('Something went wrong running BFS!')
    }
}