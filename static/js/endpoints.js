export async function fetchGraph(graphId) {
    try {
        const response = await fetch(`/graph?graph_id=${graphId}`, {
            method: 'GET'
        });

        if (response.ok) {
            const data = await response.json();
            return JSON.stringify(data);
        }

        const data = await response.json();
        return JSON.stringify(data);
    } catch (error) {
        console.error('There was a problem with the fetch graph operation:', error);
        throw error;
    }
}

export async function deleteGraphEndpoint(graphId) {
    try {
        const response = await fetch('/graph?graph_id=' + graphId, {
            method: 'DELETE',
        });

        if (response.ok) {
            return await graphId
        }

    } catch (error) {
        console.error('There was a problem with the deleting graph operation:', error);
        throw error;
    }
}

export async function createVertexEndpoint(graphId, x, y) {
    try {
        const response = await fetch(`/graph/vertex?graph_id=${graphId}&x=${x}&y=${y}`, {
            method: 'POST'
        })
        const data = await response.json()
        return JSON.stringify(data)
    } catch (error) {
        console.error('There was a problem with the adding vertex to graph operation:', error);
        throw error;
    }
}

export async function deleteVertexEndpoint(graphId, vertexId) {
    try {
        const response = await fetch(`/graph/vertex?graph_id=${graphId}&vertex_id=${vertexId}`, {
            method: 'DELETE'
        })
        if (response.ok) {
            return await graphId
        }
    } catch (error) {
        console.error('There was a problem with the deleting vertex operation:', error);
        throw error;
    }
}

export async function addEdgeEndpoint(graphId, vertexInId, vertexOutId) {
    try {
        const response = await fetch(`/graph/edge?graph_id=${graphId}&vertex_in_id=${vertexInId}&vertex_out_id=${vertexOutId}`, {
            method: 'POST'
        })
        const data = await response.json()
        return JSON.stringify(data)
    } catch (error) {
        console.error('There was a problem with the adding edge to graph operation:', error);
        throw error;
    }
}

export async function deleteEdgeEndpoint(graphId, edgeId) {
    try {
        const response = await fetch(`/graph/edge?edge_id=${edgeId}&graph_id=${graphId}`, {
            method: 'DELETE'
        })

        if (!response.ok) {
            throw new Error(`Failed to delete edge with ID ${edgeId}. Status: ${response.status}`);
        }


    } catch (error) {
        console.error('There was a problem with the deleting edge operation:', error);
        throw error;
    }
}

export async function createGraphEndpoint(graphName) {
    try {
        const response = await fetch(`/graph?graph_name=${graphName}`, {
            method: 'POST'
        })
        if (!response.ok) {
            throw new Error(`Failed to create graph. Status: ${response.status}`);
        }
        const responseData = await response.json();
        return responseData.graph_id;
    } catch (error) {
        console.error('There was a problem with the create graph operation:', error);
        throw error;
    }
}

export async function updateVertexCoordsEndpoint(graphId, vertexId, newX, newY) {
    try {
        const response = await fetch(`/graph/vertex?graph_id=${graphId}&vertex_id=${vertexId}&x=${newX}&y=${newY}`, {
            method: 'PUT'
        })
        if (!response.ok) {
            throw new Error(`Failed to save new vertex coords`);
        }

    } catch (error) {
        console.error('There was a problem with saving new vertex coords:', error);
        throw error;
    }
}