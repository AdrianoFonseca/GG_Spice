from .solver import Solver
import numpy as np

class DCSolver(Solver):

    def __init__(self, elements_list, num_nodes):
        super().__init__(elements_list, num_nodes)
        self.update_system()

    
    def update_system(self):
        for element in self.elements_list:
            element.stamp(self.circuitA, self.circuitB)

    def solve(self):
        return np.linalg.solve(self.circuitA[1:,1:],self.circuitB[1:])

    def debug(self):
        print(self.circuitA, self.circuitB)