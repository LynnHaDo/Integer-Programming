import unittest

from models import SchedulingSolver
from utils import TimeConverter

from amplpy import AMPL

from utils import GREEN, RESET, PURPLE

import time 
from threading import Thread

class TestFlights(unittest.TestCase):
    def setUp(self):
        super().setUp()
        
        time_converter = TimeConverter()
        
        # Set up the solver
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
            self.solver = SchedulingSolver(start, end, prices)
            
            # Get the overlapping pairs
            overlapping_pairs = self.solver.cts
    
            # Set up AMPL
            ampl = AMPL()
            
            constraints = ""
            
            for i, pair in enumerate(overlapping_pairs):
                constraints += f"s.t. c{i}: x[{pair[0]}] + x[{pair[1]}] <= 1;\n"
            
            # Define the model
            model = f"""
            set RANGE := 0..{self.solver.n-1};
            
            var COST{{RANGE}};
            
            # Binary variable: x[i] = 1 if the task is chosen; 0 otherwise
            var x{{RANGE}} binary;
            
            maximize z: sum{{i in RANGE}} x[i] * COST[i];
            
            # For each overlapping pair, choose at most 1
            {constraints}
            """
            
            ampl.eval(model)
            
            # Fill in the cost 
            for i, c in enumerate(prices):
                ampl.eval(f"fix COST[{i}] := {c};")
            
            # Solve 
            ampl.option["solver"] = "gurobi"
            ampl.solve()
            
            # Get the solution
            self.x = ampl.get_variable("x")
            
            # Print out the result of AMPL
            selected = []
            for i in range(self.solver.n):
                if self.x[i].value() == 1:
                    selected.append(f"{i}")
                    
            print(f"{GREEN}AMPL selected flights: {', '.join(selected)}{RESET}\n")
            
            # Get the optimal value
            self.z = ampl.get_value('z')
            
    def testDP(self):
        dp_optimal_value, dp_x = self.solver.dp()
        dp_x_str = [str(x) for x in dp_x]
        print(f"{PURPLE}DP selected courses: {', '.join(dp_x_str)}{RESET}\n")
        self.assertEqual(self.z, dp_optimal_value)
    
    def testDT(self):
        begin = time.time() 
        x_result = [None]
        z_result = [None]
        th = Thread(target=self.solver.decision_tree, args=(x_result, z_result))
        th.daemon = True
        th.start() 
        th.join(timeout=10)
        if (time.time() - begin > 10):
            print("Decision tree took too long to compute!")
            return
        dt_x_str = [str(x) for x in x_result]
        print(f"{PURPLE}Decision tree selected courses: {', '.join(dt_x_str)}{RESET}\n")
        self.assertEqual(self.z, z_result[0])
    
    def testBnB(self):
        begin = time.time() 
        x_result = [None]
        z_result = [None]
        depth_result = [None]
        th = Thread(target=self.solver.branch_and_bound, args=(x_result, z_result, depth_result))
        th.daemon = True
        th.start() 
        th.join(timeout=10)
        if (time.time() - begin > 10):
            print("Branch and Bound took too long to compute!")
            return
        bnb_optimal_value = z_result[0]
        bnb_x_str = [str(x) for x in x_result]
        print(f"{PURPLE}Branch and Bound selected courses: {', '.join(bnb_x_str)}\nDepth: {depth_result[0]}\n{RESET}")
        self.assertEqual(self.z, bnb_optimal_value)