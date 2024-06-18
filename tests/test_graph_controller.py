import json
from unittest.mock import patch

from app.models import Vertex, Edge, User
from app.utils.classes import GraphDTO
from app.utils.exceptions import UserGraphCountExceededException, GraphVertexCountExceededException, EdgeAlreadyExistsException
from tests import helper_test


def test_post_graph_endpoint_should_return_200(client):
    with patch('app.services.graph_service.create_empty_graph') as mock_graph_service:
        # given
        mock_graph_service.return_value = 123
        # when
        with patch('flask_login.utils._get_user', return_value=helper_test.get_mock_user()):
            response = client.post('/graph/', query_string={'graph_name': 'test_graph_name'})
        # then
        assert response.status_code == 200
        mock_graph_service.assert_called_once()


def test_post_graph_endpoint_should_return_404(client):
    with patch('app.services.graph_service.create_empty_graph') as mock_graph_service:
        # given
        with patch('flask_login.utils._get_user', return_value=User()):
            # when
            response = client.post('/graph/', query_string={'wrong_key': 'test_graph_name'})
            # then
            assert response.status_code == 400
            mock_graph_service.assert_not_called()


def test_post_graph_endpoint_should_return_400(client):
    with patch('app.services.graph_service.create_empty_graph') as mock_graph_service:
        # given
        mock_graph_service.side_effect = UserGraphCountExceededException
        # when
        with patch('flask_login.utils._get_user', return_value=helper_test.get_mock_user()):
            response = client.post('/graph/', query_string={'graph_name': 'test_graph_name'})
        # then
        assert response.status_code == 400
        mock_graph_service.assert_called_once()


def test_delete_graph_endpoint_should_return_200(client, app):
    with patch('app.services.graph_service.delete_graph') as mock_graph_service:
        # given
        with app.app_context():
            graph = helper_test.get_empty_test_graph_in_db()
        # when
        with patch('flask_login.utils._get_user', return_value=helper_test.get_mock_user()):
            response = client.delete('/graph/', query_string={'graph_id': graph.id})
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


def test_get_graph_endpoint_should_return_200(client, app):
    with patch('app.services.graph_service.get_graph_by_id') as mock_graph_service:
        # given
        with app.app_context():
            graph = helper_test.get_empty_test_graph_in_db()
        graph_dto = GraphDTO(1, name='test_graph', vertices=[], edges=[])
        mock_graph_service.return_value = graph_dto
        # when
        with patch('flask_login.utils._get_user', return_value=helper_test.get_mock_user()):
            response = client.get('/graph/', query_string={'graph_id': graph.id})
        # then
        data = json.loads(response.data)
        assert response.status_code == 200
        assert response.data is not None
        assert data['id'] == graph_dto.id
        assert data['edges'] == graph_dto.edges
        assert data['vertices'] == graph_dto.vertices
        assert data['name'] == graph_dto.name
        mock_graph_service.assert_called_once()


def test_put_graph_endpoint_should_return_200(client, app):
    with patch('app.services.graph_service.update_graph_name') as mock_graph_service:
        # given
        with app.app_context():
            graph = helper_test.get_empty_test_graph_in_db()
        # when
        with patch('flask_login.utils._get_user', return_value=helper_test.get_mock_user()):
            response = client.put('/graph/', query_string={'graph_id': graph.id, 'name': 'updated_name'})
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


def test_post_vertex_should_return_200(client, app):
    with patch('app.services.graph_service.add_vertex_to_graph') as mock_graph_service:
        # given
        with app.app_context():
            graph = helper_test.get_empty_test_graph_in_db()
        mock_graph_service.return_value = Vertex(graph_id=graph.id, x=512, y=124)
        # when
        with patch('flask_login.utils._get_user', return_value=helper_test.get_mock_user()):
            response = client.post('/graph/vertex', query_string={'graph_id': graph.id, 'x': 512, 'y': 124}, content_type='application/json')
        # then
        assert response.status_code == 200
        mock_graph_service.assert_called_once()


