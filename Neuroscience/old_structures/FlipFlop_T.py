import matplotlib.pyplot as plt
import numpy as np

# Import both Excitatory and Inhibitory Neuron models
from structures.Excitatory_Neuron import Excitatory_Neuron
from structures.Inhibitory_Neuron import Inhibitory_Neuron

res = 0.1                       #Set the resolution
sim_time = 2000                  #Set the simulation time
x = 17                          # number of neurons in this simulation

#Initialize V.
V = []

for i in range(x):
    V.insert(i, np.zeros([sim_time,1]))

# Initialize neurons

# 1st NAND Gate
neuron1_1 = Inhibitory_Neuron(res, 3, 2)
neuron1_1.set_weights([5,5,5])

neuron1_2 = Excitatory_Neuron(res, 2, 2)
neuron1_2.set_weights([15,15])

neuron1_3 = Excitatory_Neuron(res, 1, 2)
neuron1_3.set_weights([15])

neuron1_4 = Excitatory_Neuron(res, 4, 1)
neuron1_4.set_weights([15,15,14,14])

# Establish connections between neurons inside the nand gate
neuron1_1.connect_with_neuron(neuron1_4)
neuron1_1.connect_with_neuron(neuron1_4)
neuron1_2.connect_with_neuron(neuron1_3)
neuron1_2.connect_with_neuron(neuron1_4)
neuron1_3.connect_with_neuron(neuron1_2)
neuron1_3.connect_with_neuron(neuron1_4)

# Prevent any other neurons from connecting to the remaining dendrite from neuron1_2
# This dendrite is the one activating the oscillator inside the nand gate
neuron1_2.taken_inputs[1] = 1

# 2nd NAND Gate
neuron2_1 = Inhibitory_Neuron(res, 3, 2)
neuron2_1.set_weights([5,5,5])

neuron2_2 = Excitatory_Neuron(res, 2, 2)
neuron2_2.set_weights([15,15])

neuron2_3 = Excitatory_Neuron(res, 1, 2)
neuron2_3.set_weights([15])

neuron2_4 = Excitatory_Neuron(res, 4, 1)
neuron2_4.set_weights([15,15,14,14])

# Establish connections between neurons inside the nand gate
neuron2_1.connect_with_neuron(neuron2_4)
neuron2_1.connect_with_neuron(neuron2_4)
neuron2_2.connect_with_neuron(neuron2_3)
neuron2_2.connect_with_neuron(neuron2_4)
neuron2_3.connect_with_neuron(neuron2_2)
neuron2_3.connect_with_neuron(neuron2_4)

# Prevent any other neurons from connecting to the remaining dendrite from neuron2_2
# This dendrite is the one activating the oscillator inside the nand gate
neuron2_2.taken_inputs[1] = 1

# 3rd NAND Gate
neuron3_1 = Inhibitory_Neuron(res, 2, 2)
neuron3_1.set_weights([7.5,7.5])

neuron3_2 = Excitatory_Neuron(res, 2, 2)
neuron3_2.set_weights([15,15])

neuron3_3 = Excitatory_Neuron(res, 1, 2)
neuron3_3.set_weights([15])

neuron3_4 = Excitatory_Neuron(res, 4, 1)
neuron3_4.set_weights([15,15,14,14])

neuron3_5 = Excitatory_Neuron(res, 1, 1) # Neuron to provide a delay between neurons 3 and 4
neuron3_5.set_weights([15])

# Establish connections between neurons inside the nand gate
neuron3_1.connect_with_neuron(neuron3_4)
neuron3_1.connect_with_neuron(neuron3_4)
neuron3_2.connect_with_neuron(neuron3_3)
neuron3_2.connect_with_neuron(neuron3_4)
neuron3_3.connect_with_neuron(neuron3_2)
neuron3_3.connect_with_neuron(neuron3_4)

# Prevent any other neurons from connecting to the remaining dendrite from neuron3_2
# This dendrite is the one activating the oscillator inside the nand gate
neuron3_2.taken_inputs[1] = 1

