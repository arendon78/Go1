import time
import os 
import sys
import statistics
import json
import numpy as np

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))
sys.path.append(project_root)

from Neuroscience.structures.Excitatory_Neuron import  Excitatory_Neuron
from Neuroscience.structures.Inhibitory_Neuron import Inhibitory_Neuron

from Neuroscience.structures.Flip_FLop_T import Flip_Flop_T# import the structure that you want to simulate


res = 0.1                       # Set the resolution
sim_time = 10000                # Set the simulation time


to_simulate = Flip_Flop_T(res)
name = "Flip_Flop_T" #name of the file
json_path = "../../../animation/datas/" + name + ".json" # path of the location to save

to_simulate.update_adjacency_matrix()
n_neurons = len(to_simulate.brain)

data = {
    "activity" : np.zeros((n_neurons,sim_time)),#ïf it doesn't work, intervertir les deux
    # we will convert these datas into json-compatible data at the end of the simulation
    "adjacency" : to_simulate.adjacency.matrix.tolist(),# assuming the structure of the network won't change along the simulation.
    "type" : [isinstance(neuron,Excitatory_Neuron) for neuron in to_simulate.brain]
}



inputs = np.zeros([sim_time, 2])

#----- change as you like
inputs[0] = [0,1]
def fill_inputs(inputs):
    inputs[1] = [0,1]

    inputs[850] = [1,0]
    inputs[960] = [1,0]

#------

fill_inputs(inputs)#define your own version of the function

k=0

while k < sim_time:
    to_simulate.pass_inputs(inputs, k)
    to_simulate.simulate(k, data["activity"])
    k+=1

#convert back to a json compatible format : 

data["activity"] = data["activity"].tolist()

with open(json_path,"w") as json_file: 
    json.dump(data ,json_file)






