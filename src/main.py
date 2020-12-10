from utils.parser import Parser
from solver.dc_solver import DCSolver
from solver.trans_solver import TransSolver

if __name__ == '__main__':
    netlist_example = 'data/net.txt'
    parser = Parser(netlist_example)
    solver = DCSolver(parser.elements, parser.num_nodes,0,0)
    print(solver.NewtonRaphson()[1:])
    print(parser.out_names)