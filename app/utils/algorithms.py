from typing import List

from app.utils.classes import GraphAlgorithm, VertexAlgorithm, ObjectToColor
from app.utils.constants import VERTEX, EDGE


def depth_search(graph: GraphAlgorithm) -> List[ObjectToColor]:
    visited = {}
    vertices = graph.vertices
    objects_to_color = []
    for vertex in vertices:
        visited[vertex] = False
    for vertex in vertices:
        if not visited[vertex]:
            _dfs(vertex, graph, visited, objects_to_color)
    return objects_to_color


def _dfs(vertex: VertexAlgorithm, graph: GraphAlgorithm, visited, objects_to_color: List):
    visited[vertex] = True
    print('vertex=' + str(vertex))
    objects_to_color.append(ObjectToColor(vertex.id, VERTEX))
    for neighbor in vertex.neighbors:
        if not visited[neighbor]:
            edge = _find_edge(vertex_in=vertex, vertex_out=neighbor, edges=graph.edges)
            objects_to_color.append(ObjectToColor(edge.id, EDGE))
            _dfs(neighbor, graph, visited, objects_to_color)


def _find_edge(vertex_in: VertexAlgorithm, vertex_out: VertexAlgorithm, edges):
    for edge in edges:
        if edge.vertex_in == vertex_in and edge.vertex_out == vertex_out:
            return edge
