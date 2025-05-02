import heapq

class Node: 
    """
    Represents a node/"span" in the "task" tree. Each node has the 
    following properties:
    
    * `start`: start time (integer)
    * `end`: end time (int)
    * `weight`: weight (int)
    * `selected`: list of selected jobs 
    """
    count = 0
    def __init__(self, start: int, end: int, weight: int, selected: list):
        Node.count += 1
        self.start = start 
        self.end = end 
        self.weight = weight
        self.selected = selected[:]

class DecisionTree:
    """
    Represents a max heap
    """
    def __init__(self):
        self.heap = []
    
    def push(self, node: Node):
        heapq.heappush(self.heap, (-node.weight, node.count, node))
    
    def pop(self):
        if self.heap:
            _,_, node = heapq.heappop(self.heap)
            return node 
        return None
    
    def empty(self):
        return not self.heap