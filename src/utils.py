import math
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx
import numpy as np

def jointLinearInterpolation(initPos, targetPos, rate):

    rate = np.fmin(np.fmax(rate, 0.0), 1.0)
    p = initPos*(1-rate) + targetPos*rate
    return p

def theta_hip(x,y,z):
    x= 0
    """
    Calculate the hip angle θ_hip.
    
    Parameters:
    z (float): The z-coordinate.
    y (float): The y-coordinate.
    
    Returns:
    float: The hip angle θ_hip in radians.
    """
    # print("z,y : ", z,y)
    print("returned value : ",(math.atan2(z,y)) %(math.pi))
    # true formula : (math.pi/2 + math.atan2(-y, z)) %(math.pi) equivalent to :
    return (math.atan2(z,y)) %(math.pi)
    # return math.atan2(y, z)

def theta_thigh(x, y, z, L=0.213):
    """
    Calculate the thigh angle θ_thigh.
    
    Parameters:
    x (float): The x-coordinate.
    y (float): The y-coordinate.
    z (float): The z-coordinate.
    L (float): The length parameter, default is 0.213.
    
    Returns:
    float: The thigh angle θ_thigh in radians.
    """
    distance = math.sqrt(x**2 + y**2 + z**2)
    cos_term = distance / (2 * L)
    # Ensure cos_term is within the valid range for acos
    cos_term = min(1.0, max(-1.0, cos_term))
    term1 = math.acos(cos_term)
    term2 = math.atan2(-x, math.sqrt(y**2 + z**2))
    return term1 + term2

def theta_calf(x, y, z, L=0.213):
    """
    Calculate the calf angle θ_calf.
    
    Parameters:
    x (float): The x-coordinate.
    y (float): The y-coordinate.
    z (float): The z-coordinate.
    L (float): The length parameter, default is 0.213.
    
    Returns:
    float: The calf angle θ_calf in radians.
    """
    thigh_angle = theta_thigh(x, y, z, L)
    sin_term = (-x / L) - math.sin(thigh_angle)
    # Ensure sin_term is within the valid range for asin
    sin_term = min(1.0, max(-1.0, sin_term))
    term1 = math.asin(sin_term)
    return term1 - thigh_angle


def plot_trajectory(control_points, bezier_points, stance_points):
    """
    Plots the swing and stance phases of the foot trajectory.

    Parameters:
    control_points (list of tuples): Control points for the Bézier curve.
    bezier_points (list of tuples): Points on the Bézier curve (swing phase).
    stance_points (list of tuples): Points on the stance phase trajectory.
    """
    control_points = np.array(control_points)
    bezier_curve = np.array(bezier_points)
    stance_curve = np.array(stance_points)

    plt.plot(control_points[:, 0], control_points[:, 1], 'ro--', label='Control Points')
    plt.plot(bezier_curve[:, 0], bezier_curve[:, 1], 'b-', label='Swing Phase')
    plt.plot(stance_curve[:, 0], stance_curve[:, 1], 'r-', label='Stance Phase')
    plt.legend()
    plt.xlabel('X coordinate WRT hip (m)')
    plt.ylabel('Y coordinate WRT hip (m)')
    plt.title('Sample Foot Trajectory Generation')
    plt.show()


def unphase(deg, list):
    assert deg>=0 and deg <= 360
    index =int(deg/360*len(list))
    toreturn = list[index:]+list[:index]
    return toreturn


def plot_trajectory_2(full_trajectory):
    """
    Plots the full trajectory along with its control points.

    Parameters:
    full_trajectory (list of tuples): Points on the full trajectory.
    """
    full_trajectory = np.array(full_trajectory)
    plt.plot(full_trajectory[:, 0], full_trajectory[:, 1], 'b-', label='Full Trajectory')
    plt.legend()
    plt.xlabel('X coordinate WRT hip (m)')
    plt.ylabel('Y coordinate WRT hip (m)')
    plt.title('Full Foot Trajectory Generation')
    plt.show()

def plot_trajectory_3(bezier_points, stance_points):
    bezier_curve = np.array(bezier_points)
    stance_curve = np.array(stance_points)

    plt.scatter(bezier_curve[:, 0], bezier_curve[:, 1], c=np.linspace(0, 1, len(bezier_curve)), cmap='viridis', label='Swing Phase', s=10)
    plt.scatter(stance_curve[:, 0], stance_curve[:, 1], c=np.linspace(0, 1, len(stance_curve)), cmap='plasma', label='Stance Phase', s=10)
    plt.legend(['Start', 'End'])
    plt.xlabel('X coordinate WRT hip (m)')
    plt.ylabel('Y coordinate WRT hip (m)')
    plt.title('Forward Gait Foot Trajectory')
    plt.show()

def plot_trajectory_single(points, indices_to_consider, x_description, y_descritpion):
    trajectory = np.array(points)
    

    plt.scatter(trajectory[:, indices_to_consider[0]], trajectory[:, indices_to_consider[1]], c='blue', s=10)
    plt.xlabel(x_description)
    plt.ylabel(y_descritpion)

    plt.title('Gait Foot Trajectory')
    plt.show()

