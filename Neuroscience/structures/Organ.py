import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import os
import sys

from utils import *

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(project_root)
# from structures.Abstract_Neuron import Abstract_Neuron
# from structures.Excitatory_Neuron import Excitatory_Neuron
# from structures.Inhibitory_Neuron import Inhibitory_Neuron

class Organ: 


    def __init__(self):
        self.brain = []
        self.input = []
        self.output = []
        self.network = []
        self.adjacency = AdjacencyMatrix()


    def tune(self, index, weigths):
        self.brain[index].set_weights(weigths)

    def get_voltage(self):
        return "organ voltage"
    
    def add_to_brain(self,neuron):
        self.brain.append(neuron)
    
    def update_adjacency_matrix(self): #costly function (O(n^2))
        if len(self.brain) != self.adjacency.size :
            self.adjacency = AdjacencyMatrix(len(self.brain))
        for i in range(len(self.brain)):
            for j in range(len(self.brain)):
                ni = self.brain[i]
                nj = self.brain[j]
                if ni.is_connected(nj):
                        self.adjacency.add_edge(i,j)


    def print_network(self, name):
        neuron_types = [neuron.type for neuron in self.brain]
        # self.adjacency.plot_force_directed_graph(neuron_types,graph_name = name)
        self.adjacency.plot_force_directed_graph(neuron_types, graph_name = name)

    
    def connect (self,index, neuron):
        self.brain[index].connect_with_neuron(neuron)

    def replace(self,index, neuron):
        self.brain[index]= neuron



    def simulate(self,k,V):

        neuron_count = 0
        # One for loop for calculating the state of the neurons with the current inputs

        for neuron in self.brain:
            # If there's an input present and an action potential is not going on,
            # then prepare to keep track of the voltage and reinitialize timers
            neuron.present_inputs(neuron.inputs)
            # If there's no active potential taking place,
            # call spatial_summation function to keep track of the overall voltage in the neuron
            if not neuron.active_potential_bool:
                # print("k,neuron_count : ",k,neuron_count)
                # print(k)
                # print(neuron_count)
                V[neuron_count][k] = neuron.spatial_summation()

            # There is an active potential taking place
            if neuron.active_potential_bool:
                neuron.time_neuron += 1
                # Call to active potential function
                pot = neuron.active_potential(neuron.time_neuron*neuron.resolution)

                V[neuron_count][k] = pot #... updating V along the way.
                # End of call to active potential function

            # The PSP or the active potential are over
            # Reset voltage, time, and temporal summation of the neuron to 0
            if not np.any(neuron.active_PSP) and not neuron.active_potential_bool:
                V[neuron_count][k] = 0
                neuron.time_neuron = 0
                neuron.membrane_potential = 0


            # Update current outputs of the neurons to their connected neurons for the next iteration
            neuron.propagate_outputs()

            # Update neuron counter
            neuron_count += 1