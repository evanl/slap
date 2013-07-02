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
        self.has_unknown = False

    def __str__(self):
        print "Element"
        return 'Parameter {0}'.format(self.parameter)

    def potential(self, x, y):
        return self.parameter * self.pot_unit(x, y)

    def solve(self):
        return converged == True
        
class Well(Element):
    """ 
    Summary: Wells provide pumping sources to and from the aquifer
    """
    def __init__(self, model_in, x_center, y_center, flow_rate, r_w, head_spec = False):
        Element.__init__(self, model_in, Q)
        self.x_c = x_center
        self.y_c = y_center
        self.z_c = complex(x_center, y_center)
        self.r_w = rw
        self.head_spec = head_spec

    def __str__(self):
        print "Well"
        print "Well Location (x, y): ({0}, {1})".format(self.x_c, self.y_c)
        print "Current Q: {0}".format(self.parameter)
        return "Head - Specified: {0}".format(self.head_spec)

    def set_reference(self, x, y):
        """
        Each well requires the location of the reference point to set the correct pumping rate
        """
        self.ref_x = x
        self.ref_y = y

    def pot_unit(self, x, y):
        r_sq = pow(x - self.x_c, 2) + pow(y - self.y_c, 2)
        z = complex(x,y)
        if r_sq < pow(rw, 2):
            z = complex(self.x_c + np.sqrt(self.r_w_sq), self.y_c)
        return np.log((z - self.z_c)/self.rw)

    def solve(self, tolerance, omit_index ):
        if head_spec == False:
            return True
        else:
            q_old = self.parameter

            pot_well = self.model.pot_from_head(self.head_spec, self.x_c + self.r_w, self.y_c)
            pot_other = self.model.potential(self.x_c + self.r_w, self.y_c, omit_index = omit_index)

            unit_well = self.pot_unit(self.x_c + rw, self.yc).real
            unit_ref = self.pot_unit(self.ref_x, self.ref_y).real

            self.parameter = (pot_well - pot_other) / (unit_well - unit_other)

        return abs(self.parameter - q_old) < tolerance

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

class ReferencePoint(Element):
    """
    Summary:
    Provides a reference water level at a given location
    """
    def __init__(self, model_in, x, y, head_ref, c_initial = 0.):
        Element.__init__(self, model_in, c_initial)
        self.x_ref = x
        self.y_ref = y
        self.z_ref = complex(x,y)
        self.head_ref = head_ref

    def __str__(self):
        print "Reference Point"
        print "\tLocation (x, y) = ({0}, {1})".format(self.x_ref, self.y_ref)
        print "\tReference Head: {0}\n".format(self.head_ref)
        return "\t Constant: {0}".format(self.parameter)

    def pot_unit(self,x,y):
        return 1.

    def solve(self, tolerance, omit_index ):
        c_old = self.parameter
        self.parameter = self.model.pot_from_head(self.head_ref, self.x_ref, self.y_ref) -\
                self.model.potential(self.x_ref, self.y_ref, omit_index = omit_index).real
        return abs(c_old - self.parameter) < tolerance
