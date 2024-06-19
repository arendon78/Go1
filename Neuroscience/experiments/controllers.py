import os 
import sys
import numpy as np
import matplotlib.pyplot as plt

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(project_root)

from Neuroscience.structures.Controller import Controller
from Neuroscience.structures.Frequency_Detector import Frequency_Detector

res = 0.1
sim_time = 1000
N_REPEAT = 5

ctrl = Controller(res)
V = [[np.zeros([sim_time, 1]) for _ in range(3)] for _ in range(N_REPEAT)]
inputs = np.zeros([sim_time,1])
inputs[1]=1

ctrl.create_oscillators(0.4)

outputs = [neur.brain[2] for neur in ctrl.oscillators]

watch = Frequency_Detector(res ,outputs)

# ctrl.activate()# activates the oscillator

for i in range(0,N_REPEAT):
    k=1
    while k < sim_time :

        ctrl.oscillators[i].brain[0].inputs[1] = inputs[k]
        watch.update_firing_rate()
        
        ctrl.oscillators[i].simulate(k,V[i])
        # ctrl.simulate(k,V)

        k+=1
    
# Plot the results in a single figure with subplots
fig, axs = plt.subplots(6, 5, figsize=(15, 10))  # Create a grid of 7 rows x 3 columns
axs = axs.flatten()  # Flatten to make it easier to iterate over

for i in range (N_REPEAT):
    t = np.arange(0, len(V[i][0])) * res  # Define the time axis
    axs[i].plot(t, V[i][2])

    axs[i].set_xlabel('Time [ms]')
    axs[i].set_ylabel('Voltage [mV]')
    axs[i].set_title('')

# print(ctrl.find_combination(0.5))
plt.tight_layout()  # Adjust subplots to fit into figure area.
plt.show()

# [10000.0, 45.045045045045036, 0, 45.045045045045036]
# print("print frequencyyyy")
print(watch.print_frequency())
# print("hey")
print(watch.frequency_ratio())
print("convert to motion : ")
print(watch.convert_to_motion(0))



