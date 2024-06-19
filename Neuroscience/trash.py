import numpy as np
# Define the Organ class
class Organ:
    def __init__(self):
        self.brain = []

    def get_voltage(self):
        return "Organ Voltage"

    def simulate(self, k, V):
        print("Calling get_voltage within Organ's simulate:")
        print(self.get_voltage())  # This will call the method from the instance's class

# Define the Abstract_Neuron class
class Abstract_Neuron(Organ):
    def __init__(self, res, inputs, outputs):
        super().__init__()
        self.volt_dendrites = np.zeros(inputs)

    def get_voltage(self):
        return self.volt_dendrites  # This method overrides the one in Organ

# Define the Excitatory_Neuron class
class Excitatory_Neuron(Abstract_Neuron):
    def __init__(self, res, inputs, outputs):
        super().__init__(res, inputs, outputs)

    def set_axon_terminals(self):
        for i in range(self.num_axon_terminals):
            self.axon_terminals[i][1] = 1

    def propagate_outputs(self):
        for item in self.axon_terminals:
            if self.max_active_potential:
                item[0].inputs[item[1]] = 1
            else:
                item[0].inputs[item[1]] = 0

# Create an instance of Excitatory_Neuron
neuron = Excitatory_Neuron(res=1.0, inputs=10, outputs=5)

# Use simulate method on the Excitatory_Neuron instance
print("Using simulate method on Excitatory_Neuron instance:")
neuron.simulate(0, np.zeros((1, 10)))  # This will use the simulate method from Organ but get_voltage from Abstract_Neuron
