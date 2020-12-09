from .component import Component

class OpAmp(Component):
    def __init__(self, id, nodes, value, extra_nodes):
        super().__init__(id, nodes, value)
        self.type = 'Ideal Operational Amplifier'
        self.extra_nodes = extra_nodes

    def stamp(self,circuitA,circuitb):
        circuitA[self.nodes[0],self.extra_nodes] += 1
        circuitA[self.nodes[1],self.extra_nodes] -= 1
        circuitA[self.extra_nodes,self.nodes[2]] += 1
        circuitA[self.extra_nodes,self.nodes[3]] -= 1     
    
        



