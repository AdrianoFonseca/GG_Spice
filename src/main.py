from parser import Parser
from solver.dc_solver import DCSolver

if __name__ == '__main__':
    netlist_example = 'data/net.txt'
    parser = Parser(netlist_example)
    solver = DCSolver(parser.elements, parser.num_nodes)
    solver.NewtonRapshon()
    print(solver.circuitE)