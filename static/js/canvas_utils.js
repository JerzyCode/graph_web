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
    preparedEdge.vertex_in = preparedVerticesForEdge.vertex_in
    preparedEdge.vertex_out = preparedVerticesForEdge.vertex_out
    return preparedEdge
}

function findPreparedVerticesForEdge(edge, preparedVertices) {
    let verticesForEdge = {}
    preparedVertices.forEach(vertex => {
        if (vertex.id === edge.vertex_in.id)
            verticesForEdge.vertex_in = vertex
        if (vertex.id === edge.vertex_out.id)
            verticesForEdge.vertex_out = vertex
    })
    return verticesForEdge
}