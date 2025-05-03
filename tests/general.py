import unittest

from models import SchedulingSolver

class TestGeneral(unittest.TestCase):
    def setUp(self):
        super().setUp()
        # Test 1
        startTimes = [1,2,3,4,6]
        endTimes = [3,5,10,6,9]
        profit = [20,20,100,70,60]
        self.solver1 = SchedulingSolver(startTimes, endTimes, profit)
        
        # Test 2
        startTimes = [1,2,3,3]
        endTimes = [3,4,5,6]
        profit = [50,10,40,70]
        
        self.solver2 = SchedulingSolver(startTimes, endTimes, profit)
        
        # Test 3
        startTimes = [1,1,1]
        endTimes = [2,3,4]
        profit = [5,6,4]
        
        self.solver3 = SchedulingSolver(startTimes, endTimes, profit)
    
    # Test 1 =======================================================
    
    def test_one_dp(self): 
        dp_sol = self.solver1.dp()
        self.assertEqual(150, dp_sol[0])
    
    def test_one_dt(self):
        dt_sol = self.solver1.decision_tree()
        self.assertEqual(150, dt_sol[0])
    
    def test_one_bnb(self):
        bnb_sol = self.solver1.branch_and_bound()
        self.assertEqual(150, bnb_sol[1])
    
    # Test 2 =======================================================
    
    def test_two_dp(self): 
        dp_sol = self.solver2.dp()
        self.assertEqual(120, dp_sol[0])
    
    def test_two_dt(self):
        dt_sol = self.solver2.decision_tree()
        self.assertEqual(120, dt_sol[0])
    
    def test_two_bnb(self):
        bnb_sol = self.solver2.branch_and_bound()
        self.assertEqual(120, bnb_sol[1])
    
    # Test 3 =======================================================
    
    def test_three_dp(self): 
        dp_sol = self.solver3.dp()
        self.assertEqual(6, dp_sol[0])
    
    def test_three_dt(self):
        dt_sol = self.solver3.decision_tree()
        self.assertEqual(6, dt_sol[0])
    
    def test_three_bnb(self):
        bnb_sol = self.solver3.branch_and_bound()
        self.assertEqual(6, bnb_sol[1])

if __name__ == '__main__':
    unittest.main()