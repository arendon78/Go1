import matplotlib.pyplot as plt
import numpy as np
import statistics

import os 
import sys


project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(project_root)


from Neuroscience.structures.Organ import Organ
from Neuroscience.structures.Counter_4_bits import Counter_4_bits
from Neuroscience.structures.Frequency_Detector import Frequency_Detector
from Neuroscience.structures.Activity_Detector import Activity_Detector


res = 0.1                       #Set the resolution
sim_time = 20000               #Set the simulation time
x = 120                  # number of neurons in this simulation

DELAY = Activity_Detector.DELAY
#Initialize V.
V = []
change_bit = []




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

counter = Counter_4_bits(res)#add res argument ? 
freq = Frequency_Detector(res,counter.output_neurons,delta_t = 170)
act = Activity_Detector(counter.output_neurons)


change_bit = np.zeros([sim_time,1])


# Inhibitory neurons may be needed to block the inputs and prevent other neurons from firing
# once the desired output is obtained


change_times = []
bitcode_values = []

F = []
k = 0
previous_bitcode = "0000"
start = 0
times_elapsed = []
missed = set()

while k < sim_time:
    counter.pass_inputs(inputs, k)
    counter.simulate(k, V)
    if k > 250 : 
        act.update_activity()
        bitcode = act.get_activity()

        if bitcode != previous_bitcode:
            missed.add(bitcode)
            # if int(bitcode, 2) == (int(previous_bitcode, 2) + 1) % 16:
            missed.remove(bitcode)
            # print("\nfinally !  here are the bytes that you missed : ",missed)
            missed = set()
            end = k
            # change_times.append((k-800) * res)  # Store the time of the change
            change_bit[int(k-DELAY)] = 80
            bitcode_values.append(bitcode)  # Store the bitcode at that time
            # print("Time elapsed : ", end - start)
            times_elapsed.append(end-start)
            # print("k = ", (k / 10 - 80))
            start = k
            print(bitcode)
            previous_bitcode = bitcode
    k+=1

standard_dev = statistics.stdev(times_elapsed)
print("standard deviation : ", standard_dev)

t=  [i for i in range(len(times_elapsed))]
plt.figure()
plt.plot(t, times_elapsed)
plt.xlabel('number of the counter base 10')
plt.ylabel("delay")
# ax = plt.gca()
# ax.set_ylim([-40, 100])
plt.show()


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
        plt.plot(t,change_bit)
        plt.xlabel('Time [ms]')
        plt.ylabel('Voltage [mV]')
        ax = plt.gca()
        ax.set_ylim([-40, 100])
        plt.show()

print([el.name for el in counter.brain])


print(len(counter.brain))

o = Organ()
for neuron in counter.brain:
    o.add_to_brain(neuron)

# o.build_and_display_neuron_graph()