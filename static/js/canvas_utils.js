const VERTEX_RADIUS = 10

export function prepareVerticesToDraw(vertices) {
    let preparedVertices = []
    vertices.forEach(vertex => {
        let preparedVertex = prepareVertexToDraw(vertex)
        preparedVertices.push(preparedVertex)
    })
    return preparedVertices
}

function prepareVertexToDraw(vertex) {
    let preparedVertex = {}
    preparedVertex.id = vertex.id
    preparedVertex.x = vertex.x
    preparedVertex.y = vertex.y
    return preparedVertex
}

export function prepareEdgesToDraw(edges, preparedVertices) {
    let preparedEdges = []
    edges.forEach(edge => {
        let preparedEdge = prepareEdgeToDraw(edge, preparedVertices)
        preparedEdges.push(preparedEdge)
    })
    return preparedEdges
}

function prepareEdgeToDraw(edge, preparedVertices) {
    let preparedEdge = {}
    let preparedVerticesForEdge = findPreparedVerticesForEdge(edge, preparedVertices)
    preparedEdge.id = edge.id
    preparedEdge.vertexIn = preparedVerticesForEdge.vertexIn
    preparedEdge.vertexOut = preparedVerticesForEdge.vertexOut
    return preparedEdge
}

function findPreparedVerticesForEdge(edge, preparedVertices) {
    let verticesForEdge = {}
    preparedVertices.forEach(vertex => {
        if (vertex.id === edge.vertex_in.id)
            verticesForEdge.vertexIn = vertex
        if (vertex.id === edge.vertex_out.id)
            verticesForEdge.vertexOut = vertex
    })
    return verticesForEdge
}