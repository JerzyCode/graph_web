// export async function fetchGraph(graph_id) {
//     return fetch('/graph?graph_id=' + graph_id, {
//         method: 'GET',
//         headers: {
//             'Content-Type': 'application/json'
//         }
//     })
//         .then(response => {
//             if (!response.ok) {
//                 throw new Error('Network response was not ok ' + response.statusText);
//             }
//             return response.json();
//         })
//         .then(data => {
//             console.log(data);
//             return data;
//         })
//         .catch(error => {
//             console.error('There was a problem with the fetch operation:', error);
//             throw error;
//         });
// }

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

        const data = await response.json();
        console.log(data);
        return data;
    } catch (error) {
        console.error('There was a problem with the fetch operation:', error);
        throw error;
    }
}