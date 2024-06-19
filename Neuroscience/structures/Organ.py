import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import os
import sys

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

    def tune(self, index, weigths):
        self.brain[index].set_weights(weigths)

    def get_voltage(self):
        return "organ voltage"
    
    def add_to_brain(self,neuron):
        self.brain.append(neuron)
    
    def connect (self,index, neuron):
        self.brain[index].connect_with_neuron(neuron)

    def replace(self,index, neuron):
        self.brain[index]= neuron



    def simulate(self,k,V,useV = True):

        neuron_count = 0
        # One for loop for calculating the state of the neurons with the current inputs
        for neuron in self.brain:
            # print("neuron self voltage : ", neuron.membrane_potential)
            # print("self brain, brain length")
            # print(self.brain)
            # print(len(self.brain))
            # If there's an input present and an action potential is not going on,
            # then prepare to keep track of the voltage and reinitialize timers
            neuron.present_inputs(neuron.inputs)
            # If there's no active potential taking place,
            # call spatial_summation function to keep track of the overall voltage in the neuron
            if not neuron.active_potential_bool:
                # print("should print ! 0")
                # print(neuron_count)
                if useV:
                    
                    V[neuron_count][k] = neuron.spatial_summation()
                    # print("not active potential. potential is : ",V[neuron_count][k] )

            # There is an active potential taking place
            if neuron.active_potential_bool:
                neuron.time_neuron += 1
                # Call to active potential function
                # print("should print ! 1")
                pot = neuron.active_potential(neuron.time_neuron*neuron.resolution)
                if useV:
                    V[neuron_count][k] = pot #... updating V along the way.
                # print("active potential. potential is : ",V[neuron_count][k])
                # End of call to active potential function

            # The PSP or the active potential are over
            # Reset voltage, time, and temporal summation of the neuron to 0
            if not np.any(neuron.active_PSP) and not neuron.active_potential_bool:
                # print("reset")
                if useV:
                    V[neuron_count][k] = 0
                neuron.time_neuron = 0
                neuron.membrane_potential = 0


            # Update current outputs of the neurons to their connected neurons for the next iteration
            neuron.propagate_outputs()

            # Update neuron counter
            neuron_count += 1

    def build_and_display_neuron_graph(self):
        from Neuroscience.structures.Excitatory_Neuron import Excitatory_Neuron
        from Neuroscience.structures.Inhibitory_Neuron import Inhibitory_Neuron
        G = nx.DiGraph()  # Directed graph since connections have direction

        # Add nodes to the graph with the neuron's name
        for neuron in self.brain:
            G.add_node(neuron.name)

        # Add edges based on neuron connections
        for neuron in self.brain:
            for terminal in neuron.axon_terminals:
                target_neuron, target_index = terminal
                G.add_edge(neuron.name, target_neuron.name)

        # Use the Kamada-Kawai layout
        pos = nx.kamada_kawai_layout(G)

        plt.figure(figsize=(12, 10))  # Increase the figure size for better readability

        # Draw nodes with different colors and sizes based on neuron type
        node_colors = []
        node_sizes = []
        for neuron in self.brain:
            if isinstance(neuron, Excitatory_Neuron):
                node_colors.append('skyblue')
                node_sizes.append(700)
            elif isinstance(neuron, Inhibitory_Neuron):
                node_colors.append('lightcoral')
                node_sizes.append(500)
            else:
                node_colors.append('lightgrey')
                node_sizes.append(600)

        # Debug prints
        print(f"Number of nodes in graph: {len(G.nodes())}")
        print(f"Number of elements in node_sizes: {len(node_sizes)}")
        print(f"Number of elements in node_colors: {len(node_colors)}")
        print(f"Nodes in graph: {list(G.nodes())}")
        print(f"Node sizes: {node_sizes}")
        print(f"Node colors: {node_colors}")

        # Ensure node_sizes and node_colors have the correct length
        if len(node_sizes) != len(G.nodes()) or len(node_colors) != len(G.nodes()):
            raise ValueError("node_sizes and node_colors lists must have the same number of elements as there are nodes in the graph.")

        nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color=node_colors, edgecolors='black')

        # Draw edges with arrowheads and different styles
        nx.draw_networkx_edges(G, pos, arrowstyle='->', arrowsize=20, edge_color='gray')

        # Draw labels with increased font size for better readability
        nx.draw_networkx_labels(G, pos, font_size=12, font_family='sans-serif')

        # Create a legend
        exc_patch = plt.Line2D([0], [0], marker='o', color='w', label='Excitatory Neuron',
                               markerfacecolor='skyblue', markersize=10, markeredgecolor='black')
        inh_patch = plt.Line2D([0], [0], marker='o', color='w', label='Inhibitory Neuron',
                               markerfacecolor='lightcoral', markersize=10, markeredgecolor='black')
        other_patch = plt.Line2D([0], [0], marker='o', color='w', label='Other Neuron',
                                 markerfacecolor='lightgrey', markersize=10, markeredgecolor='black')

        plt.legend(handles=[exc_patch, inh_patch, other_patch], loc='upper left', fontsize='large')

        plt.title("Neuron Connection Graph")
        plt.axis('off')
        plt.show()