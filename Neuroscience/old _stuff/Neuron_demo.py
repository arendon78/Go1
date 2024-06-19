import matplotlib.pyplot as plt
import numpy as np

from Neuron import Neuron

res = 0.1                        #Set the resolution
sim_time = 1000                   #Set the simulation time
V = np.zeros([sim_time,1])            #Initialize V.
V[0]=0                           #Set the initial value of V.

# Initialize neuron
neuron = Neuron(res)
neuron.set_weights([5,3])

#inputs = np.zeros([sim_time,1])            #Initialize V.
inputs = np.zeros([sim_time, neuron.num_dendrites])            #Initialize V.
inputs[10] = [0,1]
inputs[80] = [1,0]
inputs[150] = [1,1]
inputs[210] = [0,1]
inputs[400] = [1,1]
inputs[460] = [1,1]
inputs[600] = [1,0]
inputs[670] = [0,1]
inputs[740] = [1,0]
inputs[800] = [1,1]
inputs[870] = [1,0]

k=1
time = 0
while k < sim_time:

    # If there's an input present and an action potential is not going on,
    # then prepare to keep track of the voltage and reinitialize timers
    neuron.present_inputs(inputs[k])

    # If there's no active potential taking place,
    # call spatial_summation function to keep track of the overall voltage in the neuron
    if not neuron.active_potential_bool:
        V[k] = neuron.spatial_summation()

    # There is an active potential taking place
    if neuron.active_potential_bool:
        neuron.time_neuron += 1
        # Call to active potential function
        V[k] = neuron.active_potential(neuron.time_neuron*neuron.resolution) #... updating V along the way.
        # End of call to active potential function

    # The PSP or the active potential are over
    # Reset voltage, time, and temporal summation of the neuron to 0
    if not np.any(neuron.active_PSP) and not neuron.active_potential_bool:
        V[k] = 0
        neuron.time_neuron = 0
        neuron.membrane_potential = 0

    k += 1

t = np.arange(0,len(V))*res          #Define the time axis.

plt.figure()                         #Plot the results.
plt.plot(t,V)
plt.xlabel('Time [ms]')
plt.ylabel('Voltage [mV]');
plt.show()
