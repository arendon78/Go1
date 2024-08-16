import matplotlib.pyplot as plt
import numpy as np

import os 
import sys


project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(project_root)

from Neuroscience.structures.Organ import Organ
from Neuroscience.structures.Counter_3_bits import Counter_3_bits

res = 0.1                       #Set the resolution
sim_time = 40000                #Set the simulation time
x = 90                          # number of neurons in this simulation

#Initialize V.
V = []

for i in range(x):
    V.insert(i, np.zeros([sim_time,1]))

inputs = np.zeros([sim_time,2])            #Initialize V.

# inputs[0] = T input, inputs[1] = clock signal, inputs[2] = starting signal for oscillators of each nand gate

inputs[1] = [0,1]

# Needs two consecutive pulses 110 apart from each other to work
# inputs[700] = [1,0]
# inputs[810] = [1,0]
# inputs[1700] = [1,0]
# inputs[1810] = [1,0]
# inputs[2700] = [1,0]
# inputs[2810] = [1,0]
# inputs[3700] = [1,0]
# inputs[3810] = [1,0]
# inputs[4700] = [1,0]
# inputs[4810] = [1,0]
# inputs[5700] = [1,0]
# inputs[5810] = [1,0]
# inputs[6700] = [1,0]
# inputs[6810] = [1,0]
# inputs[7700] = [1,0]
# inputs[7810] = [1,0]
# inputs[8700] = [1,0]
# inputs[8810] = [1,0]
# inputs[9700] = [1,0]
# inputs[9810] = [1,0]

for i in range(sim_time): 
    if i %1000 == 700 or i%1000 == 810 : 
        inputs[i] = [1,0]

#initialisation of counter

counter = Counter_3_bits(res)

# Inhibitory neurons may be needed to block the inputs and prevent other neurons from firing
# once the desired output is obtained

k=1

while k < sim_time:
    neuron_count = 0
    counter.pass_inputs(inputs,k)
    counter.simulate(k,V)
    k+=1

# Plot outputs from all neurons
for i in range(len(counter.brain)):
    t = np.arange(0,len(V[i]))*res          #Define the time axis.
    if counter.brain[i] in counter.output_neurons:
    # if i == 28 or i == 57 or i == 86 or i == 89:
#    if i == 4 or i == 11 or i == 18 or i == 25: # oscillators for flip flop T2
#    if i == 33 or i == 40 or i == 47 or i == 54: # oscillators for flip flop T1
#    if i == 62 or i == 69 or i == 76 or i == 83: # oscillators for flip flop T0
        plt.figure()                         #Plot the results.
        plt.plot(t,V[i])
        plt.xlabel('Time [ms]')
        plt.ylabel('Voltage [mV]')
        ax = plt.gca()
        ax.set_ylim([-40, 100])
        plt.show()
print([el.name for el in counter.brain])

o = Organ()
for neuron in counter.brain:
    o.add_to_brain(neuron)

# o.build_and_display_neuron_graph()