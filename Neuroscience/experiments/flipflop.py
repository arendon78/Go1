import matplotlib.pyplot as plt
import numpy as np
import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(project_root)

# Import both Excitatory and Inhibitory Neuron models
from Neuroscience.structures.Excitatory_Neuron import Excitatory_Neuron
from Neuroscience.structures.Inhibitory_Neuron import Inhibitory_Neuron
from Neuroscience.structures.Flip_FLop_T import Flip_Flop_T
from Neuroscience.structures.Organ import Organ

res = 0.1                       #Set the resolution
sim_time = 2000                 #Set the simulation time
x = 29                          # number of neurons in this simulation

#Initialize V.
V = []

for i in range(x):
    V.insert(i, np.zeros([sim_time,1]))


FlipFlop = Flip_Flop_T()


inputs = np.zeros([sim_time,3])            #Initialize V.

# inputs[0] = T input, inputs[1] = clock signal, inputs[2] = starting signal for oscillators of each nand gate

inputs[1] = [0,0,1]

# Needs two consecutive pulses 110 apart from each other to work
# inputs[500] = [1,1,0]
# inputs[610] = [1,1,0]


# There is a delay in the reponse from the system
# The human brain must have a lot of redundancy for it to work correctly

# Inhibitory neurons may be needed to block the inputs and prevent other neurons from firing
# once the desired output is obtained

inputs[850] = [1,1,0]
inputs[960] = [1,1,0]

k=1

while k < sim_time:
    
    FlipFlop.start(inputs,k)

    FlipFlop.simulate(k,V)
    

    k += 1

# Plot outputs from all neurons

print(len(FlipFlop.brain))

for i in range(len(FlipFlop.brain)):
    t = np.arange(0,len(V[i]))*res          #Define the time axis.
    if i == 0 or i == 7 or i == 27 or i == 28:
        print("i = ",i, "corresponding flipflop",FlipFlop.brain[i])
        plt.figure()                         #Plot the results.
        plt.plot(t,V[i])
        plt.xlabel('Time [ms]')
        plt.ylabel('Voltage [mV]')
        ax = plt.gca()
        ax.set_ylim([-40, 100])
        plt.show()

print(FlipFlop.fst_NAND.brain[0])
print(FlipFlop.scd_NAND.brain[0])
print(FlipFlop.fth_NAND.brain[-1])
print(FlipFlop.brain[-1])

# FlipFlop.print()


o = Organ()
for neuron in FlipFlop.brain:
    o.add_to_brain(neuron)

o.build_and_display_neuron_graph()