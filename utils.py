import math
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx

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


import numpy as np
import matplotlib.pyplot as plt
from scipy.special import comb

# def bezier(points, num_points=50):
#     """
#     Generates a Bézier curve from a list of control points.

#     Parameters:
#     points (list of tuples): List of control points (x, y).
#     num_points (int): Number of points to generate along the curve.

#     Returns:
#     list of tuples: Points on the Bézier curve.
#     """

#     n = len(points) - 1
#     t_values = np.linspace(0, 1, num_points)
#     curve_points = []

#     for t in t_values:
#         x = sum(comb(n, i) * (1 - t)**(n - i) * t**i * points[i][0] for i in range(n + 1))
#         y = sum(comb(n, i) * (1 - t)**(n - i) * t**i * points[i][1] for i in range(n + 1))
#         curve_points.append((x, y))

#     return curve_points



# def stance_phase(start_point, end_point, num_points=50, delta = 0.007):
#     """
#     Generates a stance-phase trajectory using a sinusoidal function.

#     Parameters:
#     start_point (tuple): The starting point of the stance phase.
#     end_point (tuple): The ending point of the stance phase.
#     num_points (int): Number of points to generate along the stance trajectory.
#     amplitude (float): Amplitude of the sinusoidal function.

#     Returns:
#     list of tuples: Points on the stance-phase trajectory.
#     """

#     x_start, y_start = start_point
#     x_end, y_end = end_point
#     x_values = np.linspace(x_start, x_end, num_points)
#     y_values = y_start - delta * np.sin(np.pi * np.linspace(0, 1, num_points))

#     return list(zip(x_values, y_values))



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



# def generate_control_points(standx, Lspan, deltaL, delta, standy, Yspan, deltaY):
#     """
#     Generates control points for the Bézier curve based on given parameters.

#     Parameters:
#     standx (float): Stand x-coordinate.
#     Lspan (float): Span in the x-direction.
#     deltaL (float): Change in the x-direction for some points.
#     delta (float): Small delta for some y-coordinates.
#     standy (float): Stand y-coordinate.
#     Yspan (float): Span in the y-direction.
#     deltaY (float): Change in the y-direction for some points.

#     Returns:
#     list of tuples: Control points.
#     """
#     points = [
#         (standx - Lspan, standy),  # 0
#         (standx - Lspan - deltaL, standy),  # 1
#         (standx - Lspan - deltaL - delta, standy + Yspan),  # 2
#         (standx - Lspan - deltaL - delta, standy + Yspan),  # 3
#         (standx - Lspan - deltaL - delta, standy + Yspan),  # 4
#         (standx, standy + Yspan),  # 5
#         (standx, standy + Yspan),  # 6
#         (standx, standy + Yspan + deltaY),  # 7
#         (standx + Lspan + deltaL + delta, standy + Yspan + deltaY),  # 8
#         (standx + Lspan + deltaL + delta, standy + Yspan + deltaY),  # 9
#         (standx + Lspan + deltaL, standy),  # 10
#         (standx + Lspan, standy)  # 11
#     ]
#     return points

# def generate_trajectory(standx, Lspan, deltaL, delta, standy, Yspan, deltaY, num_points_bezier = 50, num_points_stance = 50):
#     points = generate_control_points(standx, Lspan, deltaL, delta, standy, Yspan, deltaY)
#     bezier_curve_points = bezier(points,num_points=num_points_bezier)
#     stance_curve_points = stance_phase(bezier_curve_points[-1], bezier_curve_points[0],delta=delta,num_points=num_points_stance)

#     return bezier_curve_points + stance_curve_points



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
    
    # plt.scatter(trajectory[:, 0], trajectory[:, 1], c='blue', s=10)  # Use a single color for all points
    # plt.xlabel('Theta thigh (radian)')
    # plt.ylabel('Theta calf (radian)')

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


#part on adjacency matrix : to delete ! -----------------------------

import numpy as np

class AdjacencyMatrix:
    def __init__(self, size=0):
        self.matrix = np.zeros((size, size), dtype=int)
        self.size = size

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
        G = nx.from_numpy_array(self.matrix)#,create_using=nx.DiGraph)

        # Calculer la disposition des nœuds (force-directed)
        pos = nx.spring_layout(G)

        # Définir les couleurs des nœuds en fonction de leur type
        node_colors = ['skyblue' if node_type == 'Excitatory' else 'red' for node_type in node_types]

        # Dessiner le graphe dirigé avec des flèches pour montrer la direction
        plt.figure(figsize=(10, 10))
        nx.draw(G, pos, with_labels=True, node_size=500, node_color=node_colors,
                font_size=10, font_color="black", edge_color="gray", width=2,
                arrows=False)#True, arrowstyle='-|>', arrowsize=10)

        # Ajouter le titre
        plt.suptitle(graph_name,fontsize = 15)
        plt.tight_layout()

        # Afficher le graphe
        plt.show()


