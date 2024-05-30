const canvas = document.getElementById("canvas")
const container = document.getElementById("canvas-container")
const ctx = canvas.getContext('2d')

const VERTEX_RADIUS = 10

const vertices = []
const edges = []
let current_vertex = null
let is_dragging = false

canvas.width = container.clientWidth
canvas.height = container.clientHeight

initializeGraph()


canvas.onmousedown = handleMouseDown
canvas.onmouseup = handleStopDragging
canvas.onmouseout = handleStopDragging
canvas.onmousemove = handleMouseMove

window.addEventListener('resize', repaint)

drawAllEdges()
drawAllVertices()

function drawVertex(vertex) {
    ctx.fillStyle = 'yellow'
    ctx.strokeStyle = 'red'
    ctx.lineWidth = 2
    ctx.beginPath()
    ctx.arc(vertex.x, vertex.y, VERTEX_RADIUS, 0, Math.PI * 2)
    ctx.fill()
    ctx.stroke()
    ctx.closePath()
}

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

function drawEdge(edge) {
    ctx.strokeStyle = 'red'
    ctx.lineWidth = 2
    ctx.beginPath()
    ctx.moveTo(edge.vertex1.x, edge.vertex1.y)
    ctx.lineTo(edge.vertex2.x, edge.vertex2.y)
    ctx.stroke()
    ctx.closePath()
}

function drawAllEdges() {
    for (let edge of edges) {
        drawEdge(edge)
    }
}

function drawAllVertices() {
    for (let vertex of vertices) {
        drawVertex(vertex)
    }
}

function repaint() {
    ctx.clearRect(0, 0, canvas.width, canvas.height)
    drawAllEdges()
    drawAllVertices()
}


function isVertexPressed(event, vertex, radius) {
    let rect = canvas.getBoundingClientRect()
    let x_canvas = event.x - rect.left
    let y_canvas = event.y - rect.top
    const dx = x_canvas - vertex.x
    const dy = y_canvas - vertex.y
    return dx * dx + dy * dy <= radius * radius
}

function handleMouseDown(event) {
    event.preventDefault()
    for (let vertex of vertices) {
        if (isVertexPressed(event, vertex, VERTEX_RADIUS)) {
            current_vertex = vertex
            is_dragging = true
            return
        }
    }
}

function handleStopDragging(event) {
    if (!is_dragging) {
        return
    }

    event.preventDefault()
    current_vertex = null
    is_dragging = false
}

function handleMouseMove(event) {
    let rect = canvas.getBoundingClientRect()
    let x_canvas = event.x - rect.left
    let y_canvas = event.y - rect.top
    if (is_dragging) {
        if (x_canvas < VERTEX_RADIUS || x_canvas > canvas.width - VERTEX_RADIUS ||
            y_canvas < VERTEX_RADIUS || y_canvas > canvas.height - VERTEX_RADIUS) {
            return
        }
        current_vertex.x = x_canvas
        current_vertex.y = y_canvas
        repaint()
    }
}
