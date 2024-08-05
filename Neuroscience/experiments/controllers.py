import numpy as np
import matplotlib.pyplot as plt

import os 
import sys


project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(project_root)

from Neuroscience.structures.Controller import Controller
from Neuroscience.structures.Frequency_Detector import Frequency_Detector

res = 0.1
sim_time = 10000
N_REPEAT = 4

ctrl = Controller(res)
V = [[np.zeros([sim_time, 1]) for _ in range(4)] for _ in range(4)]
F = [[] for _ in range(N_REPEAT)]


inputs = np.zeros([sim_time,1])
inputs[1]=1
inputs[sim_time//2] = 1

ctrl.create_oscillators(0)
watch = Frequency_Detector(res ,controller = ctrl)

k=0
# while k < sim_time :
#     if k<sim_time//2:
#         watch.update_firing_rate(k)

#         if k == 0: 
#             ctrl.pass_inputs(1)
#         else: 
#             ctrl.pass_inputs(0)

#         ctrl.simulate(k,V)

#         for i in range(0,N_REPEAT):
#             F[i].append( watch.get_freq(i))
        
#     if k == sim_time//2 : 
#         ctrl.create_oscillators(0.0001)
#         ctrl.pass_inputs(1)

#     if k>=sim_time//2:
#         watch.update_firing_rate(k)
#         if k != sim_time//2:
#             ctrl.pass_inputs(0)
        
#         ctrl.simulate(k,V)

#         for i in range(0,N_REPEAT):
#             F[i].append( watch.get_freq(i))
#         # print("frequency detector : ",watch.frequency_ratio())

#     k+=1

t=0

# old 
# while t<10:
#     for i in range(1000):
#         watch.update_firing_rate(k)

#         if i == 0: 
#             ctrl.create_oscillators(t*0.1)
#             ctrl.pass_inputs(1)
            
#         else: 
#             ctrl.pass_inputs(0)

#         ctrl.simulate(k,V)

#         for i in range(0,N_REPEAT):
#             F[i].append( watch.get_freq(i))
#         k+=1
#     t+=1

#new
ctrl.pass_inputs(1)
while t<10:
    for i in range(1000):
        watch.update_firing_rate(k)


        if i == 0 and t!=0 : 
            ctrl.create_oscillators(t*0.05)

        ctrl.simulate(k,V)
        ctrl.pass_inputs(0)

        for i in range(0,N_REPEAT):
            F[i].append( watch.get_freq(i))
        k+=1
    t+=1


# Plot the results in a single figure with subplots
fig, axs = plt.subplots(6, 5, figsize=(15, 10))  # Create a grid of 7 rows x 3 columns
axs = axs.flatten()  # Flatten to make it easier to iterate over

for i in range (N_REPEAT):
    t = np.arange(0, len(V[i][0])) * 1  # Define the time axis
    axs[i].plot(t, V[i][2])
    axs[i].plot(t, V[i][3])

    axs[i].set_xlabel('Time [ms]')
    axs[i].set_ylabel('Voltage [mV]')
    axs[i].set_title('')

plt.tight_layout()  # Adjust subplots to fit into figure area.
plt.show()

print(watch.print_frequency())
print(watch.frequency_ratio())
print("convert to motion : ")
print(watch.convert_to_motion(0))
print("neurons fire : ")
print(watch.neurons_fire_string())



fig, axs = plt.subplots(6, 5, figsize=(15, 10))  # Create a grid of 7 rows x 3 columns
axs = axs.flatten()  # Flatten to make it easier to iterate over

for i in range (N_REPEAT):
    t = np.arange(0, len(F[i])) *1  # Define the time axis
    axs[i].plot(t, F[i])
    axs[i].set_xlabel('Time [ms]')
    axs[i].set_ylabel('Frequency [Hz]')
    axs[i].set_title(f'')

plt.tight_layout()  # Adjust subplots to fit into figure area.
plt.show()





