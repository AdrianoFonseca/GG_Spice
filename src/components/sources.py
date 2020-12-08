from .component import Component

class CurrentSource(Component):
    def __init__(self, id, value, nodes):
        super().__init__(id, value, nodes)
        self.type = 'Current Source'        
    
    def stamp(self,circuitA,circuitb):
        circuitb[self.nodes[0]] -= self.value
        circuitb[self.nodes[1]] += self.value
    

class VoltageSource(Component):

    def __init__(self, id, value, nodes, extra_nodes):
        super().__init__(id, value, nodes)
        self.type = 'Voltage Source'
        self.extra_nodes = extra_nodes
        
    def stamp(self,circuitA,circuitb):
        circuitA[self.nodes[0]][self.extra_nodes] += 1.0
        circuitA[self.nodes[1]][self.extra_nodes] += -1.0
        circuitA[self.extra_nodes][self.nodes[0]] += -1.0
        circuitA[self.extra_nodes][self.nodes[1]] += 1.0
        
        circuitb[self.extra_nodes][0] += -self.value


class VCVSource(Component):

    def __init__(self, id, value, nodes, extra_nodes):
        super().__init__(id, value, nodes)
        self.type = 'Voltage Controlled Voltage Source'
        self.extra_nodes = extra_nodes
        
    def stamp(self,circuitA,circuitb):
        circuitA[self.nodes[0]][self.extra_nodes] += 1.0
        circuitA[self.nodes[1]][self.extra_nodes] += -1.0


        circuitA[self.extra_nodes][self.nodes[0]] += -1.0
        circuitA[self.extra_nodes][self.nodes[1]] += 1.0
        circuitA[self.extra_nodes][self.nodes[2]] += self.value
        circuitA[self.extra_nodes][self.nodes[3]] += -self.value		

class CCCSource(Component):

    def __init__(self, id, value, nodes, extra_nodes):
        super().__init__(id, value, nodes)
        self.type = 'Current Controlled Current Source'
        self.extra_nodes = extra_nodes
        
    def stamp(self,circuitA,circuitb):
        circuitA[self.nodes[0]][self.extra_nodes] += self.value
        circuitA[self.nodes[1]][self.extra_nodes] += -self.value
        circuitA[self.nodes[2]][self.extra_nodes] += 1.0
        circuitA[self.nodes[3]][self.extra_nodes] += -1.0


        circuitA[self.extra_nodes][self.nodes[2]] += -1.0
        circuitA[self.extra_nodes][self.nodes[3]] += 1.0	

class CCVSource(Component):

    def __init__(self, id, value, nodes, extra_nodes):
        super().__init__(id, value, nodes)
        self.type = 'Current Controlled Voltage Source'
        self.extra_nodes = extra_nodes
        
    def stamp(self,circuitA,circuitb):
        circuitA[self.nodes[0]][self.extra_nodes[1]] += 1.0
        circuitA[self.nodes[1]][self.extra_nodes[1]] += -1.0
        circuitA[self.nodes[2]][self.extra_nodes[0]] += 1.0
        circuitA[self.nodes[3]][self.extra_nodes[0]] += -1.0


        circuitA[self.extra_nodes[0]][self.nodes[2]] += -1.0
        circuitA[self.extra_nodes[0]][self.nodes[3]] += 1.0	
        circuitA[self.extra_nodes[1]][self.nodes[0]] += -1.0
        circuitA[self.extra_nodes[1]][self.nodes[1]] += 1.0	

        circuitA[self.extra_nodes[1]][self.extra_nodes[0]] += self.value	

class VCCSource(Component):

    def __init__(self, id, value, nodes):
        super().__init__(id, value, nodes)
        self.type = 'Voltage Controlled Current Source'
        
    def stamp(self,circuitA,circuitb):
        circuitA[self.nodes[0]][self.nodes[2]] += self.value
        circuitA[self.nodes[0]][self.nodes[3]] += -self.value
        circuitA[self.nodes[1]][self.nodes[2]] += -self.value
        circuitA[self.nodes[1]][self.nodes[3]] += self.value



