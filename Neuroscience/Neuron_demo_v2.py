import matplotlib.pyplot as plt
import numpy as np

# Import both Excitatory and Inhibitory Neuron models
from Excitatory_Neuron import Excitatory_Neuron
from Inhibitory_Neuron import Inhibitory_Neuron

res = 0.1                        #Set the resolution
sim_time = 1000                   #Set the simulation time
V = np.zeros([sim_time,1])            #Initialize V.
V[0]=0                           #Set the initial value of V.

# Initialize neurons
neuron1 = Excitatory_Neuron(res, 2, 2)
neuron1.set_weights([5,5])

neuron2 = Inhibitory_Neuron(res, 2, 2)
neuron2.set_weights([5,3])

neuron3 = Excitatory_Neuron(res, 2, 2)
neuron3.set_weights([2,3])

# Establish connections between neurons
neuron1.connect_with_neuron(neuron2)
neuron1.connect_with_neuron(neuron3)

neuron2.connect_with_neuron(neuron3)
neuron2.connect_with_neuron(neuron3)

neuron3.connect_with_neuron(neuron2)
neuron3.connect_with_neuron(neuron2)

#inputs = np.zeros([sim_time,1])            #Initialize V.
inputs = np.zeros([sim_time, neuron1.num_dendrites])            #Initialize V.
inputs[10] = [0,1]
inputs[80] = [1,0]
inputs[150] = [1,1]
inputs[220] = [1,0]
inputs[400] = [1,1]
inputs[460] = [1,1]
inputs[600] = [1,0]
inputs[670] = [0,1]
inputs[740] = [1,0]
inputs[800] = [1,1]
inputs[870] = [1,0]

k=1

while k < sim_time:
    # One for loop for calculating the state of the neurons with the current inputs

    # If there's an input present and an action potential is not going on,
    # then prepare to keep track of the voltage and reinitialize timers
    neuron1.present_inputs(inputs[k])

    # If there's no active potential taking place,
    # call spatial_summation function to keep track of the overall voltage in the neuron
    if not neuron1.active_potential_bool:
        V[k] = neuron1.spatial_summation()

    # There is an active potential taking place
    if neuron1.active_potential_bool:
        neuron1.time_neuron += 1
        # Call to active potential function
        V[k] = neuron1.active_potential(neuron1.time_neuron*neuron1.resolution) #... updating V along the way.
        # End of call to active potential function

    # The PSP or the active potential are over
    # Reset voltage, time, and temporal summation of the neuron to 0
    if not np.any(neuron1.active_PSP) and not neuron1.active_potential_bool:
        V[k] = 0
        neuron1.time_neuron = 0
        neuron1.membrane_potential = 0

    # Another for loop for updating current outputs of the neurons to their connected neurons for the next iteration
    

    k += 1

t = np.arange(0,len(V))*res          #Define the time axis.

plt.figure()                         #Plot the results.
plt.plot(t,V)
plt.xlabel('Time [ms]')
plt.ylabel('Voltage [mV]');
plt.show()
