#!/usr/bin/python
import os 
import sys
import numpy as np
from scipy.special import comb

from utils import * 

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))
sys.path.append(project_root)


def bezier(points, num_points=50):
    """
    Generates a Bézier curve from a list of control points.

    Parameters:
    points (list of tuples): List of control points (x, y).
    num_points (int): Number of points to generate along the curve.

    Returns:
    list of tuples: Points on the Bézier curve.
    """

    n = len(points) - 1
    t_values = np.linspace(0, 1, num_points)
    curve_points = []

    for t in t_values:
        x = sum(comb(n, i) * (1 - t)**(n - i) * t**i * points[i][0] for i in range(n + 1))
        y = sum(comb(n, i) * (1 - t)**(n - i) * t**i * points[i][1] for i in range(n + 1))
        curve_points.append((x, y))

    return curve_points

def stance_phase(start_point, end_point, num_points=50, delta = 0.007):
    """
    Generates a stance-phase trajectory using a sinusoidal function.

    Parameters:
    start_point (tuple): The starting point of the stance phase.
    end_point (tuple): The ending point of the stance phase.
    num_points (int): Number of points to generate along the stance trajectory.
    amplitude (float): Amplitude of the sinusoidal function.

    Returns:
    list of tuples: Points on the stance-phase trajectory.
    """

    x_start, y_start = start_point
    x_end, y_end = end_point
    x_values = np.linspace(x_start, x_end, num_points)
    y_values = y_start - delta * np.sin(np.pi * np.linspace(0, 1, num_points))

    return list(zip(x_values, y_values))

def generate_control_points(standx, Lspan, deltaL, delta, standy, Yspan, deltaY):
    """
    Generates control points for the Bézier curve based on given parameters.

    Parameters:
    standx (float): Stand x-coordinate.
    Lspan (float): Span in the x-direction.
    deltaL (float): Change in the x-direction for some points.
    delta (float): Small delta for some y-coordinates.
    standy (float): Stand y-coordinate.
    Yspan (float): Span in the y-direction.
    deltaY (float): Change in the y-direction for some points.

    Returns:
    list of tuples: Control points.
    """
    points = [
        (standx - Lspan, standy),  # 0
        (standx - Lspan - deltaL, standy),  # 1
        (standx - Lspan - deltaL - delta, standy + Yspan),  # 2
        (standx - Lspan - deltaL - delta, standy + Yspan),  # 3
        (standx - Lspan - deltaL - delta, standy + Yspan),  # 4
        (standx, standy + Yspan),  # 5
        (standx, standy + Yspan),  # 6
        (standx, standy + Yspan + deltaY),  # 7
        (standx + Lspan + deltaL + delta, standy + Yspan + deltaY),  # 8
        (standx + Lspan + deltaL + delta, standy + Yspan + deltaY),  # 9
        (standx + Lspan + deltaL, standy),  # 10
        (standx + Lspan, standy)  # 11
    ]
    return points

def generate_trajectory(standx, Lspan, deltaL, delta, standy, Yspan, deltaY, num_points_bezier = 50, num_points_stance = 50):
    points = generate_control_points(standx, Lspan, deltaL, delta, standy, Yspan, deltaY)
    bezier_curve_points = bezier(points,num_points=num_points_bezier)
    stance_curve_points = stance_phase(bezier_curve_points[-1], bezier_curve_points[0],delta=delta,num_points=num_points_stance)

    return bezier_curve_points + stance_curve_points





def foot_trajectory(NUM_POINTS_BEZIER = 50 ,NUM_POINTS_STANCE = 50):
    # generation of the points of the curve ------------
    
    standx = -0.045
    Lspan= 0.025
    deltaL = 0.02
    delta= 0.02
    standy= -0.35
    Yspan= 0.04
    deltaY= 0.01




    trajectory = generate_trajectory(standx, Lspan, deltaL, delta, standy, Yspan, deltaY,num_points_bezier=NUM_POINTS_BEZIER, num_points_stance= NUM_POINTS_STANCE)
    
    # control_points = [(-0.07, -0.34), 
    #                   (-0.09, -0.34), 
    #                   (-0.1, -0.3), (-0.1, -0.3),(-0.1, -0.3),
    #                   (-0.045, -0.3),(-0.045, -0.3),
    #                   (-0.045,-0.29),
    #                   (0,-0.29),(0,-0.29),
    #                   (-0.01,-0.34),
    #                   (-0.03,-0.34)]

    control_points = generate_control_points(standx, Lspan, deltaL, delta, standy, Yspan, deltaY)

    bezier_curve_points = bezier(control_points)
    stance_curve_points = stance_phase(bezier_curve_points[-1], bezier_curve_points[0])

    plot_trajectory(control_points, bezier_curve_points, stance_curve_points)     
    plot_trajectory_2(trajectory)   
    plot_trajectory_3(bezier_curve_points,stance_curve_points)
    plot_trajectory_single(trajectory,(0,1), "X coordinates WRT hip (m)", "Y coordinates WRT hip (m)")


    # a little bit dumb but stays as it is for the moment
    return trajectory