# 4th NAND Gate
neuron4_1 = Inhibitory_Neuron(res, 2, 2)
neuron4_1.set_weights([7.5,7.5])

neuron4_2 = Excitatory_Neuron(res, 2, 2)
neuron4_2.set_weights([15,15])

neuron4_3 = Excitatory_Neuron(res, 1, 2)
neuron4_3.set_weights([15])

neuron4_4 = Excitatory_Neuron(res, 4, 1)
neuron4_4.set_weights([15,15,14,14])

# Establish connections between neurons inside the nand gate
neuron4_1.connect_with_neuron(neuron4_4)
neuron4_1.connect_with_neuron(neuron4_4)
neuron4_2.connect_with_neuron(neuron4_3)
neuron4_2.connect_with_neuron(neuron4_4)
neuron4_3.connect_with_neuron(neuron4_2)
neuron4_3.connect_with_neuron(neuron4_4)

# Prevent any other neurons from connecting to the remaining dendrite from neuron4_2
# This dendrite is the one activating the oscillator inside the nand gate
neuron4_2.taken_inputs[1] = 1

# Establish connections between neurons for the Flip-Flop T
neuron1_4.connect_with_neuron(neuron3_1)    # Output of nand gate 1 with input of nand gate 3
neuron2_4.connect_with_neuron(neuron4_1)    # Output of nand gate 2 with input of nand gate 4
neuron3_4.connect_with_neuron(neuron3_5)    # Delay neuron
neuron3_5.connect_with_neuron(neuron2_1)    # Output of nand gate 3 with input of nand gate 2 (Q output)
neuron3_5.connect_with_neuron(neuron4_1)    # Output of nand gate 3 with input of nand gate 2 (Q output)
neuron4_4.connect_with_neuron(neuron1_1)    # Output of nand gate 3 with input of nand gate 2 (~Q output)
neuron4_4.connect_with_neuron(neuron3_1)    # Output of nand gate 3 with input of nand gate 2 (~Q output)

# Create the neural network
brain = [neuron1_1, neuron1_2, neuron1_3, neuron1_4,
         neuron2_1, neuron2_2, neuron2_3, neuron2_4,
         neuron3_1, neuron3_2, neuron3_3, neuron3_4,
         neuron4_1, neuron4_2, neuron4_3, neuron4_4, neuron3_5]

inputs = np.zeros([sim_time,3])            #Initialize V.

# inputs[0] = T input, inputs[1] = clock signal, inputs[2] = starting signal for oscillators of each nand gate

inputs[1] = [0,0,1]

# With inputs at these times, the system does not respond properly
#inputs[500] = [1,1,0]
#inputs[610] = [1,1,0]

# There is a delay in the reponse from the system
# The human brain must have a lot of redundancy for it to work correctly
inputs[550] = [1,1,0]
inputs[660] = [1,1,0]

k=1

while k < sim_time:
    neuron_count = 0

    # Set inputs for the oscillators on each 2nd dendrite of each nand gate
    neuron1_2.inputs[1] = inputs[k][2]
    neuron2_2.inputs[1] = inputs[k][2]
    neuron3_2.inputs[1] = inputs[k][2]
    neuron4_2.inputs[1] = inputs[k][2]

    # Set inputs for nand gates 1 and 2 (neurons 1_1 and 2_1)
    neuron1_1.inputs[1] = inputs[k][0]
    neuron1_1.inputs[2] = inputs[k][1]
    neuron2_1.inputs[1] = inputs[k][0]
    neuron2_1.inputs[2] = inputs[k][1]

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

    if i == 15 or i == 16:
        plt.figure()                         #Plot the results.
        plt.plot(t,V[i])
        plt.xlabel('Time [ms]')
        plt.ylabel('Voltage [mV]')
        ax = plt.gca()
        ax.set_ylim([-40, 100])
        plt.show()
