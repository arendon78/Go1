import matplotlib.pyplot as plt
import numpy as np

# Import both Excitatory and Inhibitory Neuron models
from structures.Excitatory_Neuron import Excitatory_Neuron
from structures.Tunable_Oscillator import Tunable_Oscillator

#### Header
#---------------
res = 0.1                        #Set the resolution
sim_time = 1000            #Set the simulation time
#V = np.zeros([sim_time,1])            #Initialize V.
#V[0]=0                           #Set the initial value of V.
#Initialize V.
V = [np.zeros([sim_time,1]), np.zeros([sim_time,1]), np.zeros([sim_time,1])]
#---------------

# # Initialize neurons
# neuron1 = Excitatory_Neuron(res, 2, 2)
# neuron1.set_weights([15,15])
# # 
# neuron2 = Excitatory_Neuron(res, 1, 2)
# neuron2.set_weights([15])
# # 
# neuron3 = Excitatory_Neuron(res, 2, 1)
# neuron3.set_weights([7.8,7.8])

# Establish connections between neurons
oscil = Tunable_Oscillator(res = res)

#could also be 
# oscil = Tunable_Oscillator(neuron1,neuron2,neuron3)

# Prevent any other neurons from connecting to the remaining dendrite from neuron1
# neuron1.taken_inputs[1] = 1
oscil.brain[0].taken_inputs[1] = 1


# Create the neural network

inputs = np.zeros([sim_time,1])            #Initialize V.
inputs[1] = [1]
k=1


#main loop
while k < sim_time:
    oscil.brain[0].inputs[1] = inputs[k]
    oscil.simulate(k,V)
    k += 1


# Plot outputs from all neurons
for i in range(len(oscil.brain)):
    t = np.arange(0,len(V[i]))*res          #Define the time axis.

    plt.figure()                         #Plot the results.
    plt.plot(t,V[i])
    plt.xlabel('Time [ms]')
    plt.ylabel('Voltage [mV]');
    plt.show()
