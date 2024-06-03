import {prepareEdgesToDraw, prepareVerticesToDraw} from "./canvas_utils.js";
import {fetchGraph} from "./graph_service.js";

const canvas = document.getElementById("canvas")
const container = document.getElementById("canvas-container")
const ctx = canvas.getContext('2d')

const VERTEX_BORDER_COLOR = 'purple'
const VERTEX_FILL_COLOR = 'yellow'
const VERTEX_RADIUS = 10
const EDGE_COLOR = 'purple'


let graph
let vertices
let edges
let currentVertex = null
let isDragging = false

canvas.width = container.clientWidth
canvas.height = container.clientHeight


canvas.onmousedown = handleMouseDown
canvas.onmouseup = handleStopDragging
canvas.onmouseout = handleStopDragging
canvas.onmousemove = handleMouseMove

window.addEventListener('resize', repaint)

let preparedVertices = []
let preparedEdges = []


export async function loadGraphOnCanvas(graph_id) {
    graph = await fetchGraph(graph_id)
    vertices = graph.vertices
    edges = graph.edges
    preparedVertices = prepareVerticesToDraw(vertices)
    preparedEdges = prepareEdgesToDraw(edges, preparedVertices)
    redrawGraph()
}


function handleMouseDown(event) {
    event.preventDefault()
    for (let path of preparedVertices) {
        if (isVertexPressed(event, path)) {
            currentVertex = path
            isDragging = true
            console.log(path)
            return
        }
    }
}

function isVertexPressed(event, path) {
    let rect = canvas.getBoundingClientRect()
    let x_canvas = event.x - rect.left
    let y_canvas = event.y - rect.top
    const dx = x_canvas - path.x
    const dy = y_canvas - path.y
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
    let rect = canvas.getBoundingClientRect()
    let x_canvas = event.x - rect.left
    let y_canvas = event.y - rect.top
    if (isDragging) {
        if (x_canvas < VERTEX_RADIUS || x_canvas > canvas.width - VERTEX_RADIUS ||
            y_canvas < VERTEX_RADIUS || y_canvas > canvas.height - VERTEX_RADIUS) {
            return
        }
        currentVertex.x = x_canvas
        currentVertex.y = y_canvas
        repaint()
    }
}

export function repaint() {
    ctx.clearRect(0, 0, canvas.width, canvas.height)
    drawAllEdges()
    drawAllVertices()
}

function drawAllVertices() {
    for (let vertex of preparedVertices) {
        drawVertex(vertex)
    }
}

function drawVertex(vertex) {
    ctx.fillStyle = VERTEX_FILL_COLOR
    ctx.strokeStyle = VERTEX_BORDER_COLOR
    ctx.lineWidth = 2
    ctx.beginPath()
    ctx.arc(vertex.x, vertex.y, VERTEX_RADIUS, 0, Math.PI * 2)
    ctx.fill()
    ctx.stroke()
    ctx.closePath()
}

function drawEdge(edge) {
    ctx.strokeStyle = EDGE_COLOR
    ctx.lineWidth = 2
    ctx.beginPath()
    ctx.moveTo(edge.vertexIn.x, edge.vertexIn.y)
    ctx.lineTo(edge.vertexOut.x, edge.vertexOut.y)
    ctx.stroke()
    ctx.closePath()
}

function drawAllEdges() {
    for (let edge of preparedEdges) {
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