import time
import os 
import sys
import statistics
import json
import numpy as np



from sim.Counter_4_bits_sim import instance_and_input



project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))
sys.path.append(project_root)

from Neuroscience.structures.Excitatory_Neuron import  Excitatory_Neuron
from Neuroscience.structures.Inhibitory_Neuron import Inhibitory_Neuron



#this module allows you to simulate any neural network, And save the neural activity of all the neurons into a file.
# all you have to do is export the right instance_and_input(sim_time) function that returns the instance you want to simulate and the inputs you give it.

res = 0.1                       # Set the resolution
sim_time = 80000          # Set the simulation time

instance,inputs = instance_and_input(sim_time)
name = instance.name

print(instance)

json_path = "../../../animation/datas/" + name + ".json" # path of the location saved


instance.update_adjacency_matrix()
n_neurons = len(instance.brain)

data = {
    "activity" : np.zeros((n_neurons,sim_time)),#ïf it doesn't work, intervertir les deux
    # we will convert these datas into json-compatible data at the end of the simulation
    "adjacency" : instance.adjacency.matrix.tolist(),# assuming the structure of the network won't change along the simulation.
    "type" : [isinstance(neuron,Excitatory_Neuron) for neuron in instance.brain],
    "output_neurons" : []
}

#retrieve the index of the output neuron
if len(instance.output_neurons) == 0 : 
    print("no output neurons ! ")
else: 
    for o_n in instance.output_neurons : 
        for j in range (len(instance.brain)):
            if o_n == instance.brain[j] : 
                data["output_neurons"].append(j)

data["output_neurons"].sort()
print(data["output_neurons"])




k=0
while k < sim_time:
    instance.pass_inputs(inputs, k)
    instance.simulate(k, data["activity"])
    k+=1

#convert back to a json compatible format : 

data["activity"] = data["activity"].tolist()

with open(json_path,"w") as json_file: 
    json.dump(data ,json_file)
