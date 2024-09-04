import matplotlib.pyplot as plt
import numpy as np
import os 
import sys
import statistics

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(project_root)

from Neuroscience.structures.Organ import Organ
from Neuroscience.structures.Counter_2_bits import Counter_2_bits
from Neuroscience.structures.Frequency_Detector import Frequency_Detector
from Neuroscience.structures.Activity_Detector import Activity_Detector

res = 0.1                       # Set the resolution
sim_time = 80000               # Set the simulation time
x = 90                          # Number of neurons in this simulation

# Initialize V.
V = []

for i in range(x):
    V.insert(i, np.zeros([sim_time, 1]))

inputs = np.zeros([sim_time, 2])  # Initialize inputs

inputs[0] = [0,1]
# Setup input pulses
for i in range(sim_time): 
    if i % 1000 == 700 or i % 1000 == 810: 
        # if i == 700: 
        #     inputs[i] = [1, 1]
        # else:
            inputs[i] = [1, 0]

# Initialization of counter
counter = Counter_2_bits(res)
freq = Frequency_Detector(res, counter.output_neurons, delta_t=170, spike_detector=True)
act = Activity_Detector(counter.output_neurons)

# Lists to store the times when bitcode changes and the corresponding bitcodes
change_times = []
bitcode_values = []

# Simulation loop
F = []
k = 0
previous_bitcode = "00"
start = 0
times_elapsed = []  

while k < sim_time:
    counter.pass_inputs(inputs, k)
    counter.simulate(k, V)

    act.update_activity()
    bitcode = act.get_activity()

    if bitcode != previous_bitcode:
        if int(bitcode, 2) == (int(previous_bitcode, 2) + 1) % 2:
            end = k
            change_times.append((k-800) * res)  # Store the time of the change
            bitcode_values.append(bitcode)  # Store the bitcode at that time
            print("Time elapsed : ", end - start)
            times_elapsed.append(end-start)
            print("k = ", (k / 10 - 80))
            start = k
            print(bitcode)
            previous_bitcode = bitcode
    k += 1

standard_dev = statistics.stdev(times_elapsed)
print("standard deviation : ", standard_dev)

# Plot outputs from all neurons and mark bitcode changes
for i in range(len(counter.brain)):
    t = np.arange(0, len(V[i])) * res  # Define the time axis
    if counter.brain[i] in counter.output_neurons or i == len(counter.brain) - 1 or i == len(counter.brain) - 2 :
        plt.figure()  # Plot the results
        plt.plot(t, V[i], label="Voltage")
        
        # Plot the bitcode change points
        plt.scatter(change_times, np.zeros_like(change_times), color='red', label='Bitcode Change', zorder=5)
        
        plt.xlabel('Time [ms]')
        plt.ylabel('Voltage [mV]')
        ax = plt.gca()
        ax.set_ylim([-40, 100])
        plt.legend()
        plt.show()

print(len(counter.brain))