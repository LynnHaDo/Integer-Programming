from models.solver import SchedulingSolver

# Time utils
from utils import TimeConverter
import time 

# Test suite
import unittest
from tests import TestGeneral

if __name__ == "__main__":
    GREEN = '\033[32m'
    RESET = '\033[0m'
    time_converter = TimeConverter()
    
    padding = "=" * 50
    print(f"{GREEN}GENERAL\t{padding}{RESET}\n")
    suite = unittest.TestLoader().loadTestsFromTestCase(TestGeneral)
    unittest.TextTestRunner(verbosity=2).run(suite)
    
    print("\n")
    # Test on timetable data
    print(f"{GREEN}TIMETABLE\t{padding}{RESET}\n")
    
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
        solver = SchedulingSolver(start, end, ratings)
        # Print result
        print(solver)
        
    print("\n")
    # Test on airplane data
    print(f"{GREEN}AIR FLIGHTS\t{padding}{RESET}\n")
    
    with open("data/flights.txt", "r") as f:
        start = []
        end = []
        ratings = []
        
        # Get all lines in the file
        lines = f.readlines()
        
        for line in lines:
            line_arr = line.split(",")
            s,e,r = line_arr[2:5]
            
            s = time_converter.time_to_minutes(s)
            e = time_converter.time_to_minutes(e)
            r = float(r)
            
            start.append(s)
            end.append(e)
            ratings.append(r)
        
        # Feed it to the solver
        solver = SchedulingSolver(start, end, ratings)
        # Print result 
        print(solver)
    
    