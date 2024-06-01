import json
from unittest.mock import patch

from app.utils.dto import GraphDTO


def test_post_graph_endpoint_should_return_200(client):
    with patch('app.services.graph_service.create_empty_graph') as mock_graph_service:
        # given
        # when
        response = client.post('/graph/', query_string={'graph_name': 'test_graph_name'})
        # then
        assert response.status_code == 200
        mock_graph_service.assert_called_once()


def test_post_graph_endpoint_should_return_404(client):
    with patch('app.services.graph_service.create_empty_graph') as mock_graph_service:
        # given
        # when
        response = client.post('/graph/', query_string={'wrong_key': 'test_graph_name'})
        # then
        assert response.status_code == 400
        mock_graph_service.assert_not_called()


def test_delete_graph_endpoint_should_return_200(client):
    with patch('app.services.graph_service.delete_graph') as mock_graph_service:
        # given
        # when
        response = client.delete('/graph/', query_string={'graph_id': 1})
        # then
        assert response.status_code == 200
        mock_graph_service.assert_called_once()


def test_delete_graph_endpoint_should_return_404(client):
    with patch('app.services.graph_service.delete_graph') as mock_graph_service:
        # given
        # when
        response = client.delete('/graph/', query_string={'wrong_key': 1})
        # then
        assert response.status_code == 400
        mock_graph_service.assert_not_called()


def test_get_graph_endpoint_should_return_200(client):
    with patch('app.services.graph_service.get_graph_by_id') as mock_graph_service:
        # given
        graph_dto = GraphDTO(1, name='test_graph', vertices=[], edges=[])
        mock_graph_service.return_value = graph_dto
        # when
        response = client.get('/graph/', query_string={'graph_id': 1})
        # then
        data = json.loads(response.data)
        assert response.status_code == 200
        assert response.data is not None
        assert data['id'] == graph_dto.id
        assert data['edges'] == graph_dto.edges
        assert data['vertices'] == graph_dto.vertices
        assert data['name'] == graph_dto.name
        mock_graph_service.assert_called_once()


def test_put_graph_endpoint_should_return_200(client):
    with patch('app.services.graph_service.update_graph_name') as mock_graph_service:
        # given
        # when
        response = client.put('/graph/', query_string={'graph_id': 1, 'name': 'updated_name'})
        # then
        assert response.status_code == 200
        mock_graph_service.assert_called_once()


def test_put_graph_endpoint_should_return_404(client):
    with patch('app.services.graph_service.update_graph_name') as mock_graph_service:
        # given
        # when
        response = client.put('/graph/', query_string={'wrong_key': 1, 'name': 'updated_name'})
        # then
        assert response.status_code == 400
        mock_graph_service.assert_not_called()


def test_get_graph_endpoint_should_return_404(client):
    with patch('app.services.graph_service.get_graph_by_id') as mock_graph_service:
        # given
        # when
        response = client.get('/graph/', query_string={'wrong_key': 1})
        # then
        assert response.status_code == 400
        mock_graph_service.assert_not_called()


def test_post_vertex_should_return_200(client):
    with patch('app.services.graph_service.add_vertex_to_graph') as mock_graph_service:
        # given
        # when
        response = client.post('/graph/vertex', query_string={'graph_id': 1, 'x': 512, 'y': 124})
        # then
        assert response.status_code == 200
        mock_graph_service.assert_called_once()


def test_post_vertex_should_return_400(client):
    with patch('app.services.graph_service.add_vertex_to_graph') as mock_graph_service:
        # given
        # when
        response = client.post('/graph/vertex', query_string={'wrong_key': 1, 'x': 512, 'y': 124})
        # then
        assert response.status_code == 400
        mock_graph_service.assert_not_called()


def test_delete_vertex_should_return_200(client):
    with patch('app.services.graph_service.delete_vertex_from_graph') as mock_graph_service:
        # given
        # when
        response = client.delete('/graph/vertex', query_string={'graph_id': 1})
        # then
        assert response.status_code == 200
        mock_graph_service.assert_called_once()


def test_delete_vertex_should_return_400(client):
    with patch('app.services.graph_service.delete_vertex_from_graph') as mock_graph_service:
        # given
        # when
        response = client.delete('/graph/vertex', query_string={'wrong_key': 1})
        # then
        assert response.status_code == 400
        mock_graph_service.assert_not_called()


def test_put_vertex_should_return_200(client):
    with patch('app.services.graph_service.update_vertex_position') as mock_graph_service:
        # given
        # when
        response = client.put('/graph/vertex', query_string={'vertex_id': 1, 'x': 512, 'y': 124})
        # then
        assert response.status_code == 200
        mock_graph_service.assert_called_once()


def test_put_vertex_should_return_400(client):
    with patch('app.services.graph_service.update_vertex_position') as mock_graph_service:
        # given
        # when
        response = client.put('/graph/vertex', query_string={'wrong_key': 1, 'x': 512, 'y': 124})
        # then
        assert response.status_code == 400
        mock_graph_service.assert_not_called()


def test_post_edge_should_return_200(client):
    with patch('app.services.graph_service.add_edge_to_graph') as mock_graph_service:
        # given
        # when
        response = client.post('/graph/edge', query_string={'graph_id': 1, 'vertex_in_id': 1, 'vertex_out_id': 2})
        # then
        assert response.status_code == 200
        mock_graph_service.assert_called_once()


def test_post_edge_should_return_400(client):
    with patch('app.services.graph_service.add_edge_to_graph') as mock_graph_service:
        # given
        # when
        response = client.post('/graph/edge', query_string={'wrong_key': 1, 'vertex_in_id': 1, 'vertex_out_id': 2})
        # then
        assert response.status_code == 400
        mock_graph_service.assert_not_called()


def test_delete_edge_should_return_200(client):
    with patch('app.services.graph_service.delete_edge_from_graph') as mock_graph_service:
        # given
        # when
        response = client.delete('/graph/edge', query_string={'edge_id': 1})
        # then
        assert response.status_code == 200
        mock_graph_service.assert_called_once()


def test_delete_edge_should_return_400(client):
    with patch('app.services.graph_service.delete_edge_from_graph') as mock_graph_service:
        # given
        # when
        response = client.delete('/graph/edge', query_string={'wrong_key': 1})
        # then
        assert response.status_code == 400
        mock_graph_service.assert_not_called()
