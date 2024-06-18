import json
from unittest.mock import patch

from app.utils.classes import ObjectToColor
from app.utils.constants import EDGE, VERTEX
from tests import helper_test


def test_dfs_endpoint(client):
    # given
    with patch('app.services.algorithm_service.run_dfs_algorithm') as mock_dfs:
        graph_id = 1
        edge_ret = ObjectToColor(1, EDGE)
        vertex_ret = ObjectToColor(1, VERTEX)
        mock_dfs.return_value = [edge_ret, vertex_ret]
        # when
        with patch('flask_login.utils._get_user', return_value=helper_test.get_mock_user()):
            response = client.get('/algorithm/dfs', query_string={'graph_id': graph_id})
        # then
        data = json.loads(response.data)
        assert response.status_code == 200
        assert data is not None
        assert len(data) == 2
        assert data[0] == edge_ret.to_dict()
        assert data[1] == vertex_ret.to_dict()


def test_dfs_endpoint_no_graph_id(client):
    # given
    with patch('app.services.algorithm_service.run_dfs_algorithm') as mock_dfs:
        mock_dfs.return_value = []
        # when
        with patch('flask_login.utils._get_user', return_value=helper_test.get_mock_user()):
            response = client.get('/algorithm/dfs', query_string={'wrong_key': 123})
        # then
        assert response.status_code == 400
