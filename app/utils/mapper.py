from typing import List, Dict

from app.models import Graph, Vertex
from app.utils.classes import VertexAlgorithm, EdgeAlgorithm, GraphAlgorithm


def algorithm_graph_of_model_graph(graph: Graph):
    vertices = graph.vertices.all()
    edges = graph.edges.all()

    prepared_vertices_map = _prepare_vertices_map_for_algorithm(vertices)
    prepared_vertices = _prepare_vertices_for_algorithm(vertices, prepared_vertices_map)
    prepared_edges = _prepare_edges_for_algorithm(edges, prepared_vertices_map)

    return GraphAlgorithm(prepared_vertices, prepared_edges)


def _prepare_edges_for_algorithm(edges, mapped_vertices: Dict[int, VertexAlgorithm]) -> List[EdgeAlgorithm]:
    prepared_edges = []
    for edge in edges:
        new_edge = EdgeAlgorithm(
            id=edge.id,
            vertex_in=mapped_vertices[edge.vertex_in.id],
            vertex_out=mapped_vertices[edge.vertex_out.id]
        )
        prepared_edges.append(new_edge)
    return prepared_edges


def _prepare_vertices_for_algorithm(vertices: List[Vertex], mapped_vertices: Dict[int, VertexAlgorithm]) -> List[VertexAlgorithm]:
    prepared_vertices = []
    for vertex in vertices:
        _add_neighbors_to_vertex_algorithm(vertex.neighbors, mapped_vertices[vertex.id], mapped_vertices)
        prepared_vertices.append(mapped_vertices[vertex.id])
    return prepared_vertices


def _prepare_vertices_map_for_algorithm(vertices: List[Vertex]) -> Dict[int, VertexAlgorithm]:
    prepared_vertices_map = {}

    for vertex in vertices:
        prepared_vertices_map[vertex.id] = _vertex_algorithm_of_vertex_model(vertex)

    return prepared_vertices_map


def _add_neighbors_to_vertex_algorithm(neighbors: List[Vertex], vertex_algorithm: VertexAlgorithm,
                                       mapped_vertices: Dict[int, VertexAlgorithm]):
    for neighbor in neighbors:
        vertex_algorithm.add_neighbor(mapped_vertices[neighbor.id])


def _vertex_algorithm_of_vertex_model(vertex: Vertex) -> VertexAlgorithm:
    return VertexAlgorithm(vertex.id)
