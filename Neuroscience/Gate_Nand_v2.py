import matplotlib.pyplot as plt
import numpy as np

# Import both Excitatory and Inhibitory Neuron models
from Excitatory_Neuron import Excitatory_Neuron
from Inhibitory_Neuron import Inhibitory_Neuron

res = 0.1                        #Set the resolution
sim_time = 2000                   #Set the simulation time
#V = np.zeros([sim_time,1])            #Initialize V.
#V[0]=0                           #Set the initial value of V.
#Initialize V.
V = [np.zeros([sim_time,1]), np.zeros([sim_time,1]), np.zeros([sim_time,1]), 
     np.zeros([sim_time,1]), np.zeros([sim_time,1]), np.zeros([sim_time,1]), np.zeros([sim_time,1])]

# Initialize neurons
neuron0 = Excitatory_Neuron(res, 2, 4)
neuron0.set_weights([7.5,7.5])

neuron1 = Excitatory_Neuron(res, 1, 1)
neuron1.set_weights([15])

neuron2 = Inhibitory_Neuron(res, 3, 1)
neuron2.set_weights([15,15,15])

neuron3 = Inhibitory_Neuron(res, 1, 1)
neuron3.set_weights([15])

neuron4 = Excitatory_Neuron(res, 2, 2)
neuron4.set_weights([15,15])

neuron5 = Excitatory_Neuron(res, 1, 2)
neuron5.set_weights([15])

neuron6 = Excitatory_Neuron(res, 4, 1)
neuron6.set_weights([15,15,8,8])

# Establish connections between neurons
neuron0.connect_with_neuron(neuron1)
neuron0.connect_with_neuron(neuron2)
neuron0.connect_with_neuron(neuron2)
neuron0.connect_with_neuron(neuron2)
neuron1.connect_with_neuron(neuron3)
neuron2.connect_with_neuron(neuron6)
neuron3.connect_with_neuron(neuron6)
neuron4.connect_with_neuron(neuron5)
neuron4.connect_with_neuron(neuron6)
neuron5.connect_with_neuron(neuron4)
neuron5.connect_with_neuron(neuron6)

# Prevent any other neurons from connecting to the remaining dendrite from neuron4
neuron4.taken_inputs[1] = 1

# Create the neural network
brain = [neuron0, neuron1, neuron2, neuron3, neuron4, neuron5, neuron6]

inputs = np.zeros([sim_time,3])            #Initialize V.

inputs[1] = [0,0,1]
inputs[100] = [0,1,0]
inputs[210] = [1,0,0]
inputs[550] = [0,1,0]
inputs[660] = [1,0,0]

inputs[1000] = [1,1,0]
inputs[1110] = [1,1,0]
inputs[1230] = [1,1,0]
'''
inputs[1110] = [1,1,0]
inputs[1220] = [1,1,0]
inputs[1330] = [1,1,0]
inputs[1440] = [1,1,0]
inputs[1550] = [1,1,0]
inputs[1660] = [1,1,0]
inputs[1770] = [1,1,0]
inputs[1880] = [1,1,0]
inputs[1990] = [1,1,0]
'''
k=1

while k < sim_time:
    neuron_count = 0

    # Set inputs just for the 2nd dendrite of neuron4, which is the starting neuron in the network
    neuron4.inputs[1] = inputs[k][2]

    # Set inputs for not gate (neuron0)
    neuron0.inputs[0] = inputs[k][0]
    neuron0.inputs[1] = inputs[k][1]

    # One for loop for calculating the state of the neurons with the current inputs
    for neuron in brain:
        # If there's an input present and an action potential is not going on,
        # then prepare to keep track of the voltage and reinitialize timers
        neuron.present_inputs(neuron.inputs)

        # If there's no active potential taking place,
        # call spatial_summation function to keep track of the overall voltage in the neuron
        if not neuron.active_potential_bool:
            V[neuron_count][k] = neuron.spatial_summation()

        # There is an active potential taking place
        if neuron.active_potential_bool:
            neuron.time_neuron += 1
            # Call to active potential function
            V[neuron_count][k] = neuron.active_potential(neuron.time_neuron*neuron.resolution) #... updating V along the way.
            # End of call to active potential function

        # The PSP or the active potential are over
        # Reset voltage, time, and temporal summation of the neuron to 0
        if not np.any(neuron.active_PSP) and not neuron.active_potential_bool:
            V[neuron_count][k] = 0
            neuron.time_neuron = 0
            neuron.membrane_potential = 0

        # Update current outputs of the neurons to their connected neurons for the next iteration
        neuron.propagate_outputs()

        # Update neuron counter
        neuron_count += 1

    k += 1

# Plot outputs from all neurons
for i in range(len(brain)):
    t = np.arange(0,len(V[i]))*res          #Define the time axis.

#    if i <= 2 or i == 5:
    if i == 0 or i == 6:
        plt.figure()                         #Plot the results.
        if i == 0: plt.plot(t,V[i],color="red")
        if i == 6: plt.plot(t,V[i],color="blue")
        plt.xlabel('Time [ms]')
        plt.ylabel('Voltage [mV]');
        plt.show()
