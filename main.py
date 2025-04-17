class SchedulingSolver:
    """
    Given n tasks with start time, end time and a weight associated with each,
    we want to return the tasks that are chosen such that the weight is 
    maximized
    """
    def __init__(self, startTime, endTime, weight):
        """
        :type startTime: List[int]
        :type endTime: List[int]
        :type profit: List[int]
        """
        self.startTime = startTime
        self.endTime = endTime
        self.weight = weight

    def dp(self):
        return []
    
    def branch_and_bound(self):
        return []

if __name__ == "__main__":
    startTimes = [1, 2, 3, 3]
    endTimes = [3, 4, 5, 6]
    profit = [50, 10, 40, 70]

    solver = SchedulingSolver(startTimes, endTimes, profit)

    print(solver.dp())
