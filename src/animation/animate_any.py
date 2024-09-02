
import random
import numpy as np
import networkx as nx 
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sys
import time


import json 

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
sys.path.append(project_root)



import manim as m

from Neuroscience.structures.Abstract_Neuron import Abstract_Neuron
from utils import *

ACT_POT = Abstract_Neuron.Act_Pot_volt

# Path to the JSON file
file_path = '/animation/datas'

name = '/Counter_4_bits'

file_abs_path = project_root + file_path + name

# Open and load JSON file
with open(file_abs_path + ".json", 'r') as file:
    data_json = json.load(file)

adjacency_matrices = []

# this module allows to animate any neural network.
# to animate a neural network, all you have to do is simulate it thanks to src/Neuroscience/tests/sim/simulate_any module
# you will get a json file that will be added to src/animation/datas
# by changing the "name" variable to the name of your file (that should be the name of the neural network you simulated) witout .json at the end, 
# you should be able to simulate it.

def pretty_print(matrix):
    """
    Displays the adjacency matrix using Seaborn's heatmap.
    
    Parameters
    ----------
    matrix : list of list of int
        The adjacency matrix.
    """
    plt.figure(figsize=(8, 8))
    sns.heatmap(matrix, annot=True, fmt='d', cbar=False, cmap='viridis', linewidths=0.5, linecolor='black')
    plt.title('Adjacency Matrix')
    plt.xlabel('Vertex')
    plt.ylabel('Vertex')
    plt.show()

def directed_to_undirected(adj_matrix):
    """
    Converts a directed adjacency matrix to an undirected one.
    
    Parameters
    ----------
    adj_matrix : list of list of int
        The directed adjacency matrix.

    Returns
    -------
    undirected_matrix : np.ndarray
        The undirected adjacency matrix.
    """
    # Convert the input to a numpy array for easier manipulation
    adj_matrix = np.array(adj_matrix)
    n = adj_matrix.shape[0]
    
    # Initialize the undirected adjacency matrix
    undirected_matrix = np.zeros_like(adj_matrix)
    
    # Iterate over the upper triangle of the matrix
    for i in range(n):
        for j in range(i + 1, n):
            # Apply OR operation between corresponding elements
            # in the upper and lower triangles
            undirected_matrix[i, j] = adj_matrix[i, j] | adj_matrix[j, i]
            undirected_matrix[j, i] = undirected_matrix[i, j]
    
    # Include the diagonal elements from the original matrix
    for i in range(n):
        undirected_matrix[i, i] = adj_matrix[i, i]
    return undirected_matrix


class Neuron(m.VMobject):
    """
    Visual representation of a neuron.

    Attributes
    ----------
    index : int
        The index of the neuron.
    radius : float
        The radius of the neuron's visual representation.
    color : m.Color
        The color of the neuron.
    original_color : m.Color
        The original color of the neuron.
    original_radius : float
        The original radius of the neuron.
    circle : m.Circle
        The visual representation of the neuron.
    label : m.Text
        The label displaying the neuron's index.
    """
    def __init__(self, index, radius=0.07, color=m.BLUE, **kwargs):
        super().__init__(**kwargs)
        self.radius = radius
        self.color = color
        self.original_color = color
        self.original_radius = self.radius
        self.circle = m.Circle(radius=self.radius, color=self.color, fill_opacity=1)

        self.label = m.Text(str(index), font_size=10, color=m.WHITE).next_to(self.circle, m.RIGHT,buff=0.0)

        self.add(self.circle,self.label)
    
    def activate(self):
        """Activate the neuron (change its color)."""
        self.circle.set_fill(m.YELLOW, opacity=1)
    
    def deactivate(self):
        """Deactivate the neuron (reset its color)."""
        self.circle.set_fill(self.color, opacity=1)


