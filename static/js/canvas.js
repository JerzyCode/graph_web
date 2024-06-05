import {fetchGraph} from "./endpoints.js";
import {showAddVertexPopup} from "./main.js";
import {prepareEdgesToDraw} from "./canvas_utils.js";
import {addVertexParams} from "./modify_graph_service.js";

const canvas = document.getElementById("canvas")
const container = document.getElementById("canvas-container")
const ctx = canvas.getContext('2d')

const VERTEX_BORDER_COLOR = 'purple'
const VERTEX_FILL_COLOR = 'yellow'
const VERTEX_RADIUS = 10
const EDGE_WIDTH = 2
const EDGE_COLOR = 'purple'


let graph
let vertices = []
let edges = []
let currentVertex = null
let isDragging = false

canvas.width = container.clientWidth
canvas.height = container.clientHeight


canvas.onmousedown = handleMouseDown
canvas.onmouseup = handleStopDragging
canvas.onmouseout = handleStopDragging
canvas.onmousemove = handleMouseMove
canvas.oncontextmenu = handleRightClick

window.addEventListener('resize', repaint)


export async function loadGraphOnCanvas(graphId) {
    const graphJson = await fetchGraph(graphId);
    graph = JSON.parse(graphJson);
    console.log(`loadGraphOnCanvas(), graphId=${graphId}`)
    vertices = graph.vertices
    edges = prepareEdgesToDraw(graph.edges, vertices)
    redrawGraph()
}


function handleMouseDown(event) {
    event.preventDefault()
    for (let path of vertices) {
        if (isVertexPressed(event, path)) {
            currentVertex = path
            isDragging = true
            console.log(path)
            return
        }
    }
}

function isVertexPressed(event, path) {
    let canvasCoords = calculateCoordsOnCanvas(event)
    const dx = canvasCoords.x - path.x
    const dy = canvasCoords.y - path.y
    return dx * dx + dy * dy <= VERTEX_RADIUS * VERTEX_RADIUS
}

function handleStopDragging(event) {
    if (!isDragging) {
        return
    }
    event.preventDefault()
    currentVertex = null
    isDragging = false
}

function handleMouseMove(event) {
    let canvasCoords = calculateCoordsOnCanvas(event)
    if (isDragging) {
        if (canvasCoords.x < VERTEX_RADIUS || canvasCoords.x > canvas.width - VERTEX_RADIUS ||
            canvasCoords.y < VERTEX_RADIUS || canvasCoords.y > canvas.height - VERTEX_RADIUS) {
            return
        }
        currentVertex.x = canvasCoords.x
        currentVertex.y = canvasCoords.y
        repaint()
    }
}

function handleRightClick(event) {
    event.preventDefault()
    if (graph == null) {
        return
    }
    let canvasCoords = calculateCoordsOnCanvas(event)
    console.log(`pressed RightClick on coords: ${canvasCoords.x}, ${canvasCoords.y}`)
    addVertexParams.graph_id = graph.id
    addVertexParams.x = canvasCoords.x
    addVertexParams.y = canvasCoords.y
    showAddVertexPopup(event.x, event.y)

}

export function repaint() {
    clearAll()
    drawAllEdges()
    drawAllVertices()
}

function drawAllVertices() {
    for (let vertex of vertices) {
        drawVertex(vertex)
    }
}

function drawVertex(vertex) {
    ctx.fillStyle = VERTEX_FILL_COLOR
    ctx.strokeStyle = VERTEX_BORDER_COLOR
    ctx.lineWidth = EDGE_WIDTH
    ctx.beginPath()
    ctx.arc(vertex.x, vertex.y, VERTEX_RADIUS, 0, Math.PI * 2)
    ctx.fill()
    ctx.stroke()
    ctx.closePath()
}

function drawEdge(edge) {
    ctx.strokeStyle = EDGE_COLOR
    ctx.lineWidth = EDGE_WIDTH
    ctx.beginPath()
    ctx.moveTo(edge.vertex_in.x, edge.vertex_in.y)
    ctx.lineTo(edge.vertex_out.x, edge.vertex_out.y)
    ctx.stroke()
    ctx.closePath()
}

function drawAllEdges() {
    for (let edge of edges) {
        drawEdge(edge)
    }
}


function drawAll() {
    drawAllEdges()
    drawAllVertices()
}

export function clearAll() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
}

function redrawGraph() {
    clearAll()
    drawAll()
}

function calculateCoordsOnCanvas(event) {
    let rect = canvas.getBoundingClientRect()
    let x_canvas = event.x - rect.left
    let y_canvas = event.y - rect.top
    return {'x': x_canvas, 'y': y_canvas}
}

export function addVertexOnCanvas(vertex) {
    console.debug(`addVertexOnCanvas(), vertex=${JSON.stringify(vertex)}`)
    vertices.push(vertex)
    drawVertex(vertex)
}