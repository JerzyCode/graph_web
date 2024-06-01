import {prepareEdgesToDraw, prepareVerticesToDraw} from "./canvas_utils.js";

const canvas = document.getElementById("canvas")
const container = document.getElementById("canvas-container")
const ctx = canvas.getContext('2d')

const VERTEX_BORDER_COLOR = 'purple'
const VERTEX_FILL_COLOR = 'yellow'
const VERTEX_RADIUS = 10

const vertices = []
const edges = []
let currentVertex = null
let isDragging = false
initializeGraph()


canvas.width = container.clientWidth
canvas.height = container.clientHeight


canvas.onmousedown = handleMouseDown
canvas.onmouseup = handleStopDragging
canvas.onmouseout = handleStopDragging
canvas.onmousemove = handleMouseMove

window.addEventListener('resize', repaint)

let preparedVertices = prepareVerticesToDraw(vertices)
let preparedEdges = prepareEdgesToDraw(edges, preparedVertices)

drawAllEdges()
drawAllVertices()

function initializeGraph() {
    vertices.push({id: 0, x: VERTEX_RADIUS, y: VERTEX_RADIUS})

    for (let i = 0; i < 12; i++) {
        vertices.push({id: i, x: getRandom(), y: getRandom()})

    }
    for (let i = 0; i <= 11; i++) {
        edges.push({vertex1: vertices[0], vertex2: vertices[i]})
        edges.push({vertex1: vertices[1], vertex2: vertices[i]})
    }

    edges.push({vertex1: vertices[0], vertex2: vertices[2]})
    edges.push({vertex1: vertices[0], vertex2: vertices[1]})
    edges.push({vertex1: vertices[0], vertex2: vertices[3]})
    edges.push({vertex1: vertices[0], vertex2: vertices[4]})
    edges.push({vertex1: vertices[0], vertex2: vertices[5]})
    edges.push({vertex1: vertices[0], vertex2: vertices[6]})
}

function getRandom() {
    return Math.floor(Math.random() * (500 - 25 + 1)) + 25;
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

function repaint() {
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
    ctx.strokeStyle = 'red'
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


