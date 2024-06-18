from typing import List


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


class VertexAlgorithm:
    def __init__(self, id):
        self.id = id
        self.neighbors = []

    def add_neighbor(self, neighbor):
        self.neighbors.append(neighbor)

    def __str__(self):
        neigh_str = ''
        for neighbor in self.neighbors:
            neigh_str += str(neighbor.id) + ', '
        return f'VertexAlgorithm (id: {self.id}, neighbors=[{neigh_str}])'


class EdgeAlgorithm:
    def __init__(self, id, vertex_in: VertexAlgorithm, vertex_out: VertexAlgorithm):
        self.id = id
        self.vertex_in = vertex_in
        self.vertex_out = vertex_out

    def __str__(self):
        return f'EdgeAlgorithm (id: {self.id}, vertex_in: {self.vertex_in.id}, vertex_out: {self.vertex_out.id})'


class GraphAlgorithm:
    def __init__(self, vertices: List[VertexAlgorithm], edges: List[EdgeAlgorithm]):
        self.vertices = vertices
        self.edges = edges

    def __str__(self):
        vertices_str = ''
        edges_str = ''
        for vertex in self.vertices:
            vertices_str += str(vertex) + ', \n'
        for edge in self.edges:
            edges_str += str(edge) + ', \n'
        return vertices_str + '\n' + edges_str + '\n'
