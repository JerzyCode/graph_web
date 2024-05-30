from app.app import db
from app.utils.constants import VERTEX_ID_COLUMN, VERTEX_TABLE_NAME

neighbors_table = db.Table('neighbors_table',
                           db.Column('vertex_id', db.Integer, db.ForeignKey(VERTEX_ID_COLUMN), primary_key=True),
                           db.Column('neighbor_id', db.Integer, db.ForeignKey(VERTEX_ID_COLUMN), primary_key=True))


class Vertex(db.Model):
    __tablename__ = VERTEX_TABLE_NAME

    id = db.Column(db.Integer, primary_key=True)
    x = db.Column(db.Float)
    y = db.Column(db.Float)
    neighbors = db.relationship('Vertex', secondary='neighbors_table',
                                primaryjoin=id == neighbors_table.c.vertex_id,
                                secondaryjoin=id == neighbors_table.c.neighbor_id,
                                backref='connected_to')

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.neighbors = []

    def to_dict(self):
        return {
            'id': self.id,
            'x': self.x,
            'y': self.y,
            'neighbors': self.neighbors
        }


class Edge(db.Model):
    __tablename__ = 'edge_table'

    id = db.Column(db.Integer, primary_key=True)
    vertex_out_id = db.Column(db.Integer, db.ForeignKey(VERTEX_ID_COLUMN))
    vertex_in_id = db.Column(db.Integer, db.ForeignKey(VERTEX_ID_COLUMN))

    vertex_out = db.relationship('Vertex', foreign_keys=[vertex_out_id])
    vertex_in = db.relationship('Vertex', foreign_keys=[vertex_in_id])

    def __init__(self, vertex_in, vertex_out):
        self.vertex_in = vertex_in
        self.vertex_in_id = vertex_in.id
        self.vertex_out = vertex_out
        self.vertex_out_id = vertex_out.id

    def to_dict(self):
        return {
            'id': self.id,
            'vertex_from': self.vertex_from,
            'vertex_to': self.vertex_to
        }
