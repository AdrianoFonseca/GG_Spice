from .solver import Solver
import numpy as np

class DCSolver(Solver):

    def __init__(self, elements_list, num_nodes):
        super().__init__(elements_list, num_nodes)
        self.update_system()
        self.circuitE[1:] = self.solve()

    
    def update_system(self):
        for element in self.elements_list:
            element.stamp(self.circuitA, self.circuitb)
            if(not element.linear):
                self.nonlinear.append(element)

    def solve(self):
        return np.linalg.solve(self.circuitA[1:,1:],self.circuitb[1:])

    def NewtonRapshon(self):
        for iter in range(200):
            for element in self.nonlinear:
                element.update_biaspoint(self.circuitE, self.circuitA, self.circuitb)

            self.circuitE[1:]  = self.solve()
            
    def debug(self):
        print(self.circuitA, self.circuitB)

    def show_output(self):
        print(self.circuitE[1:])