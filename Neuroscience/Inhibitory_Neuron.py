from Abstract_Neuron import Abstract_Neuron

# Definition of class Inhibitory_Neuron, inherits from AbstractNeuron
class Inhibitory_Neuron(Abstract_Neuron):

    def set_axon_terminals(self):
        # Turn all axon terminals on
        for i in range(self.num_axon_terminals):
            self.axon_terminals[i][1] = -1

    def propagate_outputs(self):
        # Update inputs from connected neurons
        for item in self.axon_terminals:
            if self.max_active_potential:
                item[0].inputs[item[1]] = -1
            else:
                item[0].inputs[item[1]] = 0

    def __init__(self, res, inputs, outputs):
        super().__init__(res, inputs, outputs)# calls the constructor of AbstractNeuron class (prevents duplicated code)