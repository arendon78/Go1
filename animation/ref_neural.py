from manim import *
import random
import numpy as np


class Neuron(VMobject):
    def __init__(self, radius=0.12, color=BLUE, **kwargs):
        super().__init__(**kwargs)
        self.radius = radius
        self.color = color
        self.circle = Circle(radius=self.radius, color=self.color, fill_opacity=1)
        self.add(self.circle)
    
    def activate(self):
        self.circle.set_fill(YELLOW, opacity=1)
    
    def deactivate(self):
        self.circle.set_fill(self.color, opacity=1)


class NeuralNetwork(Scene):
    def construct(self):
        neurons = []
        n_neurons_per_pack = 10
        packs = 4
        radius = 0.7
        pack_centers = [
            np.array([-4, 2, 0]),  # Top-left
            np.array([4, 2, 0]),   # Top-right
            np.array([-4, -2, 0]), # Bottom-left
            np.array([4, -2, 0]),  # Bottom-right
        ]

        # Create neurons in packs and store them by pack
        neurons_by_pack = []
        adjacency_matrices = []  # List to store adjacency matrices for each pack
        for center in pack_centers:
            pack_neurons = []
            adjacency_matrix = np.zeros((n_neurons_per_pack, n_neurons_per_pack), dtype=int)
            
            for _ in range(n_neurons_per_pack):
                offset = np.array([
                    random.uniform(-radius, radius),
                    random.uniform(-radius, radius),
                    0
                ])
                neuron = Neuron()
                neuron.move_to(center + offset)
                pack_neurons.append(neuron)
                neurons.append(neuron)
                self.add(neuron)
            
            # Create adjacency matrix for current pack
            for i in range(n_neurons_per_pack):
                for j in range(i + 1, n_neurons_per_pack):
                    if random.random() < 0.005:  # 0.5% chance of connection
                        adjacency_matrix[i][j] = 1
                        adjacency_matrix[j][i] = 1
            
            neurons_by_pack.append(pack_neurons)
            adjacency_matrices.append(adjacency_matrix)
        
        # Function to apply repulsion and spring forces within each pack
        def apply_forces(neurons_pack, adjacency_matrix):
            spring_constant = 0.9
            rest_length = 0.2

            for i in range(100):  # Number of iterations
                for idx, neuron in enumerate(neurons_pack):
                    force = np.array([0.0, 0.0, 0.0])
                    
                    # Repulsion force (Coulomb's Law)
                    for other_idx, other in enumerate(neurons_pack):
                        if neuron != other:
                            diff = neuron.get_center() - other.get_center()
                            distance = np.linalg.norm(diff)
                            if distance < 0.1:
                                distance = 0.1  # Avoid division by zero
                            force += diff / (distance ** 2)

                    # Spring force (Hooke's Law)
                    for other_idx, connected in enumerate(adjacency_matrix[idx]):
                        if connected == 1:
                            other = neurons_pack[other_idx]
                            diff = other.get_center() - neuron.get_center()
                            distance = np.linalg.norm(diff)
                            displacement = distance - rest_length
                            spring_force = spring_constant * displacement
                            force += (diff / distance) * spring_force  # Normalize and apply spring force

                    # Update position based on the net force
                    new_position = neuron.get_center() + force * 0.01  # Adjust the 0.01 factor for step size
                    neuron.move_to(new_position)
                
                # Example logging statement for each iteration
                print(f'Forces applied within pack {i}')

        # Function to avoid overlap by nudging neurons slightly apart
        def avoid_overlap(neurons_pack):
            for _ in range(10):  # Number of iterations for overlap avoidance
                for i in range(len(neurons_pack)):
                    for j in range(i + 1, len(neurons_pack)):
                        neuron_a = neurons_pack[i]
                        neuron_b = neurons_pack[j]
                        diff = neuron_a.get_center() - neuron_b.get_center()
                        distance = np.linalg.norm(diff)
                        min_distance = 0.2  # Minimum acceptable distance between neurons
                        if distance < min_distance:
                            # Move neurons apart slightly
                            correction = (diff / distance) * (min_distance - distance) / 2
                            neuron_a.move_to(neuron_a.get_center() + correction)
                            neuron_b.move_to(neuron_b.get_center() - correction)

        # Function to apply centripetal force towards pack center
        def apply_centripetal_force(neurons_pack, center):
            for i in range(75):  # Number of iterations for centripetal force
                for idx, neuron in enumerate(neurons_pack):
                    force = np.array([0.0, 0.0, 0.0])
                    # Centripetal force towards pack center
                    center_diff = center - neuron.get_center()
                    force += center_diff * 1.8      # Adjust the 2 factor for centripetal strength
                    
                    # Update position based on the net force
                    new_position = neuron.get_center() + force * 0.02  # Adjust the 0.01 factor for step size
                    neuron.move_to(new_position)
                    avoid_overlap(neurons_pack)# ! costly !! 
                
                # Example logging statement for each iteration
                print(f'Centripetal force applied to pack centered at {center}.')

        # Apply repulsion and spring forces for each pack
        for pack_neurons, adjacency_matrix in zip(neurons_by_pack, adjacency_matrices):
            apply_forces(pack_neurons, adjacency_matrix)

        # Apply overlap avoidance for each pack
        for pack_neurons in neurons_by_pack:
            avoid_overlap(pack_neurons)

        # Apply centripetal forces for each pack
        for pack_neurons, center in zip(neurons_by_pack, pack_centers):
            apply_centripetal_force(pack_neurons, center)

        # Plot the edges based on the adjacency matrices
        edges = []
        for pack_neurons, adjacency_matrix in zip(neurons_by_pack, adjacency_matrices):
            for i in range(n_neurons_per_pack):
                for j in range(i + 1, n_neurons_per_pack):
                    if adjacency_matrix[i][j] == 1:
                        edge = Line(start=pack_neurons[i].get_center(), end=pack_neurons[j].get_center(), color=WHITE, stroke_width=0.5)
                        edges.append(edge)
                        self.add(edge)

        self.play(*[FadeIn(neuron) for neuron in neurons], *[Create(edge) for edge in edges])
        self.wait(1)

        # Function to calculate mean distances between neurons
        def calculate_mean_distances(neurons_by_pack, adjacency_matrices):
            connected_distances = []
            unconnected_distances = []
            for pack_neurons, adjacency_matrix in zip(neurons_by_pack, adjacency_matrices):
                for i in range(n_neurons_per_pack):
                    for j in range(i + 1, n_neurons_per_pack):
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
        mean_connected, mean_unconnected = calculate_mean_distances(neurons_by_pack, adjacency_matrices)
        print(f"Mean distance between connected neurons: {mean_connected}")
        print(f"Mean distance between unconnected neurons: {mean_unconnected}")

        def random_activation(neurons):
            random_neuron = random.choice(neurons)
            self.play(random_neuron.circle.animate.set_fill(YELLOW, opacity=1), run_time=0.5)
            self.play(random_neuron.circle.animate.set_fill(random_neuron.color, opacity=1), run_time=0.5)
        
        # Animate random neurons firing
        for _ in range(20):  # 20 random activations
            random_activation(neurons)
            self.wait(0.2)


if __name__ == "__main__":
    scene = NeuralNetwork()
    scene.render()
