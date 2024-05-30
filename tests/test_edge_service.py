from app.app import db
from app.models import Edge

from app.services import edge_service as edge_service
from tests import helper


def test_save_edge(app):
    with app.app_context():
        # given
        vertex_in = helper.get_test_vertex_in_db()
        vertex_out = helper.get_test_vertex_in_db()
        # when
        edge_service.save_edge(vertex_in, vertex_out)
        # then
        saved_edge = Edge.query.first()
        assert saved_edge.vertex_in_id == vertex_in.id
        assert saved_edge.vertex_out_id == vertex_out.id
        assert saved_edge.vertex_in == vertex_in
        assert saved_edge.vertex_out == vertex_out


def test_delete_edge(app):
    with app.app_context():
        # given
        vertex_in = helper.get_test_vertex_in_db()
        vertex_out = helper.get_test_vertex_in_db()
        edge = Edge(vertex_in, vertex_out)
        db.session.add(edge)
        db.session.commit()
        saved_edge = Edge.query.get(edge.id)
        # when
        edge_service.delete_edge(saved_edge.id)
        # then
        assert Edge.query.get(edge.id) is None
