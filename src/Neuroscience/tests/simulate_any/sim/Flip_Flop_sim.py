import os 
import sys
import numpy as np

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../'))
sys.path.append(project_root)

from Neuroscience.structures.Flip_FLop_T import Flip_Flop_T# import the structure that you want to simulate


def instance_and_input(sim_time):
    res = 0.1
    instance = Flip_Flop_T(res)
    inputs = np.zeros([sim_time, 2])


    inputs[0] = [0,1]
    inputs[1] = [0,1]
    inputs[850] = [1,0]
    inputs[960] = [1,0]

    return instance,inputs