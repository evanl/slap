import numpy as np
class Element(object):
    """ 
    Summary: 
    Elements are elements with no head-specified information. 
    These elements contribute to potential but do not need to be called
    during the solution scheme.

    Elements take in a model as well as a scaling parameter
    
    """
    def __init__(self, model_in, param_in):
        self.model = model_in
        self.parameter = param_in
    def __str__(self):
        print "Element"
        return 'Parameter {0}'.format(self.parameter)
    def potential(self, x, y):
        return self.parameter * self.pot_unit(x, y)
        
class Well(Element):
    """ 
    Summary: Wells provide pumping sources to and from the aquifer
    """
    def __init__(self, model_in, x_center, y_center, flow_rate, r_w):
        Element.__init__(self, model_in, Q)
        self.x_c = x_center
        self.y_c = y_center
        self.z_c = complex(x_center, y_center)
        self.r_w = rw

    def pot_unit(self, x, y):
        r_sq = pow(x - self.x_c, 2) + pow(y - self.y_c, 2)
        z = complex(x,y)
        if r_sq < pow(rw, 2):
            z = complex(self.x_c + np.sqrt(self.r_w_sq), self.y_c)
        return np.log((z - self.z_c)/self.rw)

class UniformFlow(Element):
    """
    Summary:
    Uniform flow simulates a background flow in the aquifer
    """
    def __init__(self, model_in, gradient, angle_deg):
        Element.__init__(self, model_in, gradient)
        self.angle_rad = angle_deg * np.pi / 180.
    def __str__(self):
        print "Uniform Flow"
        return '\tMagnitude: {0} \n\
        Direction: {1}'.format(self.parameter, self.angle_rad * 180 / np.pi)
    def pot_unit(self, x, y):
        return -complex(x,y) * np.exp( -1j * self.angle_rad)
