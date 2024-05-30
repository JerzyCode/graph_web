from app.app import db


class Vertex(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    x = db.Column(db.Float)
    y = db.Column(db.Float)

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def to_dict(self):
        return {
            'id': self.id,
            'x': self.x,
            'y': self.y
        }