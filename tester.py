from solver import SchedulingSolver

# Time utils
from utils import TimeConverter
import time 

if __name__ == "__main__":
    time_converter = TimeConverter()
    
    # Test on timetable data
    print("TIMETABLE OPTIMIZATION ======")
    
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
        
        begin = time.time()
        print(solver.dp())
        time.sleep(1)
        end = time.time()
        print(f"Total runtime of DP approach is {end - begin}")
        
        begin1 = time.time()
        print(solver.decision_tree())
        time.sleep(1)
        end1 = time.time()
        print(f"Total runtime of decision-tree approach is {end1 - begin1}")
    
    # Test on airplane data
    print("AIRPLANE OPTIMIZATION ======")
    
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
        
        begin = time.time()
        print(solver.dp())
        time.sleep(1)
        end = time.time()
        print(f"Total runtime of DP approach is {end - begin}")
        
        begin1 = time.time()
        print(solver.decision_tree())
        time.sleep(1)
        end1 = time.time()
        print(f"Total runtime of decision-tree approach is {end1 - begin1}")
    
    