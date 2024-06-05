export async function fetchGraph(graphId) {
    try {
        const response = await fetch('/graph?graph_id=' + graphId, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (!response.ok) {
            throw new Error('Network response was not ok ' + response.statusText);
        }

        return await response.json();
    } catch (error) {
        console.error('There was a problem with the fetch graph operation:', error);
        throw error;
    }
}

export async function deleteGraph(graphId) {
    try {
        const response = await fetch('/graph?graph_id=' + graphId, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (!response.ok) {
            throw new Error('Network response was not ok ' + response.statusText);
        }

        return await graphId
    } catch (error) {
        console.error('There was a problem with the deleting graph operation:', error);
        throw error;
    }
}

export async function createVertexEndpoint(graphId, x, y) {
    try {
        const response = await fetch(`/graph/vertex?graph_id=${graphId}&x=${x}&y=${y}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        return response
    } catch (error) {
        console.error('There was a problem with the adding vertex to graph operation:', error);
        throw error;
    }
}