# Time utils
from utils import TimeConverter
import time 

# Colors (for formatting)
from utils import RED, GREEN, RESET

# Test suite
import unittest
from tests import TestGeneral, TestTimetable, TestFlights

if __name__ == "__main__":    
    padding = "=" * 53
    print(f"\n{GREEN}UNIT TESTS\t{padding}{RESET}\n")
    print(f"{RED}Leetcode Examples{RESET}\n")
    general_suite = unittest.TestLoader().loadTestsFromTestCase(TestGeneral)
    unittest.TextTestRunner(verbosity=2).run(general_suite)
    
    print(f"\n{RED}Timetable (against AMPL){RESET}\n")
    timetable_suite = unittest.TestLoader().loadTestsFromTestCase(TestTimetable)
    unittest.TextTestRunner(verbosity=2).run(timetable_suite)
    
    print(f"\n{RED}Flights (against AMPL){RESET}\n")
    flights_suite = unittest.TestLoader().loadTestsFromTestCase(TestFlights)
    unittest.TextTestRunner(verbosity=2).run(flights_suite)