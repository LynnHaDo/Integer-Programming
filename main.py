import copy 
import heapq

class Node: 
    def __init__(self, id: int, start: int, end: int, weight: int, selected):
        self.id = id
        self.start = start 
        self.end = end 
        self.weight = weight
        self.selected = selected[:]

class DecisionTree:
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
    def __init__(self, startTime, endTime, weight):
        """
        :type startTime: List[int]
        :type endTime: List[int]
        :type weight: List[int]
        """
        self.n = len(startTime)
        self.startTime = startTime
        self.endTime = endTime
        self.weight = weight
    
    def find_next_available(self, jobs, i):
        """
        Find the nearest job that does not conflict with the ith one

        :type jobs: List[Tuple[int, int, int]]
        :type i: int

        :rtype: int
        """
        for j in range(i+1, self.n):
            # If the start time of jth job is after the end time of the ith job
            if (jobs[j][0] >= jobs[i][1]):
                return j
        return -1
    
    def dp_reconstruct_solution(self, jobs, memo):
        """
        Reconstruct the solution from the memoization table
        
        :type jobs: List[Tuple[int, int, int]]
        :type memo: List[int]
        
        :rtype: List[int]
        """
        solution = []
        
        for i in range(self.n):
            if (i == self.n - 1):
                solution.append(i)
            else:
                if (memo[i] == memo[i+1] + jobs[i][2]):
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

        :rtype: Tuple[int, List[int]]
        """
        # Sort jobs by start time
        jobs = sorted(zip(self.startTime, self.endTime, self.weight), key=lambda v: v[0])

        # Initialize memoization array
        memo = [0] * self.n
        # The maximum profit at the last job is just the last job's value
        memo[self.n-1] = jobs[self.n-1][2]
        
        for i in range(self.n-2, -1, -1):
            next_job_id = self.find_next_available(jobs, i)
            best_value = max(memo[i+1], # not take the job
                             jobs[i][2] + # take the job
                             (0 if next_job_id == -1 else memo[next_job_id])) # and add the best profit at the job right after
            # Memoize it
            memo[i] = best_value
        
        return (memo[0], self.dp_reconstruct_solution(jobs, memo))
    
    def branch_and_bound(self):
        """
        Implementation of branch and bound to return the optimal 
        solution and optimal value

        :rtype: Tuple[int, List[int]]
        """
        # Sort jobs by start time
        jobs = sorted(zip(self.startTime, self.endTime, self.weight), key=lambda v: v[0])
        print(jobs)
        tree = DecisionTree()
        
        root = Node(-1, 0, 0, 0, [])
        
        tree.push(root)
        
        max_profit = 0
        solution = []
        
        while not tree.empty(): 
            # Current cumulative set of jobs 
            span = tree.pop()
            
            for i, job in enumerate(jobs):
                # Make sure not to re-select jobs that have been in the schedule
                if i != span.id and i not in span.selected:
                    # If this job does not conflict
                    if (job[0] >= span.end):
                        if (span.weight + job[2] > max_profit):
                            solution = copy.deepcopy(span.selected + [i])
                            
                        max_profit = max(max_profit, span.weight + job[2])
                        
                        child = Node(i, 
                                     min(job[0], span.start), 
                                     max(job[1], span.end),
                                     span.weight + job[2],
                                     span.selected + [i])
                        
                        tree.push(child)

        return (max_profit, solution)
        

if __name__ == "__main__":
    startTimes = [1,1,1]
    endTimes = [2,3,4]
    profit = [5,6,4]

    solver = SchedulingSolver(startTimes, endTimes, profit)

    print(solver.branch_and_bound())
