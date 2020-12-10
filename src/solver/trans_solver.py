from .solver import Solver
from .dc_solver import DCSolver
import numpy as np

class TransSolver(Solver):

    def __init__(self, elements_list, num_nodes, final_t, step,  max_iter = 200, tol = 1e-8):
        super().__init__(elements_list, num_nodes)
        self.max_iter = max_iter
        self.tol = tol
        self.final_t = final_t
        self.step = step
        self.DC = DCSolver(elements_list, num_nodes,self.max_iter,self.tol)
        self.circuitE = self.DC.NewtonRaphson()
        self.dynamic_elements = self.find_dynamic()

    def find_dynamic(self):
        for element in self.elements_list:
                if(element.dynamic):
                    self.dynamic_elements.append(element)

    def update_step(self):
        for step in range(self.max_iter):

            for element in self.dynamic_elements:
                pass
                #update stamp

            self.circuitE = self.DC.NewtonRapshon()

    def show_output(self):
        print(self.circuitE[1:])