def test_post_vertex_for_graph_exceed_count_should_return_400(client, app):
    with patch('app.services.graph_service.add_vertex_to_graph') as mock_graph_service:
        # given
        with app.app_context():
            graph = helper_test.get_empty_test_graph_in_db()
        mock_graph_service.side_effect = GraphVertexCountExceededException
        # when
        with patch('flask_login.utils._get_user', return_value=helper_test.get_mock_user()):
            response = client.post('/graph/vertex', query_string={'graph_id': graph.id, 'x': 512, 'y': 124}, content_type='application/json')
        # then
        assert response.status_code == 400
        mock_graph_service.assert_called_once()


def test_post_vertex_should_return_400(client):
    with patch('app.services.graph_service.add_vertex_to_graph') as mock_graph_service:
        # given
        # when
        response = client.post('/graph/vertex', query_string={'wrong_key': 1, 'x': 512, 'y': 124})
        # then
        assert response.status_code == 400
        mock_graph_service.assert_not_called()


def test_delete_vertex_should_return_200(client, app):
    with patch('app.services.graph_service.delete_vertex_from_graph') as mock_graph_service:
        # given
        with app.app_context():
            graph = helper_test.get_empty_test_graph_in_db()
        # when
        with patch('flask_login.utils._get_user', return_value=helper_test.get_mock_user()):
            response = client.delete('/graph/vertex', query_string={'graph_id': graph.id, 'vertex_id': 1})
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


def test_put_vertex_should_return_200(client, app):
    with patch('app.services.graph_service.update_vertex_position') as mock_graph_service:
        # given
        with app.app_context():
            graph = helper_test.get_empty_test_graph_in_db()
        # when
        with patch('flask_login.utils._get_user', return_value=helper_test.get_mock_user()):
            response = client.put('/graph/vertex', query_string={'graph_id': graph.id, 'vertex_id': 1, 'x': 512, 'y': 124})
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


def test_post_edge_should_return_200(client, app):
    with patch('app.services.graph_service.add_edge_to_graph') as mock_graph_service:
        # given
        with app.app_context():
            graph = helper_test.get_empty_test_graph_in_db()
        mock_graph_service.return_value = Edge(vertex_in=Vertex(0, 0, graph.id), vertex_out=Vertex(0, 0, graph.id), graph_id=graph.id)
        # when
        with patch('flask_login.utils._get_user', return_value=helper_test.get_mock_user()):
            response = client.post('/graph/edge', query_string={'graph_id': graph.id, 'vertex_in_id': 1, 'vertex_out_id': 2})
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


def test_post_edge_should_return_400_edge_exists(client, app):
    with patch('app.services.graph_service.add_edge_to_graph') as mock_graph_service:
        # given
        with app.app_context():
            graph = helper_test.get_test_graph_with_multiple_edges_in_db()
            edge = graph.edges.first()
        mock_graph_service.side_effect = EdgeAlreadyExistsException
        # when
        with patch('flask_login.utils._get_user', return_value=helper_test.get_mock_user()):
            response = client.post('/graph/edge', query_string={'graph_id': graph.id,
                                                                'vertex_in_id': edge.vertex_in_id, 'vertex_out_id': edge.vertex_out_id})
        # then
        assert response.status_code == 400
        mock_graph_service.assert_called_once()


def test_delete_edge_should_return_200(client, app):
    # given
    with app.app_context():
        graph = helper_test.get_test_graph_with_edges_in_db()
        edge_to_delete = graph.edges.first()
    # when
    with patch('flask_login.utils._get_user', return_value=helper_test.get_mock_user()):
        with patch('app.services.graph_service.delete_edge_from_graph') as mock_graph_service:
            response = client.delete('/graph/edge', query_string={'edge_id': edge_to_delete.id, 'graph_id': graph.id})
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
