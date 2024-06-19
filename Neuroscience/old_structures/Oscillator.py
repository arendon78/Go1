import matplotlib.pyplot as plt
import numpy as np

# Import both Excitatory and Inhibitory Neuron models
from Neuroscience.structures.Excitatory_Neuron import Excitatory_Neuron

res = 0.1                        #Set the resolution
sim_time = 1000                   #Set the simulation time
#V = np.zeros([sim_time,1])            #Initialize V.
#V[0]=0                           #Set the initial value of V.
#Initialize V.
V = [np.zeros([sim_time,1]), np.zeros([sim_time,1])]

# Initialize neurons
neuron1 = Excitatory_Neuron(res, 2, 1)
neuron1.set_weights([15,15])

neuron2 = Excitatory_Neuron(res, 1, 1)
neuron2.set_weights([15])

# Establish connections between neurons
neuron1.connect_with_neuron(neuron2)
neuron2.connect_with_neuron(neuron1)

# Prevent any other neurons from connecting to the remaining dendrite from neuron1
neuron1.taken_inputs[1] = 1

# Create the neural network
brain = [neuron1, neuron2]

inputs = np.zeros([sim_time,1])            #Initialize V.

inputs[1] = [1]

k=1

while k < sim_time:
    neuron_count = 0

    # Set inputs just for the 2nd dendrite of neuron1, which is the starting neuron in the network
    neuron1.inputs[1] = inputs[k]

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

    plt.figure()                         #Plot the results.
    plt.plot(t,V[i])
    plt.xlabel('Time [ms]')
    plt.ylabel('Voltage [mV]');
    plt.show()
