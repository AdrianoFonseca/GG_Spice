from components.resistor import *
from components.opamp import *
from components.sources import *

class Parser():
    def __init__(self, filename):
        self.filename = filename
        self.num_nodes = 0
        self.elements, self.out_names = self.parse(self.filename)

    #transform Sip string into Float
    @staticmethod
    def sip2num(net_value):
        postfix = {'k' : 1e3, 'M' : 1e6, 'G' : 1e9, 'T' : 1e12, 
                    'm' : 1e-3, 'u' : 1e-6, 'n' : 1e-9, 'p' : 1e-12, 'f' : 1e-15}
        
        if net_value[-1].isnumeric():
            return float(net_value)
            
        num_postfix = net_value[-1]
        num = float(net_value[:-1]) 

        return num*postfix[num_postfix]


    def parse(self,netlist):

        netfile = open(netlist, "r")

        first_line = netfile.readline() 

        self.num_nodes = int(first_line.split()[0]) + 1

        out_names = ['e' + str(i) for i in range(1,self.num_nodes)]

        elements = []

        for line in netfile:

            component_id, *args = line.split()   

            if component_id[0].lower() == 'r':
                component_nodes = [int(args[0]), int(args[1])]
                component_value = self.sip2num(args[2])
                elements.append(Resistor(component_id, component_value, component_nodes))
                
            elif component_id[0].lower() == 'i':
                component_nodes = [int(args[0]), int(args[1])]
                component_value = self.sip2num(args[3])
                elements.append(CurrentSource(component_id, component_value, component_nodes))

            elif component_id[0].lower() == 'v':
                component_nodes = [int(args[0]), int(args[1])]
                component_value = self.sip2num(args[3])
                elements.append(VoltageSource(component_id, component_value, component_nodes, self.num_nodes))
                self.num_nodes += 1
                out_names.append('j' + component_id)

            elif component_id[0].lower() == 'e':
                component_nodes = [int(args[0]), int(args[1]), int(args[2]), int(args[3])]
                component_value = self.sip2num(args[4])
                elements.append(VCVSource(component_id, component_value, component_nodes, self.num_nodes))
                self.num_nodes += 1
                out_names.append('j' + component_id)

            elif component_id[0].lower() == 'f':
                component_nodes = [int(args[0]), int(args[1]), int(args[2]), int(args[3])]
                component_value = self.sip2num(args[4])
                elements.append(CCCSource(component_id, component_value, component_nodes, self.num_nodes))
                self.num_nodes += 1 
                out_names.append('j' + component_id)

            elif component_id[0].lower() == 'h':
                component_nodes = [int(args[0]), int(args[1]), int(args[2]), int(args[3])]
                component_value = self.sip2num(args[4])
                elements.append(CCVSource(component_id, component_value, component_nodes, [self.num_nodes,self.num_nodes + 1]))
                self.num_nodes += 2
                out_names.append('jx' + component_id)
                out_names.append('jy' + component_id)

            elif component_id[0].lower() == 'g':
                component_nodes = [int(args[0]), int(args[1]), int(args[2]), int(args[3])]
                component_value = self.sip2num(args[4])
                elements.append(VCCSource(component_id, component_value, component_nodes))

            elif component_id[0].lower() == 'o':
                component_nodes = [int(args[0]), int(args[1]), int(args[2]), int(args[3])]
                elements.append(OpAmp(component_id, None, component_nodes, self.num_nodes))
                self.num_nodes += 1
                out_names.append('j' + component_id)

            else:
                print('Invalid Element in Netlist!!')

        
        return elements, out_names

    
