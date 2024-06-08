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