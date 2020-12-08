from .component import Component

class Resistor(Component):
    def __init__(self, id, value, nodes):
        super().__init__(id, value, nodes)
        self.type = 'Resistor'
        self.G = 1.0/self.value
        self.extra_nodes = 0

    def stamp(self,circuitA,circuitb):
        circuitA[self.nodes[0],self.nodes[0]] += self.G
        circuitA[self.nodes[0],self.nodes[1]] -= self.G
        circuitA[self.nodes[1],self.nodes[0]] -= self.G
        circuitA[self.nodes[1],self.nodes[1]] += self.G     
    
        



