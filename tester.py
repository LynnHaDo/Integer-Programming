from solver import SchedulingSolver

# Time utils
from utils import TimeConverter

if __name__ == "__main__":
    time_converter = TimeConverter()
    
    # Test on timetable data
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
        
        print(solver.dp())