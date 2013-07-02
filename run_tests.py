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
        self.assertRaises(IndexError, lambda: self.test_model.potential(0.,0.))
    def test_head_funcs(self):
        self.assertEqual(1125., self.test_model.pot_from_head(15., 0.,0.))
        self.assertEqual(3000., self.test_model.pot_from_head(25., 0.,0.))

    def test_uniform_flow(self):
        self.test_model.elements = []
        gradient = 0.1
        angle = 0.
        self.test_model.elements.append(e.UniformFlow(self.test_model,\
                gradient, angle))
        self.assertEqual(self.test_model.potential(10.,0.).real,-1.0)
        self.assertEqual(self.test_model.potential(10.,10.).real,-1.0)
        self.assertEqual(self.test_model.potential(-10.,-10.).real,1.0)
    def test_reference_point_pre_solve(self):
        self.test_model.elements = []
        gradient = 0.1
        angle = 0.
        self.test_model.elements.append(e.UniformFlow(self.test_model,\
                gradient, angle))
        head_reference = 30. 
        xr = -1000.
        yr = -1000.
        c_init = self.test_model.pot_from_head(30, xr, yr)
        self.assertEqual(c_init, 4000.)
        self.test_model.elements.append(e.ReferencePoint(self.test_model, xr, yr, \
                head_reference, c_initial = c_init))
        self.assertEqual(self.test_model.potential(10.,0.),3999.)
        self.assertEqual(self.test_model.potential(-10.,0.),4001.)

    # test head and potential function switches
    # test uniform flow
    # test well
    # test plotting functions
if __name__ == "__main__":
    unittest.main()
