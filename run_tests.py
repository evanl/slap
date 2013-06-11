import unittest
import numpy as np
import model as m
import element as e
class TestSlap(unittest.TestCase):
    """ Runs a handful of test cases for the elements
    """
    def setUp(self):
        k0 = 10. # m/day
        thickness = 20. # meters
        self.test_model = m.Model(k0, thickness)

    def test_initialization(self):
        self.assertEqual(10., self.test_model.conductivity(0., 0.))
        self.assertEqual(20., self.test_model.thickness(0., 0.))
    # tests to be written
    # test head and potential function switches
    # test uniform flow
    # test well
    # test plotting functions
if __name__ == "__main__":
    unittest.main()
