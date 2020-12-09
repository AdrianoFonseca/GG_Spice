from .component import Component

class Resistor(Component):
    def __init__(self, id, nodes, value):
        super().__init__(id, nodes, value)
        self.type = 'Resistor'
        self.G = 1.0/self.value

    def stamp(self,circuitA,circuitb):
        circuitA[self.nodes[0],self.nodes[0]] += self.G
        circuitA[self.nodes[0],self.nodes[1]] -= self.G
        circuitA[self.nodes[1],self.nodes[0]] -= self.G
        circuitA[self.nodes[1],self.nodes[1]] += self.G     
    
        
class Diode(Component):
    def __init__(self, id, nodes, js=4.3e-9, vt=25e-3, n=1.9):
        super().__init__(id, nodes, js)
        self.type = 'Diode'
        self.js = js
        self.n = n
        self.vt = vt


