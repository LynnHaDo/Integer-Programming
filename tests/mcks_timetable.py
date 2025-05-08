import unittest

from models import SchedulingSolver
from utils import TimeConverter
import time

from amplpy import AMPL

from utils import GREEN, RESET, PURPLE

class TestTimetableMCKS(unittest.TestCase):
    def setUp(self):
        super().setUp()
        
        time_converter = TimeConverter()
        
        # Set up the solver
        with open("data/timetable.csv", "r") as f:
            start = []
            end = []
            ratings = []
            groups = {}
            
            # Get all lines in the file
            lines = f.readlines()
            
            # Remove the header
            lines.pop(0)
            
            for i, line in enumerate(lines):
                line_arr = line.split(",")
                group_id = line_arr[1]
                d,s,e,r = line_arr[3:7]
                
                s = time_converter.day_and_time_to_int(d,s)
                e = time_converter.day_and_time_to_int(d,e)
                r = float(r)
                
                start.append(s)
                end.append(e)
                ratings.append(r)
                groups[group_id] = [i] if group_id not in groups else groups[group_id] + [i]
            
            # Feed it to the solver
            self.solver = SchedulingSolver(start, end, ratings)
            
            # Get the overlapping pairs
            overlapping_pairs = self.solver.cts
    
            # Set up AMPL
            ampl = AMPL()
            
            # Overlapping constraint
            overlapping_constraints = ""
            
            for i, pair in enumerate(overlapping_pairs):
                overlapping_constraints += f"s.t. overlap_{i}: x[{pair[0]}] + x[{pair[1]}] <= 1;\n"
            
            # Group constraint
            group_constraints = ""
            
            for id in groups.keys():
                group_name = '_'.join(id.split(" "))
                group_constraints += f"s.t. group_{group_name}: "
                for i in groups[id]:
                    group_constraints += f"x[{i}] +"
                group_constraints = group_constraints[:-1]
                group_constraints += "<= 1;\n"
            
            # Define the model
            model = f"""
            set RANGE := 0..{self.solver.n-1};
            
            var COST{{RANGE}};
            
            # Binary variable: x[i] = 1 if the task is chosen; 0 otherwise
            var x{{RANGE}} binary;
            
            maximize z: sum{{i in RANGE}} x[i] * COST[i];
            
            # For each overlapping pair, choose at most 1
            {overlapping_constraints}
            
            # For each group, select at most 1
            {group_constraints}
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
            
    def testAMPL(self):
        pass