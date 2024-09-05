import numpy as np
import os
import sys

from utils import *

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(project_root)
# from structures.Abstract_Neuron import Abstract_Neuron
# from structures.Excitatory_Neuron import Excitatory_Neuron
# from structures.Inhibitory_Neuron import Inhibitory_Neuron

class Organ:
    """
    A class representing an organ in a neural network model, consisting of multiple neurons and managing their interactions.

    The `Organ` class serves as a container for neurons, managing their connections, updating the adjacency matrix,
    and simulating the neural activity. It can be used to represent more complex structures within a neural network.

    Attributes
    ----------
    name : str
        The name of the organ. If not overridden, defaults to "Your class does not implement name attribute (it should)".
    
    brain : list of Abstract_Neuron
        A list of neurons that make up the organ.
    
    input_neurons : list of Abstract_Neuron
        A list of input neurons for the organ.
    
    output_neurons : list of Abstract_Neuron
        A list of output neurons for the organ.
    
    network : list
        A list representing the network connections within the organ.
    
    adjacency : AdjacencyMatrix
        An adjacency matrix representing the connections between neurons in the organ.
    """

    def __init__(self):
        """
        Initializes the Organ instance, setting up the basic attributes including the brain, input, and output neurons,
        as well as the network and adjacency matrix.
        """
        self.name = "Your class does not implement name attribute (it should)"
        self.brain = []
        self.input_neurons = []
        self.output_neurons = []
        self.network = []
        self.adjacency = AdjacencyMatrix()

    def tune(self, index, weights):
        """
        Tunes the weights of a specific neuron in the organ.

        :param index: The index of the neuron in the brain list.
        :type index: int
        :param weights: The new weights to be set for the neuron.
        :type weights: list of float
        """
        self.brain[index].set_weights(weights)

    def get_voltage(self):
        """
        Gets the voltage of the organ (currently a placeholder function).

        :returns: A string indicating that this is the organ voltage.
        :rtype: str
        """
        return "organ voltage"
    
    def add_to_brain(self, neuron):
        """
        Adds a neuron to the organ's brain.

        :param neuron: The neuron to be added to the brain list.
        :type neuron: Abstract_Neuron
        """
        self.brain.append(neuron)
    
    def update_adjacency_matrix(self):
        """
        Updates the adjacency matrix to reflect the current connections between neurons in the organ.

        This is a costly function with a time complexity of O(n^2), where n is the number of neurons.
        """
        if len(self.brain) != self.adjacency.size:
            self.adjacency = AdjacencyMatrix(len(self.brain))
        for i in range(len(self.brain)):
            for j in range(len(self.brain)):
                ni = self.brain[i]
                nj = self.brain[j]
                if ni.is_connected(nj):
                    self.adjacency.add_edge(i, j)

    def print_network(self, name):
        """
        Prints the network structure of the organ using the adjacency matrix.

        :param name: The name for the graph or network being printed.
        :type name: str
        """
        neuron_types = [neuron.type for neuron in self.brain]
        self.adjacency.plot_force_directed_graph(neuron_types, name)
    
    def connect(self, index, neuron):
        """
        Connects a neuron at a specified index in the brain to another neuron.

        :param index: The index of the neuron in the brain list.
        :type index: int
        :param neuron: The neuron to connect with.
        :type neuron: Abstract_Neuron
        """
        self.brain[index].connect_with_neuron(neuron)

    def replace(self, index, neuron):
        """
        Replaces a neuron at a specified index in the brain with another neuron.

        :param index: The index of the neuron to be replaced.
        :type index: int
        :param neuron: The new neuron to replace the old one.
        :type neuron: Abstract_Neuron
        """
        self.brain[index] = neuron

    def simulate(self, k, V):
        """
        Simulates the neural activity within the organ for a single time step.

        :param k: The current time step in the simulation.
        :type k: int
        :param V: A matrix to store the membrane potentials of the neurons over time.
        :type V: numpy.ndarray
        """
        neuron_count = 0

        # Calculate the state of each neuron based on current inputs
        for neuron in self.brain:
            neuron.present_inputs(neuron.inputs)
            
            if not neuron.active_potential_bool:
                V[neuron_count][k] = [k,neuron.spatial_summation()]

            if neuron.active_potential_bool:
                neuron.time_neuron += 1
                pot = neuron.active_potential(neuron.time_neuron * neuron.resolution)
                V[neuron_count][k] = [k,pot]

            if not np.any(neuron.active_PSP) and not neuron.active_potential_bool:
                V[neuron_count][k] = [k,0]
                neuron.time_neuron = 0
                neuron.membrane_potential = 0   

            neuron.propagate_outputs()
            neuron_count += 1
