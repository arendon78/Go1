import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(project_root)

from Neuroscience.structures.Abstract_Neuron import Abstract_Neuron

class Inhibitory_Neuron(Abstract_Neuron):
    """
    A class representing an inhibitory neuron in a neural network.

    The `Inhibitory_Neuron` class inherits from `Abstract_Neuron` and is used to simulate the behavior 
    of neurons that primarily inhibit other neurons. This class includes specific methods for setting 
    axon terminals, propagating outputs to connected neurons, and printing neuron details.

    Attributes
    ----------
    type : str
        The type of the neuron, initialized as "Inhibitory".
    
    name : str
        The name of the neuron, initialized as "Inhibitory_Neuron".
    """

    def set_axon_terminals(self):
        """
        Activates all axon terminals of the neuron with an inhibitory signal.

        This method sets all axon terminals to output a value of -1, indicating that the neuron is actively 
        sending inhibitory signals.
        """
        for i in range(self.num_axon_terminals):
            self.axon_terminals[i][1] = -1

    def propagate_outputs(self):
        """
        Propagates outputs to connected neurons based on the neuron's current state.

        If the neuron has reached its maximum active potential, it sends an inhibitory signal (value of -1) 
        to all connected neurons. Otherwise, it sends a signal of 0.
        """
        for item in self.axon_terminals:
            if self.max_active_potential:
                item[0].inputs[item[1]] = -1
            else:
                item[0].inputs[item[1]] = 0

    def print(self):
        """
        Prints details about the inhibitory neuron, including the number of dendrites and axon terminals.
        """
        print("Inhibitory Neuron")
        print("dendrites : ", self.num_dendrites)
        print("axon terminals : ", self.num_axon_terminals)

    def __init__(self, res, inputs, outputs, instance_count=""):
        """
        Initializes an instance of `Inhibitory_Neuron`.

        :param res: The resolution of the simulation, affecting time steps.
        :type res: int
        :param inputs: Number of dendrites (input connections) for the neuron.
        :type inputs: int
        :param outputs: Number of axon terminals (output connections) for the neuron.
        :type outputs: int
        :param instance_count: A string to distinguish different instances, default is an empty string.
        :type instance_count: str, optional
        """
        super().__init__(res, inputs, outputs, instance_count=instance_count)
        self.type = "Inhibitory"
        self.name = "Inhibitory_Neuron"
