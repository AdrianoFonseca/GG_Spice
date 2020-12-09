import numpy as np

class Solver():
    def __init__(self, elements_list, num_nodes):
        self.elements_list = elements_list
        self.nonlinear = []
        self.circuitA = np.zeros((num_nodes, num_nodes))
        self.circuitb = np.zeros((num_nodes, 1))
        self.circuitE = np.zeros((num_nodes, 1))
        
    def update_system():
        pass
    
    def solve(self):
        pass

    def debug(self):
        pass

    def show_output(self):
        pass