import numpy as np
import matplotlib.pyplot as plt
import os 
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))
sys.path.append(project_root)


from Neuroscience.structures.Tunable_Oscillator import Tunable_Oscillator
from Neuroscience.structures.Frequency_Detector import Frequency_Detector

res = 0.1

#---

#to see clearly spikes
sim_time = 5000

# to see clearly the frequency change
#sim_time = 10000

#---




NUM_TIMES = 2
VOLT_OFFSET = 11.9


inputs = np.zeros([sim_time,1])
inputs[1]=1


# builds a list of oscillators with different output firing threshold
#------------------------------------------------


V = [[np.zeros([sim_time, 1]) for _ in range(3)] for _ in range(NUM_TIMES)]
F = [[] for _ in range(NUM_TIMES)]
max = [[]for _ in range (NUM_TIMES)]

oscillators = []
output_neurons = []
for i in range(0,NUM_TIMES):
    # print(i)
    
    oscillators.append(Tunable_Oscillator(res = res))
    # print("i*15/21 = ",(i*15)/21)
    print("((i*(15-VOLT_OFFSET)/NUM_TIMES)+VOLT_OFFSET) = ", ((i*(15-VOLT_OFFSET)/NUM_TIMES)+VOLT_OFFSET))
    oscillators[i].tune(2,[((i*(15-VOLT_OFFSET)/NUM_TIMES)+VOLT_OFFSET),((i*(15-VOLT_OFFSET)/NUM_TIMES)+VOLT_OFFSET)])
    
    output_neurons.append(oscillators[i].brain[2])
    # oscillators[i].tune(0,[15,15])
    # oscillators[i].tune(1,[14.9,14.9])
    oscillators[i].brain[0].taken_inputs[1] = 1
freq = Frequency_Detector(res,output_neurons)


#runs the simulation for every oscillators
for i in range(0,NUM_TIMES):
    k = 1
    max[i].append(0)
    F[i].append(0)
    while k < sim_time :
        # in the middle of the simulation, retune the neurons so that they fire more
        if k == sim_time//2:
            None
            # print("i = ",i)
            # oscillators[i].tune(2,[((i*(15-VOLT_OFFSET+3)/NUM_TIMES)+VOLT_OFFSET-3),((i*(15-VOLT_OFFSET+3)/NUM_TIMES)+VOLT_OFFSET-3)])

        oscillators[i].brain[0].inputs[1] = inputs[k]
        # print(k)
        # print( "i = ",i )
        freq.update_firing_rate()
        # print(i,k)
        if (k<1000 and k>900):
            print("inside loop : what is plotted : ",freq.get_freq(i))
            print("inside loop : what is plotted : ",freq.get_freq(0))
        F[i].append( freq.get_freq(i))


        oscillators[i].simulate(k,V[i])
        # print(oscillators[i].brain[2].membrane_potential)
        # if oscillators[i].brain[2].max_active_potential == True:
        #     max[i].append(oscillators[i].brain[2].membrane_potential)
        # else :
        #     max[i].append(0)

        if freq.watch_neurons[i].max_active_potential == True:
            max[i].append(oscillators[i].brain[2].membrane_potential)
        else :
            max[i].append(0)
        k+=1
    
#-------------------------------------------------


# Plot the results in a single figure with subplots
fig, axs = plt.subplots(25, 4, figsize=(15, 10))  # Create a grid of 7 rows x 3 columns
axs = axs.flatten()  # Flatten to make it easier to iterate over




for i in range (NUM_TIMES):
    t = np.arange(0, len(V[i][0])) * res  # Define the time axis
    axs[i].plot(t, V[i][2])
    
    axs[i].plot(t, max[i])
    
    axs[i].set_xlabel('Time [ms]')
    axs[i].set_ylabel('Voltage [mV]')
    axs[i].set_title(f'last neuron input weight {((((i*(15-VOLT_OFFSET)/NUM_TIMES)+VOLT_OFFSET)*1000)//100)/10}')






# t = np.arange(0, len(V1[0])) * res  # Define the time axis
# axs[0].plot(t, V1[0])
# axs[0].set_xlabel('Time [ms]')
# axs[0].set_ylabel('Voltage [mV]')
# axs[0].set_title(f'Neuron {1} Voltage over Time')

# axs[1].plot(t, V2[0])
# axs[1].set_xlabel('Time [ms]')
# axs[1].set_ylabel('Voltage [mV]')
# axs[1].set_title(f'Neuron {1} Voltage over Time')

plt.tight_layout()  # Adjust subplots to fit into figure area.
plt.show()

for i in range(freq.len):
    # print(freq.frequency[i])
    print(freq.get_freq(i), "voltage = ",(((i*(15-VOLT_OFFSET)/NUM_TIMES)+VOLT_OFFSET)))

print (freq.frequency_ratio())

fig, axs = plt.subplots(25, 4, figsize=(15, 10))  # Create a grid of 7 rows x 3 columns
axs = axs.flatten()  # Flatten to make it easier to iterate over

for i in range (NUM_TIMES):
    t = np.arange(0, len(F[i])) * res  # Define the time axis
    axs[i].plot(t, F[i])
    axs[i].set_xlabel('Time [ms]')
    axs[i].set_ylabel('Frequency [Hz]')
    axs[i].set_title(f'last neuron input weight {((((i*(15-VOLT_OFFSET)/NUM_TIMES)+VOLT_OFFSET)*1000)//100)/10}')

plt.tight_layout()  # Adjust subplots to fit into figure area.
plt.show()