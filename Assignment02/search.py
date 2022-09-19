# CS6033 - Artificial Intelligence
# Fall 2022
# Scott Fasone
# Assignment 02

# Homework Group 14
#  - Adonia Jebessa
#  - Breanna King
#  - Mohammad Yahiya Khan
#  - Scott Fasone



from abc import ABC, abstractmethod
from typing import Callable, Tuple



class GraphNode:
    def __init__(self, label: str) -> None:
        self.label = label
        self.edges = [] # type: list[Tuple[GraphNode, float]]
    def add_edge(self, node: 'GraphNode', value: float):
        self.edges.append((node, value))
        node.edges.append((self, value))
    def get_edges(self): return self.edges

class Graph:
    def __init__(self, labels: list[str], edges: list[Tuple[str, str, float]]) -> None:
        self.verticies = {} # type: dict[str, GraphNode]
        for v in labels:
            self.verticies[v] = GraphNode(v)
        for edge in edges:
            if edge[0] not in labels:
                raise ReferenceError(f"Could not find node '{edge[0]}' in vertices")
            if edge[1] not in labels:
                raise ReferenceError(f"Could not find node '{edge[1]}' in vertices")
            self.verticies[edge[0]].add_edge(self.verticies[edge[1]], edge[2])
    def get_node(self, label: str): return self.verticies[label]



STRAIGHTLINE_DISTANCE_TO_BUCHAREST = {
    "Arad": 366,
    "Bucharest": 0,
    "Craiova": 160,
    "Drobeta": 242,
    "Eforie": 161,
    "Fagaras": 176,
    "Giurgiu": 77,
    "Hirsova": 151,
    "Iasi": 226,
    "Lugoj": 244,
    "Mehadia": 241,
    "Neamt": 234,
    "Oradea": 380,
    "Pitesti": 100,
    "Rimnicu Vilcea": 193,
    "Sibiu": 253,
    "Timisoara": 329,
    "Urziceni": 80,
    "Vaslui": 199,
    "Zerind": 374
}

romania = Graph([
    "Arad", "Bucharest", "Craiova", "Drobeta",
    "Eforie", "Fagaras", "Giurgiu", "Hirsova",
    "Iasi", "Lugoj", "Mehadia", "Neamt",
    "Oradea", "Pitesti", "Rimnicu Vilcea", "Sibiu",
    "Timisoara", "Urziceni", "Vaslui", "Zerind"
], [
    ("Arad", "Zerind", 75),
    ("Arad", "Timisoara", 118),
    ("Arad", "Sibiu", 140),
    ("Oradea", "Zerind", 71),
    ("Oradea", "Sibiu", 151),
    ("Sibiu", "Fagaras", 99),
    ("Lugoj", "Timisoara", 111),
    ("Lugoj", "Mehadia", 70),
    ("Drobeta", "Mehadia", 75),
    ("Drobeta", "Craiova", 120),
    ("Pitesti", "Craiova", 138),
    ("Rimnicu Vilcea", "Sibiu", 80),
    ("Rimnicu Vilcea", "Craiova", 146),
    ("Rimnicu Vilcea", "Pitesti", 97),
    ("Bucharest", "Pitesti", 101),
    ("Bucharest", "Fagaras", 211),
    ("Bucharest", "Giurgiu", 90),
    ("Bucharest", "Urziceni", 85),
    ("Hirsova", "Urziceni", 98),
    ("Hirsova", "Eforie", 86),
    ("Vaslui", "Urziceni", 142),
    ("Vaslui", "Iasi", 92),
    ("Neamt", "Iasi", 87)
])





class SearchQueue(ABC):
    def __init__(self) -> None:
        self.items = [] # type: list[Tuple[GraphNode, list[GraphNode]]]

    def is_empty(self) -> bool:
        return len(self.items) == 0

    @abstractmethod
    def insert(self, candidate: Tuple[GraphNode, list[GraphNode]], cost: float): pass
    @abstractmethod
    def remove(self) -> Tuple[GraphNode, list[GraphNode]]: pass

    def expand(self, node: GraphNode, path: list[GraphNode]):
        for adj_node, adj_cost in node.get_edges():
            self.insert((adj_node, [ *path, adj_node ]), adj_cost)



class DepthFirstQueue(SearchQueue):
    def insert(self, candidate: Tuple[GraphNode, list[GraphNode]], _cost):
        self.items.insert(0, candidate)
    def remove(self) -> GraphNode:
        return self.items.pop(0)

class BreadthFirstQueue(SearchQueue):
    def insert(self, candidate: Tuple[GraphNode, list[GraphNode]], _cost):
        self.items.append(candidate)
    def remove(self) -> GraphNode:
        return self.items.pop(0)



def generic_tree_search(start_node: GraphNode, queue: SearchQueue, goal_fn: Callable[[GraphNode], bool]) -> list[GraphNode]:
    """Given a start node, a goal function, and an opinionated SearchQueue,
    returns the list/path of GraphNode to get to the goal state.

    Args:
        start_node: GraphNode to start at.
        queue: SearchQueue implementing the desired search algorithm logic.
        goal_fn: A function the return true if the given GraphNode is the goal state, and false otherwise.

    Returns:
        list[GraphNode]: Path from start_node to the goal state, or None if unachievable.
    """
    seen = set() # type: set[GraphNode]
    queue.insert((start_node, [ start_node ]), 0)
    while not queue.is_empty():
        print(list(map(lambda c: c[0].label, queue.items)))
        next, next_path = queue.remove()
        if next in seen: continue
        seen.add(next)

        if goal_fn(next): return next_path
        queue.expand(next, next_path)
    return None


print("Depth-First (Queue):")
path = generic_tree_search(romania.get_node("Arad"), DepthFirstQueue(), lambda goal: goal.label == "Bucharest")
path_names = list(map(lambda node: node.label, path))
print("Depth-First (Solution):")
print(path_names)
print("")

print("Breadth-First (Queue):")
path = generic_tree_search(romania.get_node("Arad"), BreadthFirstQueue(), lambda goal: goal.label == "Bucharest")
path_names = list(map(lambda node: node.label, path))
print("Breadth-First (Solution):")
print(path_names)
