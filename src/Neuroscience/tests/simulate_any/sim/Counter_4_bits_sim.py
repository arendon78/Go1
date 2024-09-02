import numpy as np
import sys
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../'))
sys.path.append(project_root)

from Neuroscience.structures.Counter_4_bits import Counter_4_bits# import the structure that you want to simulate


def instance_and_input(sim_time):
    res = 0.1
    instance = Counter_4_bits(res)

    inputs = np.zeros([sim_time, 2])
    inputs[0] = [0,1]
    for i in range(sim_time): 
        if i % 1000 == 700 or i % 1000 == 810: 
            inputs[i] = [1, 0]

    return instance,inputs
