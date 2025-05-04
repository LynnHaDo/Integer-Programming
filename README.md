# Scheduling Task using Applications of Integer Programming

MATH-339: Optimization (Spring 2025)

## Problem

Given a set of $n$ tasks with the following features:

* Start time $s_i$: $s_i \in \mathbb{Z}, 1 \leq s_i \leq 24$
* End time $e_i$: $e_i \in \mathbb{Z}, 1 \leq s_i < e_i \leq 24$
* Weight $w_i$: $w_i \in \mathbb{Z}, 0 \leq w_i$

We want to compare 3 algorithms that will choose a subset of non-overlapping tasks that obtain the maximum weight:

* Dynamic programming
* Brute-force branch-and-bound
* Decision tree

## Applications in Real-world Data sets

* Flight scheduling that maximizes revenue
* Timetable scheduling optimization to maximize rating 

## Installation

1. Clone the repo

```
https://github.com/LynnHaDo/Integer-Programming.git
```

2. Install `scipy` and `numpy`

```
pip install -r requirements.txt
```

3. Run `main.py` to see test results

```
python3 main.py
```

* For each algorithm, the optimal solution and value will be printed out in the following format:
    * Dynamic programming: (`optimal_value`, `optimal solution`) where `optimal solution` is an array containing job IDs selected in the optimal schedule. 
    * Decision tree: similar to Dynamic programming
    * Branch and bound: (`optimal_value`, `optimal solution`, `tree_depth`) where `optimal solution` is a np-array where 1 means the job i is selected in the optimal schedule, 0 otherwise; `tree_depth` is the depth of the tree
* We also calculated the running time of each algorithm to see which one is most time-efficient in each test case. If the algorithm took too long to run, no result will be printed out. 


