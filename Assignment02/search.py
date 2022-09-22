# CS6033 - Artificial Intelligence
# Fall 2022
# Assignment 02

# Homework Group 14
#  - Adonia Jebessa
#  - Mohammad Yahiya Khan
#  - Scott Fasone



from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from queue import PriorityQueue
from typing import Callable, Tuple



# Our graph Implementation, which is similar to adjacency lists,
# but the vertices own their adjacent nodes instead of the graph itself.
class GraphNode:
    def __init__(self, label: str) -> None:
        self.label = label
        self.edges = [] # type: list[Tuple[GraphNode, float]]
    def add_edge(self, node: 'GraphNode', value: float):
        self.edges.append((node, value))
        node.edges.append((self, value))
    def get_edges(self): return self.edges
    
    def get_edge_value(self, node: 'GraphNode'):
        edge_values = [ e[1] for e in self.edges if e[0].label == node.label ]
        if len(edge_values) == 0:
            return 0
        else:
            return edge_values[0]

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



# Givin straightline distances from the given city to Bucharest.
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
    "Zerind": 374,
}
# Function used as the heuristic for Best-First Search, and part of the heuristic for A*.
def get_straightline_distance_to_bucharest(node: GraphNode):
    return STRAIGHTLINE_DISTANCE_TO_BUCHAREST[node.label]

# The given graph of Romania, using our graph implementation.
romania = Graph([
    "Arad", "Bucharest", "Craiova", "Drobeta",
    "Eforie", "Fagaras", "Giurgiu", "Hirsova",
    "Iasi", "Lugoj", "Mehadia", "Neamt",
    "Oradea", "Pitesti", "Rimnicu Vilcea", "Sibiu",
    "Timisoara", "Urziceni", "Vaslui", "Zerind",
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
    ("Neamt", "Iasi", 87),
])





# The search algorithm is implemented via the following queues.
# The generic search algorithm given is used, but passed one of the following classes
# which will define in which order nodes are visited.

# First are a few abstract classes that setup some common functionality.

@dataclass(order=True)
class GraphSearchItem:
    """A node candidate with its associated priority for use in a priority queue"""
    priority: float
    item: Tuple[GraphNode, list[GraphNode]]=field(compare=False)
class AbstractSearchQueue(ABC):
    """Lays out the common functionality used by all search algorithm queues."""
    @abstractmethod
    def get_items(self) -> list[GraphNode]: pass
    @abstractmethod
    def is_empty(self) -> bool: pass
    @abstractmethod
    def insert(self, candidate: Tuple[GraphNode, list[GraphNode]], cost: float): pass
    @abstractmethod
    def remove(self) -> Tuple[GraphNode, list[GraphNode]]: pass

    def expand(self, node: GraphNode, path: list[GraphNode]):
        """Given a node and the path taken to that node, adds the adjacent nodes to this queue
        (with their corresponding paths)"""
        for adj_node, adj_cost in node.get_edges():
            self.insert((adj_node, [ *path, adj_node ]), adj_cost)

class SearchList(AbstractSearchQueue):
    """Abstract class for search queues that using a backing list"""
    def __init__(self) -> None:
        self.items = [] # type: list[Tuple[GraphNode, list[GraphNode]]]
    def get_items(self) -> list[GraphNode]:
        return list(map(lambda c: c[0], self.items))
    def is_empty(self) -> bool:
        return len(self.items) == 0
class SearchQueue(AbstractSearchQueue):
    """Abstract class for search queues that using a backing priority queue (using GraphSearchItem)"""
    def __init__(self) -> None:
        self.queue = PriorityQueue(128)
    def get_items(self) -> list[GraphNode]:
        return list(map(lambda c: c.item[0], self.queue.queue))
    def is_empty(self) -> bool:
        return self.queue.empty()




class DepthFirstQueue(SearchList):
    """Depth-First Search Queue, implemented as LIFO on a list"""
    def insert(self, candidate: Tuple[GraphNode, list[GraphNode]], _cost):
        self.items.insert(0, candidate)
    def remove(self) -> GraphNode:
        return self.items.pop(0)

class BreadthFirstQueue(SearchList):
    """Breadth-First Search Queue, implemented as FIFO on a list"""
    def insert(self, candidate: Tuple[GraphNode, list[GraphNode]], _cost):
        self.items.append(candidate)
    def remove(self) -> GraphNode:
        return self.items.pop(0)

