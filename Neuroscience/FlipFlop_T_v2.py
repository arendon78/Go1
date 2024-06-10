import matplotlib.pyplot as plt
import numpy as np

# Import both Excitatory and Inhibitory Neuron models
from Excitatory_Neuron import Excitatory_Neuron
from Inhibitory_Neuron import Inhibitory_Neuron

res = 0.1                       #Set the resolution
sim_time = 2000                 #Set the simulation time
x = 29                          # number of neurons in this simulation

#Initialize V.
V = []

for i in range(x):
    V.insert(i, np.zeros([sim_time,1]))

# Initialize neurons

# 1st NAND Gate
neuron1_1 = Excitatory_Neuron(res, 3, 4)
neuron1_1.set_weights([6.5,6.5,6.5])

neuron1_2 = Excitatory_Neuron(res, 1, 1)
neuron1_2.set_weights([15])

neuron1_3 = Inhibitory_Neuron(res, 3, 1)
neuron1_3.set_weights([15,15,15])

neuron1_4 = Inhibitory_Neuron(res, 1, 1)
neuron1_4.set_weights([15])

neuron1_5 = Excitatory_Neuron(res, 2, 2)
neuron1_5.set_weights([15,15])

neuron1_6 = Excitatory_Neuron(res, 1, 2)
neuron1_6.set_weights([15])

neuron1_7 = Excitatory_Neuron(res, 4, 1)
neuron1_7.set_weights([15,15,8,8])

# Establish connections between neurons inside the nand gate
neuron1_1.connect_with_neuron(neuron1_2)
neuron1_1.connect_with_neuron(neuron1_3)
neuron1_1.connect_with_neuron(neuron1_3)
neuron1_1.connect_with_neuron(neuron1_3)
neuron1_2.connect_with_neuron(neuron1_4)
neuron1_3.connect_with_neuron(neuron1_7)
neuron1_4.connect_with_neuron(neuron1_7)
neuron1_5.connect_with_neuron(neuron1_6)
neuron1_5.connect_with_neuron(neuron1_7)
neuron1_6.connect_with_neuron(neuron1_5)
neuron1_6.connect_with_neuron(neuron1_7)

# Prevent any other neurons from connecting to the remaining dendrite from neuron1_5
# This dendrite is the one activating the oscillator inside the nand gate
neuron1_5.taken_inputs[1] = 1

# 2nd NAND Gate
neuron2_1 = Excitatory_Neuron(res, 3, 4)
neuron2_1.set_weights([6.5,6.5,6.5])

neuron2_2 = Excitatory_Neuron(res, 1, 1)
neuron2_2.set_weights([15])

neuron2_3 = Inhibitory_Neuron(res, 3, 1)
neuron2_3.set_weights([15,15,15])

neuron2_4 = Inhibitory_Neuron(res, 1, 1)
neuron2_4.set_weights([15])

neuron2_5 = Excitatory_Neuron(res, 2, 2)
neuron2_5.set_weights([15,15])

neuron2_6 = Excitatory_Neuron(res, 1, 2)
neuron2_6.set_weights([15])

neuron2_7 = Excitatory_Neuron(res, 4, 1)
neuron2_7.set_weights([15,15,8,8])

# Establish connections between neurons inside the nand gate
neuron2_1.connect_with_neuron(neuron2_2)
neuron2_1.connect_with_neuron(neuron2_3)
neuron2_1.connect_with_neuron(neuron2_3)
neuron2_1.connect_with_neuron(neuron2_3)
neuron2_2.connect_with_neuron(neuron2_4)
neuron2_3.connect_with_neuron(neuron2_7)
neuron2_4.connect_with_neuron(neuron2_7)
neuron2_5.connect_with_neuron(neuron2_6)
neuron2_5.connect_with_neuron(neuron2_7)
neuron2_6.connect_with_neuron(neuron2_5)
neuron2_6.connect_with_neuron(neuron2_7)

# Prevent any other neurons from connecting to the remaining dendrite from neuron2_5
# This dendrite is the one activating the oscillator inside the nand gate
neuron2_5.taken_inputs[1] = 1

# 3rd NAND Gate
neuron3_1 = Excitatory_Neuron(res, 2, 4)
neuron3_1.set_weights([7.5,7.5])

neuron3_2 = Excitatory_Neuron(res, 1, 1)
neuron3_2.set_weights([15])

neuron3_3 = Inhibitory_Neuron(res, 3, 1)
neuron3_3.set_weights([15,15,15])

neuron3_4 = Inhibitory_Neuron(res, 1, 1)
neuron3_4.set_weights([15])

neuron3_5 = Excitatory_Neuron(res, 2, 2)
neuron3_5.set_weights([15,15])

neuron3_6 = Excitatory_Neuron(res, 1, 2)
neuron3_6.set_weights([15])

neuron3_7 = Excitatory_Neuron(res, 4, 1)
neuron3_7.set_weights([15,15,8,8])

neuron3_8 = Excitatory_Neuron(res, 1, 1) # Neuron to provide a delay between NAND gates 3 and 4
neuron3_8.set_weights([15])

