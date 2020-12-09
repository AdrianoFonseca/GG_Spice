from .component import Component
import numpy as np

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
        self.vt = n*vt
        self.linear = False

        self.vd = 0.6
        self.G = self.diode_conductance(self.vd)
        self.I = self.diode_current(self.vd) - self.G*self.vd

    def stamp(self,circuitA,circuitb,add=1):

        G = self.G * add
        I = self.I * add

        circuitA[self.nodes[0],self.nodes[0]] += G
        circuitA[self.nodes[0],self.nodes[1]] -= G
        circuitA[self.nodes[1],self.nodes[0]] -= G
        circuitA[self.nodes[1],self.nodes[1]] += G  

        circuitb[self.nodes[0]] -= I
        circuitb[self.nodes[1]] += I

    def update_biaspoint(self,circuitE, circuitA,circuitb):

        self.stamp(circuitA,circuitb,-1)

        vd = circuitE[self.nodes[0]] - circuitE[self.nodes[1]]
        
        self.vd = vd[0]
        self.G = self.diode_conductance(self.vd) 
        self.I = self.diode_current(self.vd) - self.G*self.vd

        self.stamp(circuitA,circuitb,1)


        
    def diode_current(self,vd):
	    return(self.js*(np.exp(vd/self.vt)-1))

    def diode_conductance(self,vd):
	    return((self.js/self.vt)*np.exp(vd/self.vt))


