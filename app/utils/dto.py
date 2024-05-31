class GraphDTO:
    def __init__(self, id, name, vertices, edges):
        self.id = id
        self.name = name
        self.edges = edges
        self.vertices = vertices

    def map_to_dictionary(self):
        return {
            'id': self.id,
            'name': self.name,
            'edges': self.edges,
            'vertices': self.vertices
        }
