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
        
        return (memo[0], [])
    
    def branch_and_bound(self):
        """
        Implementation of branch and bound to return the optimal 
        solution and optimal value

        :rtype: Tuple[int, List[int]]
        """
        
        return (0, [])

if __name__ == "__main__":
    startTimes = [1, 2, 3, 3]
    endTimes = [3, 4, 5, 6]
    profit = [50, 10, 40, 70]

    solver = SchedulingSolver(startTimes, endTimes, profit)

    print(solver.dp())
