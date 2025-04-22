# Scheduling Task using Applications of Integer Programming

MATH-339: Optimization (Spring 2025)

## Problem

Given a set of $n$ tasks with the following features:

\begin{enumerate}
    \item Start time $s_i$: $s_i \in \Z, 1 \leq s_i \leq 24$
    \item End time $e_i$: $e_i \in \Z, 1 \leq s_i < e_i \leq 24$
    \item Profit $p_i$: $p_i \in \Z, 0 \leq p_i$
    \item Happiness level $h_i$: $h_i \in \Z, 1 \leq h_i \leq 10$
\end{enumerate}

We want to compare 2 algorithms that will choose a subset of non-overlapping tasks that obtain the maximum profit:

* Dynamic programming
* Brute-force branch-and-bound


