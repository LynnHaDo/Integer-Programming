# Scheduling Task using Applications of Integer Programming

MATH-339: Optimization (Spring 2025)

## Problem

Given a set of $n$ tasks with the following features:

* Start time $s_i$: $s_i \in \Z, 1 \leq s_i \leq 24$
* End time $e_i$: $e_i \in \Z, 1 \leq s_i < e_i \leq 24$
* Weight $w_i$: $w_i \in \Z, 0 \leq w_i$

We want to compare 2 algorithms that will choose a subset of non-overlapping tasks that obtain the maximum weight:

* Dynamic programming
* Brute-force branch-and-bound

## Applications in Real-world Data sets

* Flight scheduling that maximizes revenue