class NeuralNetwork(m.Scene):
    """
    Manim scene to visualize the neural network and its activity.

    This class constructs a visual representation of a neural network based on
    the data provided in the JSON file. It handles the placement of neurons,
    the drawing of connections, and the animation of neuron activations.
    """
    def construct(self):
        """
        Constructs the neural network visualization, applies forces to neurons,
        and animates their activations.
        """
          # Increase the frame width to zoom out  # Scale the frame by 1.5 (or any other factor > 1 to zoom out)
        neurons = []
        n_neurons_per_pack = 4*4*3 #3 articulations each with 4 tunable oscillators each containing 4 neurons
        packs = 1
        radius = 0.7
        pack_centers = {#should become useless
            'FR': np.array([0, 0, 0]),  
            'FL': np.array([4, 2, 0]),   
            'RR': np.array([-4, -2, 0]), 
            'RL': np.array([-4, 2, 0]),  
        }

        # Create neurons in packs and store them by pack
        neurons_by_pack = []
        center = np.array([0, 0, 0])
        pack_neurons = []
        previous_offset = np.array([
                0,
                0,
                0
            ])
        n_neurons_per_pack = len(data_json["type"])

        step_label = m.Text(f"Step: 0", font_size=24, color=m.WHITE).to_corner(m.UL)
        self.add(step_label)

        self.camera.frame_width = self.camera.frame_width * n_neurons_per_pack/31
        self.camera.frame_height = self.camera.frame_height * n_neurons_per_pack/31

        print(self.camera.frame_width,self.camera.frame_height )
        adjacency_matrix = np.zeros((n_neurons_per_pack, n_neurons_per_pack), dtype=int)
        for i in range(n_neurons_per_pack):
            pre_off_x = previous_offset[0]
            pre_off_y = previous_offset[1]
            # neurons are created inside the circle close to one another in a random way
            offset = np.array([
                random.uniform(min(-pre_off_x - 0.1,-radius), max(pre_off_x + 0.1,radius)),
                random.uniform(min(-pre_off_y - 0.1,-radius), max(pre_off_y + 0.1,radius)),
                0
            ])

            # neuron color
            #access to the list of neuron types stored in the json
            if data_json["type"][i] : 
                current_color = m.BLUE
            else : 
                current_color = m.RED

            #adds neuron to the scene
            neuron = Neuron(index = i,color = current_color)
            neuron.move_to(center + offset)
            previous_offset = offset
            pack_neurons.append(neuron)
            neurons.append(neuron)
            self.add(neuron)
            
            # Create adjacency matrix for current pack
            
        matrix = data_json["adjacency"]
        np_matrix = np.array(matrix)
        pretty_print(np_matrix)
        n= len(matrix)
        for i in range(n):
            for j in range(n):
                index = np_matrix[i, j]
                if index > 0: 
                    adjacency_matrix[i, j] = index
            
            neurons_by_pack.append(pack_neurons)
            adjacency_matrices.append(adjacency_matrix)


        def apply_forces(neurons_pack, adjacency_matrix):
            """
            Applies repulsion and spring forces within each pack of neurons.

            Parameters
            ----------
            neurons_pack : list of Neuron
                The list of neurons in the pack.
            adjacency_matrix : np.ndarray
                The adjacency matrix representing connections between neurons.
            """
                
            undirected_matrix = directed_to_undirected(adjacency_matrix)
            spring_constant = 1.1
            rest_length = 0.5
            for i in range(25):  # Number of iterations
                for idx, neuron in enumerate(neurons_pack):
                    force = np.array([0.0, 0.0, 0.0])
                    # Repulsion force (Coulomb's Law)
                    for other_idx, other in enumerate(neurons_pack):
                        if neuron != other:
                            diff = neuron.get_center() - other.get_center()
                            distance = np.linalg.norm(diff)
                            if distance < 0.01:
                                distance = 0.01  # Avoid division by zero
                            force +=  1.1*diff / (distance ** 2)
                    # Spring force (Hooke's Law)
                    for other_idx, connected in enumerate(undirected_matrix[idx]):
                        if connected == 1:
                            other = neurons_pack[other_idx]
                            diff = other.get_center() - neuron.get_center()
                            distance = np.linalg.norm(diff)
                            displacement = distance - rest_length
                            spring_force = spring_constant * displacement
                            force += (diff / distance) * spring_force  # Normalize and apply spring force
                    # Update position based on the net force
                    new_position = neuron.get_center() + force * 0.3  # Adjust the 0.01 factor for step size
                    neuron.move_to(new_position)
                # logging statement for each iteration
                print(f'Forces applied within pack {i}')
    
        # Fnction to avoid overlap by nudging neurons slightly apart
        def avoid_overlap(neurons_pack):
            """
            Avoids overlap by nudging neurons slightly apart.

            Parameters
            ----------
            neurons_pack : list of Neuron
                The list of neurons in the pack.
            """
            for _ in range(10):  # Number of iterations for overlap avoidance
                for i in range(len(neurons_pack)):
                    for j in range(len(neurons_pack)):
                        neuron_a = neurons_pack[i]
                        neuron_b = neurons_pack[j]
                        diff = neuron_a.get_center() - neuron_b.get_center()
                        distance = np.linalg.norm(diff)
                        min_distance = 0.5  # Minimum acceptable distance between neurons
                        if distance == 0 : 
                            distance = 0.1
                        if distance < min_distance:
                            # Move neurons apart slightly
                            correction = (diff / distance) * (min_distance - distance) / 2
                            neuron_a.move_to(neuron_a.get_center() + correction)
                            neuron_b.move_to(neuron_b.get_center() - correction)

        # Function to apply centripetal force towards pack center
        def apply_centripetal_force(neurons_pack, center):
            """
            Applies centripetal force towards the pack center.

            Parameters
            ----------
            neurons_pack : list of Neuron
                The list of neurons in the pack.
            center : np.ndarray
                The center towards which the centripetal force is applied.
            """
            for i in range(100):  # Number of iterations for centripetal force
                for idx, neuron in enumerate(neurons_pack):
                    force = np.array([0.0, 0.0, 0.0])
                    # Centripetal force towards pack center
                    center_diff = center - neuron.get_center()
                    force += center_diff * 1.3     # Adjust the 2 factor for centripetal strength

                    # Update position based on the net force
                    new_position = neuron.get_center() + force * 0.01  # Adjust the 0.01 factor for step size
                    neuron.move_to(new_position)

                # logging statement for each iteration
                print(f'Centripetal force applied to pack centered at {center}.')

        # Apply repulsion and spring forces for each pack
        apply_forces(pack_neurons, adjacency_matrix)
