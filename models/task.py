class Task:
    """
    Represents a task
    """
    def __init__(self, id, start: int, end: int, weight: int):
        self.id = id
        self.start = start 
        self.end = end 
        self.weight = weight
    
    def __str__(self):
        return f"Task {self.id}, start at: {self.start}, end at: {self.end}, with weight: {self.weight}"