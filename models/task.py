class Task:
    """
    Represents a task
    """
    def __init__(self, id, start: int, end: int, weight: int, group: int = 0):
        self.id = id
        self.start = start 
        self.end = end 
        self.weight = weight
        self.group = group
    
    def __str__(self):
        return f"[Group {self.group}] Task {self.id}, start at: {self.start}, end at: {self.end}, with weight: {self.weight}"