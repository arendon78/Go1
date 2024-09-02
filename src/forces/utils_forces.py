import numpy as np
import json
import matplotlib.pyplot as plt
import random
import math

def calculate_derivative(p1, p2):
    """
    Calculates the derivative (slope) between two points.

    :param p1: The first point (x1, y1).
    :type p1: tuple of float
    :param p2: The second point (x2, y2).
    :type p2: tuple of float
    :returns: The slope between the two points.
    :rtype: float
    """
    return (p2[1] - p1[1]) / (p2[0] - p1[0])

def gradient_ascent(list_point_derivative):
    """
    Performs gradient ascent to find a local maximum in the list of points.

    :param list_point_derivative: A list of points with their derivatives.
    :type list_point_derivative: list of tuples
    :returns: The point corresponding to the local maximum found.
    :rtype: tuple
    """
    HORIZON = min(max(int(len(list_point_derivative)/10), 2), 10)
    p = random.randrange(HORIZON//2, len(list_point_derivative) - HORIZON//2)
    for _ in range(int(0.25 * len(list_point_derivative))):
        current_point = list_point_derivative[p]
        found_higher_point = False
        j = 1
        while j < HORIZON // 2 and not found_higher_point:
            if (p + j) > len(list_point_derivative) - 1 or (p - j) < 0:
                break
            left_point = list_point_derivative[p - j]
            right_point = list_point_derivative[p + j]
            if right_point[1] > current_point[1]:
                p += j
                found_higher_point = True
                break
            elif left_point[1] >= current_point[1]:
                p -= j
                found_higher_point = True
                break
            j += 1                
    return list_point_derivative[p]

def gradient_descent(list_point_derivative):
    """
    Performs gradient descent to find a local minimum in the list of points.

    :param list_point_derivative: A list of points with their derivatives.
    :type list_point_derivative: list of tuples
    :returns: The point corresponding to the local minimum found.
    :rtype: tuple
    """
    HORIZON = min(max(int(len(list_point_derivative) / 10), 2), 10)
    p = random.randrange(HORIZON // 2, len(list_point_derivative) - HORIZON // 2)
    for _ in range(int(0.25 * len(list_point_derivative))):
        current_point = list_point_derivative[p]
        found_higher_point = False
        j = 1
        while j < HORIZON // 2 and not found_higher_point:
            if p + j > len(list_point_derivative) - 1 or p - j < 0:
                break
            left_point = list_point_derivative[p - j]
            right_point = list_point_derivative[p + j]
            if right_point[1] < current_point[1]:
                p += j
                found_higher_point = True
            elif left_point[1] <= current_point[1]:
                p -= j
                found_higher_point = True
            j += 1                
    return list_point_derivative[p]

def calculate_mean_rooted_derivative(p1, p2, l):
    """
    Calculates the mean rooted derivative between two points within a list.

    :param p1: The first point (x1, y1).
    :type p1: tuple of float
    :param p2: The second point (x2, y2).
    :type p2: tuple of float
    :param l: The list of points to search within.
    :type l: list of tuples
    :returns: The mean rooted derivative between p1 and p2.
    :rtype: float
    """
    i1, i2 = -1, -1
    for i in range(len(l)): 
        if l[i] == p1: 
            i1 = i
        if l[i] == p2: 
            i2 = i
    if i1 < 0 and i2 < 0:
        print("One of the points was not found in the list!")
    if i1 > i2:
        p1, p2 = p2, p1
        i1, i2 = i2, i1
    d_abs_sum = 0
    for p in range(i1, i2 + 1):
        d_abs_sum += math.sqrt(abs(l[p][2]))
    d_abs_mean = d_abs_sum / (i2 - i1)
    return d_abs_mean

def find_value(time, list):
    """
    Finds the value at a specific time within a list of points.

    :param time: The time to search for.
    :type time: float
    :param list: The list of points to search within.
    :type list: list of tuples
    :returns: The point corresponding to the given time, or None if not found.
    :rtype: tuple or None
    """
    for i in range(len(list)):
        if list[i][0] == time:
            return list[i]
    print("Not found")
    return None

def monte_carlo_gradient(direction, l):
    """
    Performs Monte Carlo gradient ascent or descent to find local extrema.

    :param direction: The direction to search in; negative for descent, positive for ascent.
    :type direction: int
    :param l: The list of points to search within.
    :type l: list of tuples
    :returns: A list of local maxima or minima found.
    :rtype: list of tuples
    """
    n_rep = int(len(l) // 10 * 1.5)
    if direction < 0: 
        local_mins = []
        for i in range(n_rep): 
            local_min_found = gradient_descent(l)
            local_mins.append(local_min_found)
        local_mins = list(set(tuple(sub_list) for sub_list in local_mins))
        return local_mins
    else: 
        local_maxes = []
        for i in range(n_rep): 
            local_max_found = gradient_ascent(l)
            local_maxes.append(local_max_found)
        local_maxes = list(set(tuple(sub_list) for sub_list in local_maxes))
        return local_maxes

def find_patterns(merged_mins_maxes_coordinates, coordinates, p0_spike, p2_spike, MRD_value):
    """
    Finds specific patterns in the list of merged minima and maxima coordinates.

    :param merged_mins_maxes_coordinates: The list of merged minima and maxima coordinates.
    :type merged_mins_maxes_coordinates: list of tuples
    :param coordinates: The list of original coordinates.
    :type coordinates: list of tuples
    :param p0_spike: The threshold for the first peak.
    :type p0_spike: float
    :param p2_spike: The threshold for the second peak.
    :type p2_spike: float
    :param MRD_value: The minimum mean rooted derivative value to qualify as a pattern.
    :type MRD_value: float
    """
    pattern_to_fit = ["max", "min", "max"]
    p = 0
    for i in range(len(merged_mins_maxes_coordinates) - 2): 
        p0 = merged_mins_maxes_coordinates[i]
        p1 = merged_mins_maxes_coordinates[i + 1]
        p2 = merged_mins_maxes_coordinates[i + 2]
        pattern = [p0[3], p1[3], p2[3]]
        if pattern == pattern_to_fit:
            deltat1 = abs(p1[0] - p0[0])
            deltat2 = abs(p2[0] - p1[0])
            amplitude1 = abs(p1[1] - p0[1])
            amplitude2 = abs(p2[1] - p1[1])
            if p0[1] > p0_spike and p2[1] > p2_spike:
                if calculate_mean_rooted_derivative(p0[:-1], p2[:-1], coordinates) > MRD_value:
                    p += 1
                    print("Pattern found! The robot was walking: ", p0, p1, p2, abs(amplitude1 - amplitude2) / (amplitude1 + amplitude2), deltat1, deltat2,
                          "\nMean absolute derivative: ", calculate_mean_rooted_derivative(p0[:-1], p2[:-1], coordinates), "\n")
    print(p)

def find_a_pattern(merged_mins_maxes_coordinates, coordinates, p0_spike, p2_spike, MRD_value):
    """
    Finds a specific pattern in the list of merged minima and maxima coordinates.

    :param merged_mins_maxes_coordinates: The list of merged minima and maxima coordinates.
    :type merged_mins_maxes_coordinates: list of tuples
    :param coordinates: The list of original coordinates.
    :type coordinates: list of tuples
    :param p0_spike: The threshold for the first peak.
    :type p0_spike: float
    :param p2_spike: The threshold for the second peak.
    :type p2_spike: float
    :param MRD_value: The minimum mean rooted derivative value to qualify as a pattern.
    :type MRD_value: float
    :returns: A tuple indicating whether a pattern was found, and the points involved in the pattern.
    :rtype: tuple (bool, tuple, tuple, tuple)
    """
    PRECISION = 0.5 
    pattern_to_fit = ["max", "min", "max"]
    for i in range(len(merged_mins_maxes_coordinates) - 2): 
        p0 = merged_mins_maxes_coordinates[i]
        p1 = merged_mins_maxes_coordinates[i + 1]
        p2 = merged_mins_maxes_coordinates[i + 2]
        pattern = [p0[3], p1[3], p2[3]]
        if pattern == pattern_to_fit:
            deltat1 = abs(p1[0] - p0[0])
            deltat2 = abs(p2[0] - p1[0])
            amplitude1 = abs(p1[1] - p0[1])
            amplitude2 = abs(p2[1] - p1[1])
            if abs(deltat1 - 25) < 25 * PRECISION and abs(deltat2 - 25) < 25 * PRECISION:
                if p0[1] > p0_spike and p2[1] > p2_spike:
                    if calculate_mean_rooted_derivative(p0[:-1], p2[:-1], coordinates) > MRD_value:
                        print("Pattern found! The robot was walking: ", p0, p1, p2, abs(amplitude1 - amplitude2) / (amplitude1 + amplitude2), deltat1, deltat2,
                              "\nMean absolute derivative: ", calculate_mean_rooted_derivative(p0[:-1], p2[:-1], coordinates), "\n")
                        return True, p0, p1, p2
    return False, None, None, None

def build_merge(local_maxes, local_mins):
    """
    Builds an ordered list of maxima and minima along the time axis.

    :param local_maxes: The list of local maxima.
    :type local_maxes: list of tuples
    :param local_mins: The list of local minima.
    :type local_mins: list of tuples
    :returns: A merged list of minima and maxima ordered by time.
    :rtype: list of tuples
    """
    merged_mins_maxes_coordinates = []
    local_maxes_copy = local_maxes
    local_mins_copy = local_mins
    nmax = len(local_maxes)
    nmin = len(local_mins)
    for _ in range(nmax + nmin):
        if local_maxes_copy:
            index_max_in_list = 0
            time_maxes_index = local_maxes_copy[index_max_in_list][0]
            for j in range(len(local_maxes_copy)): 
                if local_maxes_copy[j][0] < time_maxes_index:
                    time_maxes_index = local_maxes_copy[j][0]
                    index_max_in_list = j
        else: 
            time_maxes_index = float('inf')
        if local_mins_copy:
            index_min_in_list = 0
            time_mins_index = local_mins_copy[index_min_in_list][0]
            for p in range(len(local_mins_copy)):
                if local_mins_copy[p][0] < time_mins_index:
                    time_mins_index = local_mins_copy[p][0]
                    index_min_in_list = p
        else: 
            time_mins_index = float('inf')
        if time_maxes_index < time_mins_index: 
            el = local_maxes_copy.pop(index_max_in_list)
            merged_mins_maxes_coordinates.append([el[0], el[1], el[2], "max"])
        else: 
            el = local_mins_copy.pop(index_min_in_list)
            merged_mins_maxes_coordinates.append([el[0], el[1], el[2], "min"])
    return merged_mins_maxes_coordinates
