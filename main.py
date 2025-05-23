# Colors (for formatting)
from utils import RED, GREEN, RESET

# Test suite
import unittest
from tests import TestGeneral, TestTimetable, TestFlights, TestTimetableMCKS, TestDualPrimal

if __name__ == "__main__":    
    padding = "=" * 40
    
    # print(f"\n{GREEN}TASK SCHEDULING [WITHOUT CONSTRAINTS]\t{padding}{RESET}\n")
    # print(f"{RED}Leetcode Examples{RESET}\n")
    # general_suite = unittest.TestLoader().loadTestsFromTestCase(TestGeneral)
    # unittest.TextTestRunner(verbosity=2).run(general_suite)
    
    # print(f"\n{RED}Timetable (against AMPL){RESET}\n")
    # timetable_suite = unittest.TestLoader().loadTestsFromTestCase(TestTimetable)
    # unittest.TextTestRunner(verbosity=2).run(timetable_suite)
    
    # print(f"\n{RED}Flights (against AMPL){RESET}\n")
    # flights_suite = unittest.TestLoader().loadTestsFromTestCase(TestFlights)
    # unittest.TextTestRunner(verbosity=2).run(flights_suite)
    
    # print(f"\n{GREEN}TASK SCHEDULING [WITH CONSTRAINTS]\t{padding}{RESET}\n")
    
    # print(f"\n{RED}Timetable (AMPL){RESET}\n")
    # timetable_mc_suite = unittest.TestLoader().loadTestsFromTestCase(TestTimetableMCKS)
    # unittest.TextTestRunner(verbosity=2).run(timetable_mc_suite)
    
    print(f"\n{GREEN}TASK SCHEDULING [PRIMAL - DUAL TEST]\t{padding}{RESET}\n")
    
    print(f"\n{RED}Timetable (AMPL){RESET}\n")
    timetable_dual_suite = unittest.TestLoader().loadTestsFromTestCase(TestDualPrimal)
    unittest.TextTestRunner(verbosity=2).run(timetable_dual_suite)
    
    