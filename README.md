# Scheduling Task using Applications of Integer Programming

MATH-339: Optimization (Spring 2025)

## Table of Content

* [Problem Formulation](#problem)
    * [IP](#ip)
    * [LP relaxation Problem vs. Dual](#duality-comparison-between-lp-relaxation-and-its-dual)
    * [Applications in Real-world Data sets](#applications-in-real-world-data-sets)
* [Libraries and Packages](#libraries-and-packages)
* [Installation](#installation)
    * [`SchedulingSolver` Guide](#schedulingsolver-guide)
    * [Run Tests](#run-unit-tests)


## Problem

### IP

Given a set of $n$ tasks with the following features:

* Start time $s_i$: $s_i \in \mathbb{Z}, 1 \leq s_i \leq 24$
* End time $e_i$: $e_i \in \mathbb{Z}, 1 \leq s_i < e_i \leq 24$
* Weight $w_i$: $0 \leq w_i$

Want to maximize: 

$\sum_{i=1}^{n}w_ix_i$

where $x_i$ is a binary variable representing the choice of task in the final subset. 

We want to compare 3 algorithms that will choose a subset of non-overlapping tasks that obtain the maximum weight:

* Dynamic programming
* Brute-force branch-and-bound
* Decision tree

### Duality: Comparison between LP relaxation and its Dual 

The LP relaxation of the IP problem is as follows:

$$\begin{align*}
    &\max &\sum_{i=1}^{n} x_ip_i \\
    &\text{such that } \quad &x_i + x_j \leq 1 &\quad \text{for all } i,j \text{ overlap} \\ 
    & & x_i \leq 1 &\quad \text{for } i = 1, 2, ..., n \\ 
    & & 0 \leq x_i &\quad \text{for } i = 1, 2, ..., n
\end{align*}$$


### Applications in Real-world Data sets

* Flight scheduling that maximizes revenue
* Timetable scheduling optimization to maximize rating 

## Libraries and Packages

* [scipy](https://docs.scipy.org/doc/scipy/reference/index.html): computes LP relaxation problem
* [numpy](https://numpy.org/install/): computes matrices to feed into `scipy`'s `linprog`
* [amplpy](https://amplpy.ampl.com/en/latest/getting-started.html#installation): runs IP for unit tests

## Installation

1. Clone the repo

```
https://github.com/LynnHaDo/Integer-Programming.git
```

2. Install `scipy` and `numpy`

```
pip install -r requirements.txt
```

### `SchedulingSolver` Guide 

The `SchedulingSolver` class takes in 3 arguments:

* `startTime` (List[int]): List of start times for all jobs
* `endTime` (List[int]): List of end times for all jobs
* `weight` (List[int]): List of weight for all jobs to maximize 

Example with `flights.txt` data set:

* Object initialization

```
from utils import TimeConverter

time_converter = TimeConverter()

with open("data/flights.txt", "r") as f:
    start = []
    end = []
    prices = []
            
    # Get all lines in the file
    lines = f.readlines()
            
    for line in lines:
        line_arr = line.split(",")
        s,e,p = line_arr[2:5]
                
        s = time_converter.time_to_minutes(s)
        e = time_converter.time_to_minutes(e)
        p = float(p)
                
        start.append(s)
        end.append(e)
        prices.append(p)
        
    # Feed it to the solver
    solver = SchedulingSolver(start, end, prices)
```

* Run each method: 

```
print(solver.dp()) # DP
print(solver.decision_tree()) # Decision tree
print(solver.branch_and_bound()) # Branch and Bound
```

### Run unit tests

Run `main.py` to see test results

```
python3 main.py
```

* For each algorithm, the optimal solution and value will be printed out in the following format:
    * Dynamic programming (DP): (`optimal_value`, `optimal solution`) where `optimal solution` is an array containing job IDs selected in the optimal schedule. 
    * Decision tree (DT): similar to Dynamic programming
    * Branch and bound: (`optimal_value`, `optimal solution`, `tree_depth`) where the first 2 are similar to DP and DT; `tree_depth` is the depth of the tree
* We also calculated the running time of each algorithm to see which one is most time-efficient in each test case. If the algorithm took too long to run, no result will be printed out. 