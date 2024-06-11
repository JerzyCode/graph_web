import {fetchGraph, updateVertexCoordsEndpoint} from "./endpoints.js";
import {showAddVertexPopup, showDeleteEdgePopup, showGraphActionsPopup} from "./graph_panel.js";
import {prepareEdgesToDraw, prepareEdgeToDraw} from "./canvas_utils.js";
import {addEdgeParams, addVertexParams, deleteEdgeParams, deleteVertexParams, selectedVertexId} from "./modify_graph_service.js";

const canvas = document.getElementById("canvas")
const container = document.getElementById("canvas-container")
const ctx = canvas.getContext('2d')

const VERTEX_BORDER_COLOR = '#2dcebc'
const VERTEX_FILL_COLOR = '#0b5351'
const VERTEX_REPAINT_COLOR = '#d90368'
const VERTEX_TO_EDGE_COLOR = ' yellow'
const VERTEX_RADIUS = 12
const EDGE_WIDTH = 3
const EDGE_COLOR = '#2dcebc'
const EDGE_REPAINT_COLOR = '#d90368'


let graph
let vertices = []
let verticesColor = new Map()
let edgesColor = new Map()
let edges = []
let currentVertex = null
let isDragging = false
let selectedVertices = []


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
    console.debug(`loadGraphOnCanvas(), graphId=${graphId}`)
    vertices = graph.vertices
    edges = prepareEdgesToDraw(graph.edges, vertices)
    mapVerticesColor()
    mapEdgesColor()
    redrawGraph()
}

function mapVerticesColor() {
    for (let vertex of vertices) {
        verticesColor.set(vertex.id, VERTEX_FILL_COLOR)
    }
}

function mapEdgesColor() {
    for (let edge of edges) {
        edgesColor.set(edge.id, EDGE_COLOR)
    }
}


function handleMouseDown(event) {

    if (event.button !== 0) {
        return;
    }

    event.preventDefault()
    for (let vertex of vertices) {
        if (isMouseOnVertex(event, vertex)) {
            currentVertex = vertex
            isDragging = true
            console.log(vertex)
            return
        }
    }
}

function isMouseOnVertex(event, vertex) {
    let canvasCoords = calculateCoordsOnCanvas(event)
    const dx = canvasCoords.x - vertex.x
    const dy = canvasCoords.y - vertex.y
    return dx * dx + dy * dy <= VERTEX_RADIUS * VERTEX_RADIUS
}

function handleStopDragging(event) {
    if (!isDragging) {
        return
    }
    updateVertexPosition()
    event.preventDefault()
    isDragging = false
}

function updateVertexPosition() {
    updateVertexCoordsEndpoint(currentVertex.id, currentVertex.x, currentVertex.y)
        .then(() => {
            console.log('Updated vertex position: ' + currentVertex.id)
            currentVertex = null
        })
}

function handleMouseMove(event) {
    canvas.style.cursor = 'default'
    let canvasCoords = calculateCoordsOnCanvas(event)

    mouseOnVertexEvent(event)
    mouseOnEdgeEvent(event)
    if (isDragging) {
        if (canvasCoords.x < VERTEX_RADIUS || canvasCoords.x > canvas.width - VERTEX_RADIUS ||
            canvasCoords.y < VERTEX_RADIUS || canvasCoords.y > canvas.height - VERTEX_RADIUS) {
            return
        }
        canvas.style.cursor = 'grab'
        currentVertex.x = canvasCoords.x
        currentVertex.y = canvasCoords.y
        repaint()
    }
}

function mouseOnVertexEvent(event) {
    for (let vertex of vertices) {
        let isSelected = isVertexSelected(vertex)
        if (isMouseOnVertex(event, vertex)) {
            if (!isSelected) {
                verticesColor.set(vertex.id, VERTEX_REPAINT_COLOR)
            }
            canvas.style.cursor = 'pointer'
        } else if (isSelected) {
            //no change color for selected
        } else {
            verticesColor.set(vertex.id, VERTEX_FILL_COLOR)
        }
    }
    repaint()
}


function isVertexSelected(vertex) {
    for (let selected of selectedVertices) {
        if (selected === vertex.id) {
            return true
        }
    }
    return false
}

function mouseOnEdgeEvent(event) {
    let canvasCoords = calculateCoordsOnCanvas(event)
    for (let edge of edges) {
        if (isMouseOnEdge(edge, canvasCoords)) {
            edgesColor.set(edge.id, EDGE_REPAINT_COLOR)
            canvas.style.cursor = 'pointer'
        } else {
            edgesColor.set(edge.id, EDGE_COLOR)
        }
    }
    repaint()
}

