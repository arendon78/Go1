import numpy as np
import matplotlib.pyplot as plt

import os 
import sys


project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(project_root)

from Neuroscience.structures.Controller import Controller
from Neuroscience.structures.Frequency_Detector import Frequency_Detector

res = 0.1
sim_time = 5000
N_REPEAT = 4

ctrl = Controller(res)
V = [[np.zeros([sim_time, 1]) for _ in range(3)] for _ in range(4)]
F = [[] for _ in range(N_REPEAT)]


inputs = np.zeros([sim_time,1])
inputs[1]=1
inputs[sim_time//2] = 1

ctrl.create_oscillators(0.01)

# outputs = [neur.brain[2] for neur in ctrl.oscillators]
# [print("output neuron number  : ", neur.name) for neur in outputs]

watch = Frequency_Detector(res ,controller = ctrl)

# ctrl.activate()# activates the oscillator

# for i in range(0,N_REPEAT):
#     k=1
#     while k < sim_time :

#         ctrl.oscillators[i].brain[0].inputs[1] = inputs[k]
#         watch.update_firing_rate(k)
#         print("k : ",k)
#         print("watch.internal_time : ",watch.internal_time)
        
#         ctrl.oscillators[i].simulate(k,V[i])
#         # ctrl.simulate(k,V)
#         F[i].append( watch.get_freq_hertz(i))

#         k+=1
    

k=0
while k < sim_time :
    print(len(V))
    if k%1000 == 0:
        print(watch.print_frequency())
    if k<sim_time//2:
        # 
        # ctrl.oscillators[i].brain[0].inputs[1] = inputs[k]
        # 
        if k == 0: 
            ctrl.pass_inputs(1)
        else: 
            ctrl.pass_inputs(0)
        # print("k : ",k)
        # print("watch.internal_time : ",watch.internal_time)

        # 
        # ctrl.oscillators[i].simulate(k,V[i])
        # 
        ctrl.simulate(k,V)

        watch.update_firing_rate()
        # ctrl.simulate(k,V)

        for i in range(0,N_REPEAT):
            F[i].append( watch.get_freq_hertz(i))
        print(watch.frequency_ratio())
        
    if k == sim_time//2 : 
#         print("created new oscillator")
        ctrl.create_oscillators(0.57)
        ctrl.pass_inputs(1)


    if k>=sim_time//2:
        if k != sim_time//2:
            ctrl.pass_inputs(0)

        # print("here ! k = ",k)
# 
        ctrl.simulate(k,V)
# 
        watch.update_firing_rate()
        # ctrl.simulate(k,V)
# 
        for i in range(0,N_REPEAT):
            F[i].append( watch.get_freq_hertz(i))
        print(watch.frequency_ratio())

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
print("neurons fire : ")
print(watch.neurons_fire_string())



fig, axs = plt.subplots(6, 5, figsize=(15, 10))  # Create a grid of 7 rows x 3 columns
axs = axs.flatten()  # Flatten to make it easier to iterate over

for i in range (N_REPEAT):
    t = np.arange(0, len(F[i])) * res  # Define the time axis
    axs[i].plot(t, F[i])
    axs[i].set_xlabel('Time [ms]')
    axs[i].set_ylabel('Frequency [Hz]')
    axs[i].set_title(f'')

plt.tight_layout()  # Adjust subplots to fit into figure area.
plt.show()





