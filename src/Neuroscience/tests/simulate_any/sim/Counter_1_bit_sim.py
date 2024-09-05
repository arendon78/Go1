import os 
import sys
import numpy as np

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../'))
sys.path.append(project_root)

from Neuroscience.structures.Counter_1_bit import Counter_1_bit# import the structure that you want to simulate


def instance_and_input(sim_time):
    res = 0.1
    instance = Counter_1_bit(res)

    inputs = np.zeros([sim_time, 2])
    inputs[0] = [0,1]
    for i in range(sim_time): 
        if i % 1000 == 700 or i % 1000 == 810: 
            inputs[i] = [1, 0]

    return instance,inputs
