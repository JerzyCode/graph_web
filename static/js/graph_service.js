export async function fetchGraph(graph_id) {
    try {
        const response = await fetch('/graph?graph_id=' + graph_id, {
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