#   
        # Apply overlap avoidance for each pack
        avoid_overlap(pack_neurons)
#   
        # Apply centripetal forces for each pack
        apply_centripetal_force(pack_neurons, center)
        
        # Plot the edges based on the adjacency matrices
        edges = []
        for i in range(n_neurons_per_pack):
            for j in range( n_neurons_per_pack):
                if adjacency_matrix[i][j] == 1:
                    edge = m.Line(start=pack_neurons[i].get_center(), end=pack_neurons[j].get_center(), color=m.WHITE, stroke_width=0.5)
                    edges.append(edge)
                    self.add(edge)
        self.play(*[m.FadeIn(neuron) for neuron in neurons], *[m.Create(edge) for edge in edges])
        self.wait(1)

        # Function to calculate mean distances between neurons
        def calculate_mean_distances(pack_neurons, adjacency_matrix):
            """
            Calculates mean distances between connected and unconnected neurons.

            Parameters
            ----------
            pack_neurons : list of Neuron
                The list of neurons in the pack.
            adjacency_matrix : np.ndarray
                The adjacency matrix representing connections between neurons.

            Returns
            -------
            mean_connected : float
                The mean distance between connected neurons.
            mean_unconnected : float
                The mean distance between unconnected neurons.
            """
            connected_distances = []
            unconnected_distances = []
            for i in range(n_neurons_per_pack):
                for j in range( n_neurons_per_pack):
                    print(pack_neurons[i])
                    pos_i = pack_neurons[i].get_center()
                    pos_j = pack_neurons[j].get_center()
                    distance = np.linalg.norm(pos_i - pos_j)
                    if adjacency_matrix[i][j] == 1:
                        connected_distances.append(distance)
                    else:
                        unconnected_distances.append(distance)

            mean_connected = np.mean(connected_distances) if connected_distances else 0
            mean_unconnected = np.mean(unconnected_distances) if unconnected_distances else 0
            return mean_connected, mean_unconnected
        
        # Calculate and print mean distances
        mean_connected, mean_unconnected = calculate_mean_distances(pack_neurons, adjacency_matrix)
        print(f"Mean distance between connected neurons: {mean_connected}")
        print(f"Mean distance between unconnected neurons: {mean_unconnected}")

        def map_data_to_neuron(neuron_number, pack_neurons) : 
            """
            Maps data to the corresponding neuron in the visualization.

            Parameters
            ----------
            neuron_number : int
                The index of the neuron.
            pack_neurons : list of Neuron
                The list of neurons in the pack.

            Returns
            -------
            Neuron
                The neuron object corresponding to the provided data.
            """
            return pack_neurons[neuron_number]

        def activation(time_neuron_to_fire, pack_neurons):
            """
            Animates neuron activations over time.

            Parameters
            ----------
            time_neuron_to_fire : list of list of list
                A time-indexed structure containing neurons that fire at each step.
            pack_neurons : list of Neuron
                The list of neurons in the pack.
            """
            active_color = "yellow"  # Choose a distinct color
            active_color_output_neuron = "purple"
            active_scale_factor = 1.5  # Scale factor for active neurons

            active_color
            l = len(time_neuron_to_fire)
            
            for i in range(l):
                # if i/l *100 in [i *10 for i in range(10)]:
                    # print("loading... ", i/l * 100," % \n")
                
                if len(time_neuron_to_fire[i]) == 0 : 
                    None
                else : 
                    step_label.become(m.Text(f"Step: {i}", font_size=24, color=m.WHITE).to_corner(m.UL))
                    for el in time_neuron_to_fire[i]:

                        neuron_number = el[0]

                        # Map the neuron number to the neuron object
                        n_to_activate = map_data_to_neuron(neuron_number, pack_neurons)
                        new_radius = n_to_activate.original_radius * active_scale_factor
                        
                        n_to_activate.radius = new_radius
                        n_to_activate.circle.width = 2* new_radius
                        n_to_activate.circle.height = 2* new_radius


                        if neuron_number in data_json["output_neurons"]: # add some more conditions and color : bigger size when it fires etc
                            n_to_activate.radius = new_radius
                            n_to_activate.circle.width = 4* new_radius
                            n_to_activate.circle.height = 4* new_radius
                            n_to_activate.circle.set_color(active_color_output_neuron)
                        else : 
                            n_to_activate.circle.set_color(active_color)

                    #generates the animation
                    # self.wait(0.017)# for 60fps 1 frame is 0,016666667s
                    self.wait(0.07)# for 15fps ( lower quality ) frame is 0,066666667

                    for el in time_neuron_to_fire[i] : 
                        neuron_number = el[0]

                        # Map the neuron number to the neuron object
                        n_to_activate = map_data_to_neuron(neuron_number, pack_neurons)
                        new_radius = n_to_activate.original_radius * active_scale_factor
                        

                        n_to_activate.radius = n_to_activate.original_radius
                        n_to_activate.circle.width = 2 * n_to_activate.original_radius
                        n_to_activate.circle.height = 2 * n_to_activate.original_radius
                        n_to_activate.circle.set_color(n_to_activate.original_color)

            #creation of a data structure where each index is on step of simulation, containing a list of the neurons which fired at this step.
        time_neuron_to_fire = [[] for _ in range(len(data_json["activity"][0]))]
        print("len outside : ",len(time_neuron_to_fire))
        print("len outside : other ",len(time_neuron_to_fire[0]))     
                    
        for neuron_potentials_index in range(len(data_json["activity"])):
            neuron_potentials = data_json["activity"][neuron_potentials_index]
            for time_index in range(len(neuron_potentials)):
                p = data_json["activity"][neuron_potentials_index][time_index]                    
                # print(p)
                # time.sleep(0.00001)
                if p > ACT_POT - 0.05:
                        time_neuron_to_fire[time_index].append([neuron_potentials_index])

        # for el in time_neuron_to_fire : 
            # if len(el) != 0 :
                # print("non null element !")

        activation(time_neuron_to_fire, pack_neurons)
        print(data_json["output_neurons"])    


        




if __name__ == "__main__":
    scene = NeuralNetwork()
    scene.render()