def plot_joint_angles(full_trajectory):
    full_trajectory = np.array(full_trajectory)
    num_points = len(full_trajectory)
    
    hip_angles = np.zeros(num_points)
    thigh_angles = np.zeros(num_points)
    calf_angles = np.zeros(num_points)
    
    for i in range(num_points):
        x, y = full_trajectory[i]
        hip_angles[i] = theta_hip(0, y)
        thigh_angles[i] = theta_thigh(x, y, 0)
        calf_angles[i] = theta_calf(x, y, 0)
    
    t = np.arange(num_points)
    
    plt.figure(figsize=(10, 5))
    
    plt.subplot(1, 2, 1)
    plt.scatter(t, thigh_angles, c=np.linspace(0, 1, num_points), cmap='viridis', label='Thigh Joint Solution', s=10)
    plt.xlabel('Timesteps')
    plt.ylabel('Angle (radians)')
    plt.title('Thigh Joint Solution')
    plt.legend()
    
    plt.subplot(1, 2, 2)
    plt.scatter(t, calf_angles, c=np.linspace(0, 1, num_points), cmap='plasma', label='Calf Joint Solution', s=10)
    plt.xlabel('Timesteps')
    plt.ylabel('Angle (radians)')
    plt.title('Calf Joint Solution')
    plt.legend()
    
    plt.tight_layout()
    plt.show()


#part on adjacency matrix ----------------

import numpy as np

class AdjacencyMatrix:
    def __init__(self, size=0):
        self.matrix = np.zeros((size, size), dtype=int)
        self.size = size

    def instanciate_matrix(adjacency_matrix):
        mat = AdjacencyMatrix.__init__(np.size(adjacency_matrix))
        mat.matrix = adjacency_matrix

    def add_vertex(self):
        size = self.matrix.shape[0]
        new_matrix = np.zeros((size + 1, size + 1), dtype=int)
        new_matrix[:size, :size] = self.matrix
        self.matrix = new_matrix

    def remove_vertex(self, vertex):
        if vertex >= self.matrix.shape[0]:
            raise ValueError("Vertex index out of range")
        self.matrix = np.delete(self.matrix, vertex, axis=0)
        self.matrix = np.delete(self.matrix, vertex, axis=1)

    def add_edge(self, v1, v2):
        if v1 >= self.matrix.shape[0] or v2 >= self.matrix.shape[0]:
            raise ValueError("Vertex index out of range")
        self.matrix[v1, v2] = 1
        # self.matrix[v2, v1] = 1  # For undirected graph

    def remove_edge(self, v1, v2):
        if v1 >= self.matrix.shape[0] or v2 >= self.matrix.shape[0]:
            raise ValueError("Vertex index out of range")
        self.matrix[v1, v2] = 0
        self.matrix[v2, v1] = 0  # For undirected graph

    def save(self, filename):
        np.save(filename, self.matrix)

    def load(self, filename):
        self.matrix = np.load(filename)
        
    def count_nonzeros(self):
        return np.count_nonzero(self.matrix)

    def pretty_print(self):
        plt.figure(figsize=(8, 8))
        sns.heatmap(self.matrix, annot=True, fmt='d', cbar=False, cmap='viridis', linewidths=0.5, linecolor='black')
        plt.title('Adjacency Matrix')
        plt.xlabel('Vertex')
        plt.ylabel('Vertex')
        plt.show()

    def draw_graph(self, name="Directed Graph"):
        G = nx.DiGraph()

        # Add nodes
        num_vertices = self.matrix.shape[0]
        G.add_nodes_from(range(num_vertices))

        # Add edges
        for i in range(num_vertices):
            for j in range(num_vertices):
                if self.matrix[i, j] == 1:
                    G.add_edge(i, j)

        pos = nx.spring_layout(G)  # positions for all nodes

        # Draw the nodes and edges
        nx.draw(G, pos, with_labels=True, node_size=700, node_color='skyblue', arrows=True)
        plt.title(name)
        plt.show()


    def plot_force_directed_graph(self, node_types, graph_name="Graph"):
        """
        Affiche un graphe force-directed à partir de la matrice d'adjacence de l'instance.

        Paramètres :
        node_types (list of str): Liste des types de nœuds ('Excitatory' ou 'Inhibitory').
        graph_name (str) : Le nom du graphe pour le titre de la visualisation.
        """
        # Créer le graphe dirigé à partir de la matrice d'adjacence
        #TO SHOW UNDIRECTED,, UNCOMMENT HERE
        G = nx.from_numpy_array(self.matrix)#,create_using=nx.DiGraph)

        # Calculer la disposition des nœuds (force-directed)
        pos = nx.spring_layout(G)

        # Définir les couleurs des nœuds en fonction de leur type
        node_colors = ['skyblue' if node_type == 'Excitatory' else 'red' for node_type in node_types]

        # Dessiner le graphe dirigé avec des flèches pour montrer la direction
        plt.figure(figsize=(10, 10))
        #TO SHOW UNDIRECTED, UNCOMMENT HERE
        nx.draw(G, pos, with_labels=True, node_size=500, node_color=node_colors,
                font_size=10, font_color="black", edge_color="gray", width=2,
                arrows=False)#True, arrowstyle='-|>', arrowsize=10)

        # Ajouter le titre
        plt.suptitle(graph_name,fontsize = 15)
        plt.tight_layout()

        # Afficher le graphe
        plt.show()