class BestFirstQueue(SearchQueue):
    """Best-First Search Queue, implemented as a min-priority queue
    using the straightline distance heuristic as its priority"""
    def __init__(self, heuristic: Callable[[GraphNode], float]) -> None:
        super().__init__()
        self.heuristic = heuristic

    def insert(self, candidate: Tuple[GraphNode, list[GraphNode]], _cost):
        item = GraphSearchItem(self.heuristic(candidate[0]), candidate)
        self.queue.put(item)
    def remove(self) -> GraphNode:
        return self.queue.get().item

class AStarQueue(SearchQueue):
    """A* Search Queue, implemented as a min-priority queue
    using the straightline distance + current path cost heuristic as its priority"""
    def __init__(self, heuristic: Callable[[GraphNode], float]) -> None:
        super().__init__()
        self.heuristic = heuristic

    def insert(self, candidate: Tuple[GraphNode, list[GraphNode]], cost):
        item = GraphSearchItem(self.heuristic(candidate[0]) + cost, candidate)
        self.queue.put(item)
    def remove(self) -> GraphNode:
        return self.queue.get().item



_cities_visited = 0
def generic_tree_search(start_node: GraphNode, queue: SearchQueue, goal_fn: Callable[[GraphNode], bool]) -> list[GraphNode]:
    """Given a start node, a goal function, and an opinionated SearchQueue,
    returns the list/path of GraphNode to get to the goal state.

    Args:
        start_node: GraphNode to start at.
        queue: SearchQueue implementing the desired search algorithm logic.
        goal_fn: A function the return true if the given GraphNode is the goal state, and false otherwise.

    Returns:
        list[GraphNode]: Path from start_node to the goal state, or the empty path if unachievable.
    """
    seen = set() # type: set[GraphNode]
    global _cities_visited
    _cities_visited = 0
    queue.insert((start_node, [ start_node ]), 0)
    while not queue.is_empty():
        # print(list(map(lambda node: node.label, queue.get_items())))
        next, next_path = queue.remove()
        if next in seen: continue
        _cities_visited += 1
        seen.add(next)

        if goal_fn(next): return next_path
        queue.expand(next, next_path)
    return []



def get_path_length(path: list[GraphNode]):
    total = 0
    for i in range(1, len(path)):
        total += path[i - 1].get_edge_value(path[i])
    return total

def goal_fn(node: GraphNode):
    return node.label == "Bucharest"

start_node = romania.get_node("Lugoj")



print()
# print("Depth-First (Queue):")
path = generic_tree_search(start_node, DepthFirstQueue(), goal_fn)
path_names = list(map(lambda node: node.label, path))
print("Depth-First (Solution):")
print(path_names)
print(f"Cities Checked: {_cities_visited}\nPath Length: {get_path_length(path)}")

print()
# print("Breadth-First (Queue):")
path = generic_tree_search(start_node, BreadthFirstQueue(), goal_fn)
path_names = list(map(lambda node: node.label, path))
print("Breadth-First (Solution):")
print(path_names)
print(f"Cities Checked: {_cities_visited}\nPath Length: {get_path_length(path)}")

print()
# print("Best-First (Queue):")
best_queue = BestFirstQueue(get_straightline_distance_to_bucharest)
path = generic_tree_search(start_node, best_queue, goal_fn)
path_names = list(map(lambda node: node.label, path))
print("Best-First (Solution):")
print(path_names)
print(f"Cities Checked: {_cities_visited}\nPath Length: {get_path_length(path)}")

print()
# print("A* (Queue):")
astar_queue = AStarQueue(get_straightline_distance_to_bucharest)
path = generic_tree_search(start_node, astar_queue, goal_fn)
path_names = list(map(lambda node: node.label, path))
print("A* (Solution):")
print(path_names)
print(f"Cities Checked: {_cities_visited}\nPath Length: {get_path_length(path)}")


"""
Correctness
===========

All algorithms can find a path to any city from an existing city 
if the graph is connected and the goal city exists. Otherwise will output an empty path.
Depth-First and Breadth-First search will often result in more costly paths.
For example, starting from Lugoj and going to Bucharest results in a path length of 609 for DFS,
679 for BFS, and 504 for both A* and Best-first meaning they produced the shorter path for our use case.

Efficiency
==========
Uninformed:
DFS - If the algorithm happens to chose the correct path their is potential 
to have a pretty efficient solution and visit less cities however if it 
doesn't chose the correct path it can take a very circuitous path 
BFS - If there is a very high branching factor this algorithm can quickly 
become very inefficient and visit many nodes

Informed:
Instead of relying on luck or the graphs general properties they 
use some logic to traverse the graph 
Best-First - Since the algorithm is greedy it will not always 
find the optimal path because it will not take into account if the least 
costly node to travel to is actually a part of the optimal path
A* - This algorithm will verify more because it will account for the cost to get
to the current node
"""