# Establish connections between neurons inside the nand gate
neuron3_1.connect_with_neuron(neuron3_2)
neuron3_1.connect_with_neuron(neuron3_3)
neuron3_1.connect_with_neuron(neuron3_3)
neuron3_1.connect_with_neuron(neuron3_3)
neuron3_2.connect_with_neuron(neuron3_4)
neuron3_3.connect_with_neuron(neuron3_7)
neuron3_4.connect_with_neuron(neuron3_7)
neuron3_5.connect_with_neuron(neuron3_6)
neuron3_5.connect_with_neuron(neuron3_7)
neuron3_6.connect_with_neuron(neuron3_5)
neuron3_6.connect_with_neuron(neuron3_7)

# Prevent any other neurons from connecting to the remaining dendrite from neuron3_5
# This dendrite is the one activating the oscillator inside the nand gate
neuron3_5.taken_inputs[1] = 1

# 4th NAND Gate
neuron4_1 = Excitatory_Neuron(res, 2, 4)
neuron4_1.set_weights([7.5,7.5])

neuron4_2 = Excitatory_Neuron(res, 1, 1)
neuron4_2.set_weights([15])

neuron4_3 = Inhibitory_Neuron(res, 3, 1)
neuron4_3.set_weights([15,15,15])

neuron4_4 = Inhibitory_Neuron(res, 1, 1)
neuron4_4.set_weights([15])

neuron4_5 = Excitatory_Neuron(res, 2, 2)
neuron4_5.set_weights([15,15])

neuron4_6 = Excitatory_Neuron(res, 1, 2)
neuron4_6.set_weights([15])

neuron4_7 = Excitatory_Neuron(res, 4, 1)
neuron4_7.set_weights([15,15,8,8])

# Establish connections between neurons inside the nand gate
neuron4_1.connect_with_neuron(neuron4_2)
neuron4_1.connect_with_neuron(neuron4_3)
neuron4_1.connect_with_neuron(neuron4_3)
neuron4_1.connect_with_neuron(neuron4_3)
neuron4_2.connect_with_neuron(neuron4_4)
neuron4_3.connect_with_neuron(neuron4_7)
neuron4_4.connect_with_neuron(neuron4_7)
neuron4_5.connect_with_neuron(neuron4_6)
neuron4_5.connect_with_neuron(neuron4_7)
neuron4_6.connect_with_neuron(neuron4_5)
neuron4_6.connect_with_neuron(neuron4_7)

# Prevent any other neurons from connecting to the remaining dendrite from neuron4_5
# This dendrite is the one activating the oscillator inside the nand gate
neuron4_5.taken_inputs[1] = 1

# Establish connections between neurons for the Flip-Flop T
neuron1_7.connect_with_neuron(neuron3_1)    # Output of nand gate 1 with input of nand gate 3
neuron2_7.connect_with_neuron(neuron4_1)    # Output of nand gate 2 with input of nand gate 4
neuron3_7.connect_with_neuron(neuron3_8)    # Delay neuron
neuron3_8.connect_with_neuron(neuron2_1)    # Output of nand gate 3 with input of nand gate 2 (Q output)
neuron3_8.connect_with_neuron(neuron4_1)    # Output of nand gate 3 with input of nand gate 2 (Q output)
neuron4_7.connect_with_neuron(neuron1_1)    # Output of nand gate 4 with input of nand gate 1 (~Q output)
neuron4_7.connect_with_neuron(neuron3_1)    # Output of nand gate 4 with input of nand gate 1 (~Q output)

# Create the neural network
brain = [neuron1_1, neuron1_2, neuron1_3, neuron1_4, neuron1_5, neuron1_6, neuron1_7,
         neuron2_1, neuron2_2, neuron2_3, neuron2_4, neuron2_5, neuron2_6, neuron2_7,
         neuron3_1, neuron3_2, neuron3_3, neuron3_4, neuron3_5, neuron3_6, neuron3_7,
         neuron4_1, neuron4_2, neuron4_3, neuron4_4,  neuron4_5, neuron4_6, neuron4_7, neuron3_8]

inputs = np.zeros([sim_time,3])            #Initialize V.

# inputs[0] = T input, inputs[1] = clock signal, inputs[2] = starting signal for oscillators of each nand gate

inputs[1] = [0,0,1]

# Needs two consecutive pulses 110 apart from each other to work
inputs[500] = [1,1,0]
inputs[610] = [1,1,0]


# There is a delay in the reponse from the system
# The human brain must have a lot of redundancy for it to work correctly

# Inhibitory neurons may be needed to block the inputs and prevent other neurons from firing
# once the desired output is obtained

#inputs[850] = [1,1,0]
#inputs[960] = [1,1,0]

k=1

while k < sim_time:
    neuron_count = 0

    # Set inputs for the oscillators on each 5th dendrite of each nand gate
    neuron1_5.inputs[1] = inputs[k][2]
    neuron2_5.inputs[1] = inputs[k][2]
    neuron3_5.inputs[1] = inputs[k][2]
    neuron4_5.inputs[1] = inputs[k][2]

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

    if i == 0 or i == 7 or i == 27 or i == 28:
        plt.figure()                         #Plot the results.
        plt.plot(t,V[i])
        plt.xlabel('Time [ms]')
        plt.ylabel('Voltage [mV]')
        ax = plt.gca()
        ax.set_ylim([-40, 100])
        plt.show()
