import unittest

from models import SchedulingSolver
from utils import TimeConverter
import time

from amplpy import AMPL

from utils import GREEN, RESET, PURPLE

class TestTimetable(unittest.TestCase):
    def setUp(self):
        super().setUp()
        
        time_converter = TimeConverter()
        
        # Set up the solver
        with open("data/timetable.csv", "r") as f:
            start = []
            end = []
            ratings = []
            
            # Get all lines in the file
            lines = f.readlines()
            
            # Remove the header
            lines.pop(0)
            
            for line in lines:
                line_arr = line.split(",")
                d,s,e,r = line_arr[3:7]
                
                s = time_converter.day_and_time_to_int(d,s)
                e = time_converter.day_and_time_to_int(d,e)
                r = float(r)
                
                start.append(s)
                end.append(e)
                ratings.append(r)
            
            # Feed it to the solver
            self.solver = SchedulingSolver(start, end, ratings)
            
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
            for i, c in enumerate(ratings):
                ampl.eval(f"fix COST[{i}] := {c};")
            
            # Solve 
            ampl.option["solver"] = "gurobi"
            solver_begin = time.time()
            ampl.solve()
            solver_end = time.time()
            
            # Get the solution
            self.x = ampl.get_variable("x")
            
            # Print out the result of AMPL
            selected = []
            for i in range(self.solver.n):
                if self.x[i].value() == 1:
                    selected.append(f"{i}")
                    
            print(f"{GREEN}AMPL selected courses: {', '.join(selected)}\n>\tRun-time: {solver_end - solver_begin}{RESET}")
            
            # Get the optimal value
            self.z = ampl.get_value('z')
            
    def testDP(self):
        # Start the timer
        begin = time.time()
        dp_optimal_value, dp_x = self.solver.dp()
        end = time.time()
        dp_x_str = [str(x) for x in dp_x]
        print(f"{PURPLE}DP selected courses: {', '.join(dp_x_str)}\n>\tRun-time: {end - begin}{RESET}")
        self.assertEqual(self.z, dp_optimal_value)
    
    def testDT(self):
        # Start the timer
        begin = time.time()
        dt_optimal_value, dt_x = self.solver.decision_tree()
        end = time.time()
        dt_x_str = [str(x) for x in dt_x]
        print(f"{PURPLE}Decision tree selected courses: {', '.join(dt_x_str)}\n>\tRun-time: {end - begin}{RESET}")
        self.assertEqual(self.z, dt_optimal_value)
    
    def testBnB(self):
        # Start the timer
        begin = time.time()
        bnb_optimal_value, bnb_x, depth = self.solver.branch_and_bound()
        end = time.time()
        bnb_x_str = [str(x) for x in bnb_x]
        print(f"{PURPLE}Branch and Bound selected courses: {', '.join(bnb_x_str)}\n>\tRun-time: {end-begin}\n>\tDepth: {depth}{RESET}")
        self.assertEqual(self.z, bnb_optimal_value)