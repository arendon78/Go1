from Neuroscience.structures.Counter_1_bit import Counter_1_bit# import the structure that you want to simulate
import numpy as np

def instance_and_input(sim_time):
    res = 0.1
    instance = Counter_1_bit(res)

    inputs = np.zeros([sim_time, 2])
    inputs[0] = [0,1]
    for i in range(sim_time): 
        if i % 1000 == 700 or i % 1000 == 810: 
            inputs[i] = [1, 0]

    return instance,inputs
