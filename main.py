import copy 
import heapq

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
    def __init__(self, id: int, start: int, end: int, weight: int, selected: list):
        Node.count += 1
        self.id = id
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
        heapq.heappush(self.heap, (-node.weight, node.id, node))
    
    def pop(self):
        if self.heap:
            _,_, node = heapq.heappop(self.heap)
            return node 
        return None
    
    def empty(self):
        return not self.heap

class SchedulingSolver:
    """
    Given n tasks with start time, end time and a weight associated with each,
    we want to return the tasks that are chosen such that the weight is 
    maximized
    """
    def __init__(self, startTime: list, endTime: list, weight: list, order=1):
        """        
        Args:
            startTime (List[int]): List of start times for all jobs
            endTime (List[int]): List of end times for all jobs
            weight (List[int]): List of weight for all jobs to maximize 
        """
        self.n = len(startTime)
        self.startTime = startTime
        self.endTime = endTime
        self.weight = weight
        self.initialize_jobs(order)
    
    def initialize_jobs(self, order):
        """
        Initialize set of jobs by particular order
        
        Args:
            order (int): 
            * 1 if order in ascending start time 
            * 2 if order in ascending end time
            * 3 if order in ascending profit 
        """
        tasks = []
        
        # Create a range of tasks
        for i in range(self.n):
            t = Task(i, 
                     start=self.startTime[i],
                     end=self.endTime[i],
                     weight=self.weight[i])
            tasks.append(t)
        
        match (order):
            case 1:
                self.jobs = sorted(tasks, key=lambda x: x.start)
            case 2:
                self.jobs = sorted(tasks, key=lambda x: x.end)
            case 3:
                self.jobs = sorted(tasks, key=lambda x: x.weight)
        
    
    def find_next_available(self, jobs: list, i: int):
        """
        Find the nearest job that does not conflict with the ith one

        Args:
            jobs: List of jobs in order of ascending start time
            i: Index of current job to search for the next available on 

        Returns: 
            int: Index of next available job. -1 if none is found
        """
        for j in range(i+1, self.n):
            # If the start time of jth job is after the end time of the ith job
            if (jobs[j].start >= jobs[i].end):
                return j
        return -1
    
    def dp_reconstruct_solution(self, jobs, memo):
        """
        Reconstruct the solution from the memoization table
        
        Args:
            jobs: List[Task] 
            memo: List[int]
        
        Returns: 
            List[int]
        """
        solution = []
        
        for i in range(self.n):
            if (i == self.n - 1):
                solution.append(i)
            else:
                if (memo[i] == memo[i+1] + jobs[i].weight):
                    solution.append(i)
                    i = self.find_next_available(jobs, i)
        
        return solution
                

    def dp(self):
        """
        Implementation of dynamic programming to return the optimal 
        solution and optimal value

        First, we want to sort the jobs by start time

        Next, iterate from the right to left (meaning from the job that ends the latest).
        In each iteration, keep track of the best profit obtained at the 
        ith job. The best profit is computed by taking the maximum of 2 possibilities:

        1. Not taking the ith job: the profit is just the profit at the (i+1)th job. 

        2. Taking the ith job: the profit is the sum of the job's value and the best profit 
        at the next job that does not conflict with the ith one. If there are no such jobs, 
        then profit will just be the ith job's value. 
        
        Time complexity: O(n^2)

        Returns:
            Tuple[int, List[int]]
        """
        for j in self.jobs:
            print(j)
            
        # Initialize memoization array
        memo = [0] * self.n
        # The maximum profit at the last job is just the last job's value
        memo[self.n-1] = self.jobs[self.n-1].weight
        
        for i in range(self.n-2, -1, -1):
            next_job_id = self.find_next_available(self.jobs, i)
            best_value = max(memo[i+1], # not take the job
                             self.jobs[i].weight + # take the job
                             (0 if next_job_id == -1 else memo[next_job_id])) # and add the best profit at the job right after
            # Memoize it
            memo[i] = best_value
        
        return (memo[0], self.dp_reconstruct_solution(self.jobs, memo))
    
    def branch_and_bound(self):
        """
        Implementation of branch and bound to return the optimal 
        solution and optimal value

        Returns:
            Tuple[int, List[int]]
        """
        # Initialize a tree
        tree = DecisionTree()
        
        root = Node(-1, 0, 0, 0, [])
        
        tree.push(root)
        
        max_profit = 0
        solution = []
        
        while not tree.empty(): 
            # Current cumulative set of jobs 
            span = tree.pop()
            
            # print("Current span: " + span.count)
            
            for job in self.jobs:
                i = job.id
                # Make sure not to re-select jobs that have been in the schedule
                if i != span.id and i not in span.selected:
                    # If this job does not conflict
                    if (job.start >= span.end):
                        if (span.weight + job.weight > max_profit):
                            solution = copy.deepcopy(span.selected + [i])
                            
                        max_profit = max(max_profit, span.weight + job.weight)
                        
                        child = Node(i,
                                     min(job.start, span.start), 
                                     max(job.end, span.end),
                                     span.weight + job.weight,
                                     span.selected + [i])
                        
                        tree.push(child)

        return (max_profit, solution)
        

if __name__ == "__main__":
    startTimes = [1,2,3,4,6]
    endTimes = [3,5,10,6,9]
    profit = [20,20,100,70,60]

    solver = SchedulingSolver(startTimes, endTimes, profit)

    print(solver.branch_and_bound())