function isMouseOnEdge(edge, canvasCoords) {
    let minX = Math.min(edge.vertex_in.x, edge.vertex_out.x)
    let maxX = Math.max(edge.vertex_in.x, edge.vertex_out.x)
    let minY = Math.min(edge.vertex_in.y, edge.vertex_out.y)
    let maxY = Math.max(edge.vertex_in.y, edge.vertex_out.y)
    if (canvasCoords.x < minX || canvasCoords.x > maxX || canvasCoords.y < minY || canvasCoords.y > maxY) {
        return
    }
    calculateDistanceFromMouseToEdgeLine(edge, canvasCoords)
    let distance = calculateDistanceFromMouseToEdgeLine(edge, canvasCoords)
    // return true
    return Math.abs(distance - EDGE_WIDTH) <= 10;
}

function calculateDistanceFromMouseToEdgeLine(edge, canvasCoords) {
    let x1 = edge.vertex_in.x
    let y1 = edge.vertex_in.y
    let x2 = edge.vertex_out.x
    let y2 = edge.vertex_out.y

    // Line coefficients
    let A = (y2 - y1)
    let B = -(x2 - x1)
    let C = x2 * y1 - y2 * x1
    let nominator = Math.abs(A * canvasCoords.x + B * canvasCoords.y + C)
    let denominator = Math.sqrt(A * A + B * B)
    return nominator / denominator
}


function handleRightClick(event) {
    event.preventDefault()
    if (graph == null) {
        return
    }
    let canvasCoords = calculateCoordsOnCanvas(event)
    console.debug(`pressed RightClick() on coords: ${canvasCoords.x}, ${canvasCoords.y}`)

    let pressedVertex = returnPressedVertex(event)
    let pressedEdge = returnPressedEdge(event)
    if (pressedVertex != null) {
        onCanvasShowGraphActionsPopup(event)
        setGraphOptionsParams(pressedVertex)
    } else if (pressedEdge != null) {
        deleteEdgeParams.edgeId = pressedEdge.id
        onCanvasShowDeleteEdgePopup(event)
    } else {
        onCanvasShowAddVertexPopup(canvasCoords, event)
    }
}

function setGraphOptionsParams(pressedVertex) {
    deleteVertexParams.graphId = graph.id
    deleteVertexParams.vertexId = pressedVertex.id
    selectedVertexId.vertexId = pressedVertex.id
    addEdgeParams.graphId = graph.id
}

function returnPressedVertex(event) {
    for (let vertex of vertices) {
        if (isMouseOnVertex(event, vertex)) {
            return vertex
        }
    }
    return null
}

function returnPressedEdge(event) {
    let canvasCoords = calculateCoordsOnCanvas(event)
    for (let edge of edges) {
        if (isMouseOnEdge(edge, canvasCoords)) {
            return edge
        }
    }
    return null
}

function onCanvasShowGraphActionsPopup(event) {
    showGraphActionsPopup(event.x, event.y)
}

function onCanvasShowDeleteEdgePopup(event) {
    showDeleteEdgePopup(event.x, event.y)
}

function onCanvasShowAddVertexPopup(canvasCoords, event) {
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

function drawVertexSetColor(vertex, color) {
    ctx.fillStyle = color
    ctx.strokeStyle = VERTEX_BORDER_COLOR
    ctx.lineWidth = EDGE_WIDTH
    ctx.beginPath()
    ctx.arc(vertex.x, vertex.y, VERTEX_RADIUS, 0, Math.PI * 2)
    ctx.fill()
    ctx.stroke()
    ctx.closePath()
}

function drawVertex(vertex) {
    drawVertexSetColor(vertex, verticesColor.get(vertex.id))
}

export function drawEdge(edge) {
    ctx.strokeStyle = edgesColor.get(edge.id)
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

export function addEdgeOnCanvas(edge) {
    let preparedEdge = prepareEdgeToDraw(edge, vertices)
    edges.push(preparedEdge)
    repaint()
}


export function addVertexOnCanvas(vertex) {
    console.debug(`addVertexOnCanvas(), vertex=${JSON.stringify(vertex)}`)
    vertices.push(vertex)
    verticesColor.set(vertex.id, VERTEX_FILL_COLOR)
    repaint()
}

export function deleteVertexOnCanvas(vertexId) {
    vertices = vertices.filter(vertex => vertex.id !== vertexId);
    deleteEdgesIncidental(vertexId)
    repaint()
}

export function deleteEdgesIncidental(vertexId) {
    edges = edges.filter(edge => edge.vertex_in.id !== vertexId && edge.vertex_out.id !== vertexId)
}

export function markVertexSelected(vertexId) {
    verticesColor.set(vertexId, VERTEX_TO_EDGE_COLOR)
    selectedVertices.push(vertexId)
    repaint()
}

export function backVertexBgToDefault(vertexId) {
    verticesColor.set(vertexId, VERTEX_FILL_COLOR)
    redrawGraph()
}


export function unmarkSelectedVertices() {
    for (let selected of selectedVertices) {
        backVertexBgToDefault(selected)
    }
    selectedVertices = []
}

export function deleteEdgeOnCanvas(edgeId) {
    edges = edges.filter(edge => edge.id !== edgeId)
    repaint()
}
