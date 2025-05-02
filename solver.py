import copy 
import time
from models import DecisionTree, Node, Task

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
    
    # SET-UP        =================================================== 
    
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
    
    # HELPERS      =================================================== 
    
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
    
    def __str__(self):        
        begin = time.time()
        dp_res = self.dp()
        time.sleep(1)
        end = time.time()
        dp_dur = end - begin
            
        begin1 = time.time()
        dt_res = self.decision_tree()
        time.sleep(1)
        end1 = time.time()
        dt_dur = end1 - begin1
        
        return f"== Dynamic Programming (without constraint)\nResult: {dp_res}\nRun-time: {dp_dur}\n== Decision Tree (without constraint)\nResult: {dt_res}\nRun-time: {dt_dur}\n"
    
    # ALGORITHMS    ===================================================            

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
    
    def multiple_choice_dp(self, classes: list):
        pass
    
    def decision_tree(self):
        """
        Implementation of decision tree to return the optimal 
        solution and optimal value
        
        Decision tree is implemented as a max-heap where the 
        root is the set of jobs that yields the maximum cumulative
        weight. 
        
        Each time we pop the current most valuable span of jobs out and
        add another job to the span if it (1) is not already in the span,
        and (2) doesn't conflict with the end of the span. If the job is
        mergable, update the span with the added weight and job, then add
        it to the heap. 
        
        The process continues until the tree is emptied. 

        Returns:
            Tuple[int, List[int]]
        """
        # Initialize a tree
        tree = DecisionTree()
        
        root = Node(0, 0, 0, [])
        
        tree.push(root)
        
        max_profit = 0
        solution = []
        
        while not tree.empty(): 
            # Current cumulative set of jobs 
            span = tree.pop()
            
            for job in self.jobs:
                i = job.id
                # Make sure not to re-select jobs that have been in the schedule
                if i not in span.selected:
                    # If this job does not conflict
                    if (job.start >= span.end):
                        if (span.weight + job.weight > max_profit):
                            solution = copy.deepcopy(span.selected + [i])
                            
                        max_profit = max(max_profit, span.weight + job.weight)
                        
                        child = Node(min(job.start, span.start), 
                                     max(job.end, span.end),
                                     span.weight + job.weight,
                                     span.selected + [i])
                        
                        tree.push(child)

        return (max_profit, solution)