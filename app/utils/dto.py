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
            'edges': [edge.to_dict() for edge in self.edges],
            'vertices': [vertex.to_dict() for vertex in self.vertices]
        }
