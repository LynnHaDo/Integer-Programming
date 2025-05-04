import copy 
import time
import scipy
import numpy as np
import math
from . import DecisionTree, Node, Task

from utils import RED, RESET
from threading import Thread

class SchedulingSolver:
    """
    Given n tasks with start time, end time and a weight associated with each,
    we want to return the tasks that are chosen such that the weight is 
    maximized
    """
    def __init__(self, startTime: list, endTime: list, weight: list):
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
        # Initialize jobs for DP and Decision tree
        self.initialize_jobs()
        # Initialize matrices/vectors/bounds for Branch and Bound
        self.initialize_matrices()
        self.set_optimal_bound()
    
    # SET-UP        =================================================== 
    
    def initialize_jobs(self):
        """
        Initialize set of jobs by ascending start time 
        """
        tasks = []
        
        # Create a range of tasks
        for i in range(self.n):
            t = Task(i, 
                     start=self.startTime[i],
                     end=self.endTime[i],
                     weight=self.weight[i])
            tasks.append(t)
        
        self.jobs = sorted(tasks, key=lambda x: x.start)
    
    def initialize_matrices(self):
        """
        Initialize c, A, b, lb, ub to the following optimization problem:
        
        ```
        min c^Tx
        s.t. 
            Ax <= b 
            lb <= x <= ub
        ```
        """
        # Cost vector
        self.c = np.array(self.weight)
        
        # Constraint
        self.cts = self.overlapping_pairs()
        self.A = self.compute_matrix_A(self.cts)
        self.b = np.ones(len(self.cts))
        
        # Lower bound for each decision var 
        self.lb = np.zeros(self.n)
        # Upper bound for each decision var 
        self.ub = np.ones(self.n)
    
    def set_optimal_bound(self, x=None, z=-math.inf, depth=0):
        """
        Set the optimal bound found so far
        """
        self.x_optimal = x
        self.z_optimal = z
        self.depth = depth
        
    
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
            jobs: List of jobs in order of ascending start time
            memo: memoization table
        
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
    
    def is_overlapping(self, s1, e1, s2, e2):
        """
        Check if 2 tasks (s1, e1) and (s2, e2) overlap.
        
        Args:
            s1: start time of job 1
            e1: end time of job 1
            s2: start time of job 2
            e2: end time of job 2
        
        Returns: 
            True if they overlap, False otherwise
        """
        if (e1 <= s2 or s1 >= e2):
            return False 
        return True

    def overlapping_pairs(self):
        """
        Get all overlapping pairs in the job list
        
        Returns: 
            List of all overlapping pairs in (id1, id2) format
        """    
        pairs = []
            
        for i in range(self.n):
            s1, e1 = self.startTime[i], self.endTime[i]
            for j in range(i+1, self.n):
                s2, e2 = self.startTime[j], self.endTime[j]
                if (self.is_overlapping(s1, e1, s2, e2)):
                    pairs.append([i, j])
        
        return pairs
    
    def compute_matrix_A(self, ov_pairs):
        """
        Set up matrix A in the optimization problem:
        
        ```
        min c^Tx
        s.t. 
            Ax <= b 
            lb <= x <= ub
        ```
        
        Here, the number of rows of A is the number of overlapping pairs (1
        constraint for each pair). 
        
        The number of columns of A is the number of decision variables (or 
        number of jobs). 
        
        Returns:
            Matrix A
        """
        # Number of columns is the number of variables
        cols = self.n
        # Number of rows is the number of all possible pair of the variables
        rows = len(ov_pairs)
        A = np.zeros((rows, cols))

        # Generate matrix A by letting coefficients of jobs contained in each 
        # overlapping pair equal to 1 
        for i in range(rows):
            A[i][ov_pairs[i][0]] = 1
            A[i][ov_pairs[i][1]] = 1
        return A
    
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
    
    def decision_tree(self, x_result = [None], z_result = [None]):
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
                        
        x_result[0] = solution
        z_result[0] = max_profit
        return (max_profit, solution)
    
    def branch_and_bound(self, x_result=[None], z_result=[None], depth_result=[None]):
        """
        Caller of recursive branch and bound 
        
        Args:
            x_result: list where the optimal solution will be stored
            z_result: list where the optimal value will be stored
            depth_result: list where the depth of the branch will be stored
        
        Returns:
            Tuple[int] | None
            * optimal value (-np.inf if infeasible/omitted) 
            * optimal solution ([] if infeasible/omitted) \n
            * depth: depth of the tree
        """
        res = self.recursive_branch_and_bound(self.lb, self.ub)
        if res is None:
            return None 
        x, z, depth = res
        x_result[0] = x 
        z_result[0] = z 
        depth_result[0] = depth
        res = []
        for i in range(self.n):
            if x[i] == 1:
                res.append(i)
        return z,res,depth
    
    def recursive_branch_and_bound(self, lb, ub, depth = 1):
        """
        Implementation of branch and bound method. 
        Using `scipy`'s `linprog` utility, we compute the optimal solution
        and check for non-integers. 
        
        If there are none, return the solution and update the bound. 
        
        If there exists non-integers, recursively branch on each non-integer 
        solution. 
        
        Args:
            lb: lower bound for each decision variable
            ub: upper bound for each decision variable
            depth: the depth of the tree
        
        Returns:
            Tuple[int] | None
            * optimal solution ([] if infeasible/omitted)
            * optimal value (-np.inf if infeasible/omitted) 
            * depth: depth of the tree
        """
        # Optimal solution for LP relaxation
        c = -self.c 
        res = scipy.optimize.linprog(c=c, 
                                     A_ub=self.A, 
                                     b_ub=self.b, 
                                     bounds = list(zip(lb, ub)))

        # Check if LP is feasible
        if not res.success:
            return None
        
        # Candidate for the optimal value and the objective value
        x_candidate, z_candidate = res.x, res.fun
        # Correct sign for maximization
        z_candidate = -z_candidate 
        
        # If the value is less than the current best solution,
        # don't bother going further
        if (z_candidate < self.z_optimal):
            return None
        
        # Check the optimal solution to see if any is non-integer
        is_int = True 
        for i in range(self.n):
            # If x_i is not integer
            if not x_candidate[i] % 1 == 0:
                is_int = False
                break
        
        # Found integer solution 
        if is_int:
            if z_candidate > self.z_optimal:
                self.set_optimal_bound(x_candidate, z_candidate, depth)
            return x_candidate, z_candidate, depth
        
        # Branch on the first non-integer variable
        for i in range(self.n):
            if not x_candidate[i] % 1 == 0:
                # Left branch: x_i <= floor(x_i)
                left_lb = np.copy(lb)
                left_ub = np.copy(ub)
                left_ub[i] = np.floor(x_candidate[i])
                left_res = self.recursive_branch_and_bound(left_lb, left_ub, depth + 1)
                if left_res is not None:
                    x_left, z_left, depth_left = left_res

                # Right branch: x_i >= ceil(x_i)
                right_lb = np.copy(lb)     
                right_ub = np.copy(ub) 
                right_lb[i] = np.ceil(x_candidate[i])
                right_res = self.recursive_branch_and_bound(right_lb, right_ub, depth + 1)
                if right_res is not None:
                    x_right, z_right, depth_right = right_res

                # Return the best solution
                if left_res is None and right_res is not None:
                    return x_right, z_right, depth_right
                elif left_res is not None and right_res is None:
                    return x_left, z_left, depth_left
                elif left_res is not None and right_res is not None:
                    if(z_left > z_right):
                        return x_left, z_left, depth_left
                    else: 
                        return x_right, z_right, depth_right
                return None 