import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(project_root)


from Neuroscience.structures.Abstract_Neuron import Abstract_Neuron

# Definition of class Inhibitory_Neuron, inherits from AbstractNeuron
class Excitatory_Neuron(Abstract_Neuron):

    def print(self):
        print("Excitatory Neuron "+self.name)
        print("dendrites : ",self.num_dendrites)
        print("axon terminals : ", self.num_axon_terminals)

    def set_axon_terminals(self):
        # Turn all axon terminals on
        for i in range(self.num_axon_terminals):
            self.axon_terminals[i][1] = 1
            
    def propagate_outputs(self):
        # Update inputs from connected neurons
        for item in self.axon_terminals:
            if self.max_active_potential:
                item[0].inputs[item[1]] = 1
            else:
                item[0].inputs[item[1]] = 0

    def __init__(self, res, inputs, outputs,name =""):
        super().__init__(res, inputs, outputs,name = name) #calls the constructor of AbstractNeuron class (prevents duplicated code)
        self.type = "Excitatory"

    