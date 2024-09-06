import numpy as np
import matplotlib.pyplot as plt

import os 
import sys


project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(project_root)

from Neuroscience.structures.Controller import Controller
from Neuroscience.structures.Frequency_Detector import Frequency_Detector
# from Neuroscience.structures.Frequency_Detector_new import Frequency_Detector

res = 0.1
sim_time = 5000
N_REPEAT = Controller.N_REPEAT

ctrl = Controller(res,use_old_combinations=False)
V = [[np.zeros([sim_time, 1]) for _ in range(sim_time)] for _ in range(16)]
F = [[] for _ in range(N_REPEAT)]


inputs = np.zeros([sim_time,1])
inputs[1]=1
inputs[sim_time//2] = 1

# ctrl.create_oscillators(0)
print(ctrl.oscillators)
watch = Frequency_Detector(res ,controller = ctrl)

k=0
t= 0
#new

ctrl.pass_inputs(1)
while t<10:
    print(t*0.05)
    for i in range(500):
        watch.update_firing_rate(k)
        ctrl.simulate(k,V)
        ctrl.pass_inputs(0)

        if i == 0 and t!=0 : 
            ctrl.create_oscillators(t*0.05)
            ctrl.pass_inputs(1)



        for j in range(0,N_REPEAT):
            F[j].append( watch.get_freq(j))
        k+=1
    t+=1

# while t<4:
#     print(t*0.66)
#     print(ctrl.create_oscillators(t*0.66))
#     ctrl.pass_inputs(1)
#     for i in range(2500):
#         watch.update_firing_rate(k)
#         ctrl.simulate(k,V)
#         ctrl.pass_inputs(0)




#         for j in range(0,N_REPEAT):
#             F[j].append( watch.get_freq(j))
#         k+=1
#     t+=1

# Plot the results in a single figure with subplots
fig, axs = plt.subplots(6, 5, figsize=(15, 10))  # Create a grid of 7 rows x 3 columns
axs = axs.flatten()  # Flatten to make it easier to iterate over

for i in range (N_REPEAT):
    t = np.arange(0, len(V[ (4*(i+1)-1) ])) * 1  # Define the time axis
    axs[i].plot(t, V[ (4*(i+1)-1 )])#inhibitory neurons
    axs[i].plot(t, V[ (4*(i+1)-2 )])#excitatory neurons
    # axs[i].plot(t, V[4*i][3])

    axs[i].set_xlabel('Time [ms]')
    axs[i].set_ylabel('Voltage [mV]')
    axs[i].set_title('')

plt.tight_layout()  # Adjust subplots to fit into figure area.
plt.show()



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







