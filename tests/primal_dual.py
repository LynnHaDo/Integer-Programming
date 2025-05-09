import unittest

from models import SchedulingSolver
from utils import TimeConverter

from amplpy import AMPL

from utils import GREEN, RESET, PURPLE

class TestDualPrimal(unittest.TestCase):
    def initialize_data(self):
        time_converter = TimeConverter()
        
        # Set up the solver
        with open("data/timetable.csv", "r") as f:
            start = []
            end = []
            self.ratings = []
            
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
                self.ratings.append(r)
            
            # Feed it to the solver
            self.solver = SchedulingSolver(start, end, self.ratings)
            
            # Get the overlapping pairs
            self.overlapping_pairs = self.solver.cts
    
            # Set up AMPL
            self.ampl = AMPL()
        
    def setUp(self):
        super().setUp()
        
        self.initialize_data()
        
        ## PRIMAL       ====================================================
        constraints = ""
            
        for i, pair in enumerate(self.overlapping_pairs):
            constraints += f"s.t. c{i}: x[{pair[0]}] + x[{pair[1]}] <= 1;\n"
            
        # Define the model
        model = f"""
            set RANGE := 0..{self.solver.n-1};
            
            var COST{{RANGE}};
            
            # LP Relaxation constraint: 1 >= x_i >= 0
            var x{{RANGE}} >= 0, <= 1;
            
            maximize z: sum{{i in RANGE}} x[i] * COST[i];
            
            # For each overlapping pair, choose at most 1
            {constraints}
            """
            
        self.ampl.eval(model)
            
        # Fill in the cost 
        for i, c in enumerate(self.ratings):
            self.ampl.eval(f"fix COST[{i}] := {c};")
            
        # Solve 
        self.ampl.option["solver"] = "gurobi"
        self.ampl.solve()
            
        # Get the solution
        self.primal_x = self.ampl.get_variable("x")
            
        # Print out the result of AMPL
        self.primal_sol = []
        for i in range(self.solver.n):
            self.primal_sol.append(str(self.primal_x[i].value()))
                
        # Get the optimal value
        self.primal_val = self.ampl.get_value('z')
                    
        print(f"{GREEN}AMPL Primal LP solution: {', '.join(self.primal_sol)}\n>\tOptimal value: {self.primal_val}{RESET}")
        
        ## DUAL       ===================================================
        self.ampl.reset()

        overlap_dict = {}
        
        for i, pair in enumerate(self.overlapping_pairs):
            if pair[0] not in overlap_dict:
                overlap_dict[pair[0]] = [pair[1]]
            else:
                overlap_dict[pair[0]].append(pair[1])

        dual_constraints = ""
        
        # Tasks that don't overlap with anything
        for i in range(self.solver.n):
            cts = f"s.t. overlap_{i}: "
            if i not in overlap_dict:
                cts += f"s[{i}] >= p[{i}];\n"
            else:
                overlaps_with_i = overlap_dict[i]
                overlap_terms = [f"c_{i}_{j}" for j in overlaps_with_i]
                overlap_terms_str = " + ".join(overlap_terms)
                cts += f"{overlap_terms_str} + s[{i}] >= p[{i}];\n"
            dual_constraints += cts   
            
        c_terms = [f"c_{i}_{j}" for (i,j) in self.overlapping_pairs]
        c_terms = set(c_terms)
        c_str = ""
        for term in c_terms:
            c_str += f"var {term} >= 0;\n" 
            
        # Define the model
        model = f"""
            set RANGE := 0..{self.solver.n-1};
            set O := 0..{len(self.overlapping_pairs)-1};
            
            var p{{RANGE}};
            
            # Dual vars constraint: >= 0
            {c_str}
            var s{{RANGE}} >= 0;
            
            minimize z: {" + ".join(c_terms)} + sum{{k in RANGE}} s[k];
            
            # Profit is less than or equal to 'overlapping' cost + s[i]
            {dual_constraints} 
            """
        print(model)
        self.ampl.eval(model)
            
        # Fill in the cost 
        for i, c in enumerate(self.ratings):
            self.ampl.eval(f"fix p[{i}] := {c};")
            
        # Solve 
        self.ampl.option["solver"] = "gurobi"
        self.ampl.solve()
            
        # Get the solution
        self.dual_s = self.ampl.get_variable("s")
            
        # Print out the result of AMPL
        self.dual_sol_c = {}
        for pair in self.overlapping_pairs:
            c = f"c_{pair[0]}_{pair[1]}"
            self.dual_sol_c[c] = self.ampl.get_value(c)
            
        self.dual_sol_s = []
        for i in range(self.solver.n):
            self.dual_sol_s.append(str(self.dual_s[i].value()))
                
        # Get the optimal value
        self.dual_val = self.ampl.get_value('z')
                    
        print(f"{PURPLE}AMPL Dual LP solution:\n>\tc = {self.dual_sol_c}\n>\ts = {', '.join(self.dual_sol_s)}\n>\tOptimal value: {self.dual_val}{RESET}")
            
    def testCompareDualvsPrimal(self):
        self.assertEqual(self.primal_val, self.dual_val)