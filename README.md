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

Let $O$ be the set of $(i,j)$ where task $i$ and $j$ overlap. 

* Then there are $|O|$ overlapping constraints, meaning $|O|$ decision variables $c_{ij}$ in the dual. 
* Regarding the $x_i \leq 1$ constraints in the primal LP, we would want $n$ extra decision variables $s_1, ..., s_n$ for these constraints.

Since the primal constraints are "$\leq$", each of the dual variables $c_{ij}$ and $s_i$ must be nonnegative. 

$$\begin{align*}
    &\min &\sum_{ij \in O} c_{ij} + \sum_{i=1}^{n} s_i \\
    &\text{such that } &\quad \sum_{j \in \{j: ij \in O\}}c_{ij} + s_i \ge p_i&\quad \text{for } i = 1, 2, ..., n \\ 
    & & 0 \leq s_i &\quad \text{for } i = 1, 2, ..., n \\
    & & 0 \leq c_{ij} &\quad \text{for all } ij \in O
\end{align*}$$

We tested the the primal LP against the dual using AMPL (in `tests/primal_dual.py`), and obtained the same results on the timetable data set. 

```{r}
testCompareDualvsPrimal (tests.primal_dual.TestDualPrimal) ... Gurobi 12.0.1: optimal solution; objective 40.4
9 simplex iterations
AMPL Primal LP solution: 0.5, 0.5, 0.5, 1.0, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 1.0, 0.5, 0.5, 1.0, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5
>       Optimal value: 40.40000000000001
Gurobi 12.0.1: optimal solution; objective 40.4
32 simplex iterations
AMPL Dual LP solution:
>       c = {'c_0_18': 2.45, 'c_0_24': 1.85, 'c_1_13': 2.15, 'c_1_21': 1.65, 'c_2_8': 1.75, 'c_2_25': 1.75, 'c_4_16': 1.1, 'c_4_19': 1.2, 'c_5_11': 0.0, 'c_5_14': 0.3499999999999999, 'c_5_17': 0.0, 'c_5_20': 1.95, 'c_6_9': 0.65, 'c_6_22': 0.7000000000000001, 'c_7_10': 0.65, 'c_7_23': 0.7000000000000001, 'c_8_25': 1.75, 'c_9_22': 0.9999999999999999, 'c_10_23': 0.9999999999999999, 'c_11_14': 2.850000000000001, 'c_11_17': 1.55, 'c_13_21': 1.55, 'c_14_17': 0.2999999999999998, 'c_16_19': 0.75, 'c_17_20': 0.0, 'c_18_24': 1.15}
>       s = 0.0, 0.0, 0.0, 3.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.1, 0.0, 0.0, 3.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
>       Optimal value: 40.4
ok
```

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