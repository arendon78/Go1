import matplotlib.pyplot as plt
import numpy as np
import os
import sys


project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(project_root)

# Import both Excitatory and Inhibitory Neuron models
from Neuroscience.structures.Organ import Organ
from Neuroscience.structures.Excitatory_Neuron import Excitatory_Neuron
from Neuroscience.structures.Inhibitory_Neuron import Inhibitory_Neuron

res = 0.1                       #Set the resolution
sim_time = 50000                #Set the simulation time
x = 90                          # number of neurons in this simulation

#Initialize V.
V = []

for i in range(x):
    V.insert(i, np.zeros([sim_time,1]))

# Initialize neurons

# Flip Flop T0

# 1st NAND Gate
neuronT0_1_1 = Excitatory_Neuron(res, 3, 4)
neuronT0_1_1.set_weights([6.5,6.5,6.5])

neuronT0_1_2 = Excitatory_Neuron(res, 1, 1)
neuronT0_1_2.set_weights([15])

neuronT0_1_3 = Inhibitory_Neuron(res, 3, 1)
neuronT0_1_3.set_weights([15,15,15])

neuronT0_1_4 = Inhibitory_Neuron(res, 1, 1)
neuronT0_1_4.set_weights([15])

neuronT0_1_5 = Excitatory_Neuron(res, 2, 2)
neuronT0_1_5.set_weights([15,15])

neuronT0_1_6 = Excitatory_Neuron(res, 1, 2)
neuronT0_1_6.set_weights([15])

neuronT0_1_7 = Excitatory_Neuron(res, 4, 1)
neuronT0_1_7.set_weights([15,15,8,8])

# Establish connections between neurons inside the nand gate
neuronT0_1_1.connect_with_neuron(neuronT0_1_2)
neuronT0_1_1.connect_with_neuron(neuronT0_1_3)
neuronT0_1_1.connect_with_neuron(neuronT0_1_3)
neuronT0_1_1.connect_with_neuron(neuronT0_1_3)
neuronT0_1_2.connect_with_neuron(neuronT0_1_4)
neuronT0_1_3.connect_with_neuron(neuronT0_1_7)
neuronT0_1_4.connect_with_neuron(neuronT0_1_7)
neuronT0_1_5.connect_with_neuron(neuronT0_1_6)
neuronT0_1_5.connect_with_neuron(neuronT0_1_7)
neuronT0_1_6.connect_with_neuron(neuronT0_1_5)
neuronT0_1_6.connect_with_neuron(neuronT0_1_7)

# Prevent any other neurons from connecting to the remaining dendrite from neuronT0_1_5
# This dendrite is the one activating the oscillator inside the nand gate
neuronT0_1_5.taken_inputs[1] = 1

# 2nd NAND Gate
neuronT0_2_1 = Excitatory_Neuron(res, 3, 4)
neuronT0_2_1.set_weights([6.5,6.5,6.5])

neuronT0_2_2 = Excitatory_Neuron(res, 1, 1)
neuronT0_2_2.set_weights([15])

neuronT0_2_3 = Inhibitory_Neuron(res, 3, 1)
neuronT0_2_3.set_weights([15,15,15])

neuronT0_2_4 = Inhibitory_Neuron(res, 1, 1)
neuronT0_2_4.set_weights([15])

neuronT0_2_5 = Excitatory_Neuron(res, 2, 2)
neuronT0_2_5.set_weights([15,15])

neuronT0_2_6 = Excitatory_Neuron(res, 1, 2)
neuronT0_2_6.set_weights([15])

neuronT0_2_7 = Excitatory_Neuron(res, 4, 1)
neuronT0_2_7.set_weights([15,15,8,8])

# Establish connections between neurons inside the nand gate
neuronT0_2_1.connect_with_neuron(neuronT0_2_2)
neuronT0_2_1.connect_with_neuron(neuronT0_2_3)
neuronT0_2_1.connect_with_neuron(neuronT0_2_3)
neuronT0_2_1.connect_with_neuron(neuronT0_2_3)
neuronT0_2_2.connect_with_neuron(neuronT0_2_4)
neuronT0_2_3.connect_with_neuron(neuronT0_2_7)
neuronT0_2_4.connect_with_neuron(neuronT0_2_7)
neuronT0_2_5.connect_with_neuron(neuronT0_2_6)
neuronT0_2_5.connect_with_neuron(neuronT0_2_7)
neuronT0_2_6.connect_with_neuron(neuronT0_2_5)
neuronT0_2_6.connect_with_neuron(neuronT0_2_7)

# Prevent any other neurons from connecting to the remaining dendrite from neuronT0_2_5
# This dendrite is the one activating the oscillator inside the nand gate
neuronT0_2_5.taken_inputs[1] = 1

# 3rd NAND Gate
neuronT0_3_1 = Excitatory_Neuron(res, 2, 4)
neuronT0_3_1.set_weights([7.5,7.5])

neuronT0_3_2 = Excitatory_Neuron(res, 1, 1)
neuronT0_3_2.set_weights([15])

neuronT0_3_3 = Inhibitory_Neuron(res, 3, 1)
neuronT0_3_3.set_weights([15,15,15])

neuronT0_3_4 = Inhibitory_Neuron(res, 1, 1)
neuronT0_3_4.set_weights([15])

neuronT0_3_5 = Excitatory_Neuron(res, 2, 2)
neuronT0_3_5.set_weights([15,15])

neuronT0_3_6 = Excitatory_Neuron(res, 1, 2)
neuronT0_3_6.set_weights([15])

neuronT0_3_7 = Excitatory_Neuron(res, 4, 1)
neuronT0_3_7.set_weights([15,15,8,8])

# This neuron needs extra outputs because it'll be connected to 
# the input of Flip Flop T1 and to the AND gate of the counter
neuronT0_3_8 = Excitatory_Neuron(res, 1, 4) # Neuron to provide a delay between NAND gates 3 and 4
neuronT0_3_8.set_weights([15])

# Establish connections between neurons inside the nand gate
neuronT0_3_1.connect_with_neuron(neuronT0_3_2)
neuronT0_3_1.connect_with_neuron(neuronT0_3_3)
neuronT0_3_1.connect_with_neuron(neuronT0_3_3)
neuronT0_3_1.connect_with_neuron(neuronT0_3_3)
neuronT0_3_2.connect_with_neuron(neuronT0_3_4)
neuronT0_3_3.connect_with_neuron(neuronT0_3_7)
neuronT0_3_4.connect_with_neuron(neuronT0_3_7)
neuronT0_3_5.connect_with_neuron(neuronT0_3_6)
neuronT0_3_5.connect_with_neuron(neuronT0_3_7)
neuronT0_3_6.connect_with_neuron(neuronT0_3_5)
neuronT0_3_6.connect_with_neuron(neuronT0_3_7)

# Prevent any other neurons from connecting to the remaining dendrite from neuronT0_3_5
# This dendrite is the one activating the oscillator inside the nand gate
neuronT0_3_5.taken_inputs[1] = 1

# 4th NAND Gate
neuronT0_4_1 = Excitatory_Neuron(res, 2, 4)
neuronT0_4_1.set_weights([7.5,7.5])

neuronT0_4_2 = Excitatory_Neuron(res, 1, 1)
neuronT0_4_2.set_weights([15])

neuronT0_4_3 = Inhibitory_Neuron(res, 3, 1)
neuronT0_4_3.set_weights([15,15,15])

neuronT0_4_4 = Inhibitory_Neuron(res, 1, 1)
neuronT0_4_4.set_weights([15])

neuronT0_4_5 = Excitatory_Neuron(res, 2, 2)
neuronT0_4_5.set_weights([15,15])

neuronT0_4_6 = Excitatory_Neuron(res, 1, 2)
neuronT0_4_6.set_weights([15])

neuronT0_4_7 = Excitatory_Neuron(res, 4, 1)
neuronT0_4_7.set_weights([15,15,8,8])

# Establish connections between neurons inside the nand gate
neuronT0_4_1.connect_with_neuron(neuronT0_4_2)
neuronT0_4_1.connect_with_neuron(neuronT0_4_3)
neuronT0_4_1.connect_with_neuron(neuronT0_4_3)
neuronT0_4_1.connect_with_neuron(neuronT0_4_3)
neuronT0_4_2.connect_with_neuron(neuronT0_4_4)
neuronT0_4_3.connect_with_neuron(neuronT0_4_7)
neuronT0_4_4.connect_with_neuron(neuronT0_4_7)
neuronT0_4_5.connect_with_neuron(neuronT0_4_6)
neuronT0_4_5.connect_with_neuron(neuronT0_4_7)
neuronT0_4_6.connect_with_neuron(neuronT0_4_5)
neuronT0_4_6.connect_with_neuron(neuronT0_4_7)

# Prevent any other neurons from connecting to the remaining dendrite from neuronT0_4_5
# This dendrite is the one activating the oscillator inside the nand gate
neuronT0_4_5.taken_inputs[1] = 1

# Establish connections between neurons for the Flip-Flop T
neuronT0_1_7.connect_with_neuron(neuronT0_3_1)    # Output of nand gate 1 with input of nand gate 3
neuronT0_2_7.connect_with_neuron(neuronT0_4_1)    # Output of nand gate 2 with input of nand gate 4
neuronT0_3_7.connect_with_neuron(neuronT0_3_8)    # Delay neuron
neuronT0_3_8.connect_with_neuron(neuronT0_2_1)    # Output of nand gate 3 with input of nand gate 2 (Q output)
neuronT0_3_8.connect_with_neuron(neuronT0_4_1)    # Output of nand gate 3 with input of nand gate 2 (Q output)
neuronT0_4_7.connect_with_neuron(neuronT0_1_1)    # Output of nand gate 4 with input of nand gate 1 (~Q output)
neuronT0_4_7.connect_with_neuron(neuronT0_3_1)    # Output of nand gate 4 with input of nand gate 1 (~Q output)

# Flip Flop T1

# 1st NAND Gate
neuronT1_1_1 = Excitatory_Neuron(res, 3, 4)
neuronT1_1_1.set_weights([6.5,6.5,6.5])

neuronT1_1_2 = Excitatory_Neuron(res, 1, 1)
neuronT1_1_2.set_weights([15])

neuronT1_1_3 = Inhibitory_Neuron(res, 3, 1)
neuronT1_1_3.set_weights([15,15,15])

neuronT1_1_4 = Inhibitory_Neuron(res, 1, 1)
neuronT1_1_4.set_weights([15])

neuronT1_1_5 = Excitatory_Neuron(res, 2, 2)
neuronT1_1_5.set_weights([15,15])

neuronT1_1_6 = Excitatory_Neuron(res, 1, 2)
neuronT1_1_6.set_weights([15])

neuronT1_1_7 = Excitatory_Neuron(res, 4, 1)
neuronT1_1_7.set_weights([15,15,8,8])

# Establish connections between neurons inside the nand gate
neuronT1_1_1.connect_with_neuron(neuronT1_1_2)
neuronT1_1_1.connect_with_neuron(neuronT1_1_3)
neuronT1_1_1.connect_with_neuron(neuronT1_1_3)
neuronT1_1_1.connect_with_neuron(neuronT1_1_3)
neuronT1_1_2.connect_with_neuron(neuronT1_1_4)
neuronT1_1_3.connect_with_neuron(neuronT1_1_7)
neuronT1_1_4.connect_with_neuron(neuronT1_1_7)
neuronT1_1_5.connect_with_neuron(neuronT1_1_6)
neuronT1_1_5.connect_with_neuron(neuronT1_1_7)
neuronT1_1_6.connect_with_neuron(neuronT1_1_5)
neuronT1_1_6.connect_with_neuron(neuronT1_1_7)

# Prevent any other neurons from connecting to the remaining dendrite from neuronT1_1_5
# This dendrite is the one activating the oscillator inside the nand gate
neuronT1_1_5.taken_inputs[1] = 1

# 2nd NAND Gate
neuronT1_2_1 = Excitatory_Neuron(res, 3, 4)
neuronT1_2_1.set_weights([6.5,6.5,6.5])

neuronT1_2_2 = Excitatory_Neuron(res, 1, 1)
neuronT1_2_2.set_weights([15])

neuronT1_2_3 = Inhibitory_Neuron(res, 3, 1)
neuronT1_2_3.set_weights([15,15,15])

neuronT1_2_4 = Inhibitory_Neuron(res, 1, 1)
neuronT1_2_4.set_weights([15])

neuronT1_2_5 = Excitatory_Neuron(res, 2, 2)
neuronT1_2_5.set_weights([15,15])

neuronT1_2_6 = Excitatory_Neuron(res, 1, 2)
neuronT1_2_6.set_weights([15])

neuronT1_2_7 = Excitatory_Neuron(res, 4, 1)
neuronT1_2_7.set_weights([15,15,8,8])

# Establish connections between neurons inside the nand gate
neuronT1_2_1.connect_with_neuron(neuronT1_2_2)
neuronT1_2_1.connect_with_neuron(neuronT1_2_3)
neuronT1_2_1.connect_with_neuron(neuronT1_2_3)
neuronT1_2_1.connect_with_neuron(neuronT1_2_3)
neuronT1_2_2.connect_with_neuron(neuronT1_2_4)
neuronT1_2_3.connect_with_neuron(neuronT1_2_7)
neuronT1_2_4.connect_with_neuron(neuronT1_2_7)
neuronT1_2_5.connect_with_neuron(neuronT1_2_6)
neuronT1_2_5.connect_with_neuron(neuronT1_2_7)
neuronT1_2_6.connect_with_neuron(neuronT1_2_5)
neuronT1_2_6.connect_with_neuron(neuronT1_2_7)

# Prevent any other neurons from connecting to the remaining dendrite from neuronT1_2_5
# This dendrite is the one activating the oscillator inside the nand gate
neuronT1_2_5.taken_inputs[1] = 1

# 3rd NAND Gate
neuronT1_3_1 = Excitatory_Neuron(res, 2, 4)
neuronT1_3_1.set_weights([7.5,7.5])

neuronT1_3_2 = Excitatory_Neuron(res, 1, 1)
neuronT1_3_2.set_weights([15])

neuronT1_3_3 = Inhibitory_Neuron(res, 3, 1)
neuronT1_3_3.set_weights([15,15,15])

neuronT1_3_4 = Inhibitory_Neuron(res, 1, 1)
neuronT1_3_4.set_weights([15])

neuronT1_3_5 = Excitatory_Neuron(res, 2, 2)
neuronT1_3_5.set_weights([15,15])

neuronT1_3_6 = Excitatory_Neuron(res, 1, 2)
neuronT1_3_6.set_weights([15])

neuronT1_3_7 = Excitatory_Neuron(res, 4, 1)
neuronT1_3_7.set_weights([15,15,8,8])

# This neuron needs extra outputs because it'll be connected to 
# the AND gate of the counter
neuronT1_3_8 = Excitatory_Neuron(res, 1, 2) # Neuron to provide a delay between NAND gates 3 and 4
neuronT1_3_8.set_weights([15])

# Establish connections between neurons inside the nand gate
neuronT1_3_1.connect_with_neuron(neuronT1_3_2)
neuronT1_3_1.connect_with_neuron(neuronT1_3_3)
neuronT1_3_1.connect_with_neuron(neuronT1_3_3)
neuronT1_3_1.connect_with_neuron(neuronT1_3_3)
neuronT1_3_2.connect_with_neuron(neuronT1_3_4)
neuronT1_3_3.connect_with_neuron(neuronT1_3_7)
neuronT1_3_4.connect_with_neuron(neuronT1_3_7)
neuronT1_3_5.connect_with_neuron(neuronT1_3_6)
neuronT1_3_5.connect_with_neuron(neuronT1_3_7)
neuronT1_3_6.connect_with_neuron(neuronT1_3_5)
neuronT1_3_6.connect_with_neuron(neuronT1_3_7)

# Prevent any other neurons from connecting to the remaining dendrite from neuronT1_3_5
# This dendrite is the one activating the oscillator inside the nand gate
neuronT1_3_5.taken_inputs[1] = 1

# 4th NAND Gate
neuronT1_4_1 = Excitatory_Neuron(res, 2, 4)
neuronT1_4_1.set_weights([7.5,7.5])

neuronT1_4_2 = Excitatory_Neuron(res, 1, 1)
neuronT1_4_2.set_weights([15])

neuronT1_4_3 = Inhibitory_Neuron(res, 3, 1)
neuronT1_4_3.set_weights([15,15,15])

neuronT1_4_4 = Inhibitory_Neuron(res, 1, 1)
neuronT1_4_4.set_weights([15])

neuronT1_4_5 = Excitatory_Neuron(res, 2, 2)
neuronT1_4_5.set_weights([15,15])

neuronT1_4_6 = Excitatory_Neuron(res, 1, 2)
neuronT1_4_6.set_weights([15])

neuronT1_4_7 = Excitatory_Neuron(res, 4, 1)
neuronT1_4_7.set_weights([15,15,8,8])

# Establish connections between neurons inside the nand gate
neuronT1_4_1.connect_with_neuron(neuronT1_4_2)
neuronT1_4_1.connect_with_neuron(neuronT1_4_3)
neuronT1_4_1.connect_with_neuron(neuronT1_4_3)
neuronT1_4_1.connect_with_neuron(neuronT1_4_3)
neuronT1_4_2.connect_with_neuron(neuronT1_4_4)
neuronT1_4_3.connect_with_neuron(neuronT1_4_7)
neuronT1_4_4.connect_with_neuron(neuronT1_4_7)
neuronT1_4_5.connect_with_neuron(neuronT1_4_6)
neuronT1_4_5.connect_with_neuron(neuronT1_4_7)
neuronT1_4_6.connect_with_neuron(neuronT1_4_5)
neuronT1_4_6.connect_with_neuron(neuronT1_4_7)

# Prevent any other neurons from connecting to the remaining dendrite from neuronT1_4_5
# This dendrite is the one activating the oscillator inside the nand gate
neuronT1_4_5.taken_inputs[1] = 1

# Establish connections between neurons for the Flip-Flop T
neuronT1_1_7.connect_with_neuron(neuronT1_3_1)    # Output of nand gate 1 with input of nand gate 3
neuronT1_2_7.connect_with_neuron(neuronT1_4_1)    # Output of nand gate 2 with input of nand gate 4
neuronT1_3_7.connect_with_neuron(neuronT1_3_8)    # Delay neuron
neuronT1_3_8.connect_with_neuron(neuronT1_2_1)    # Output of nand gate 3 with input of nand gate 2 (Q output)
neuronT1_3_8.connect_with_neuron(neuronT1_4_1)    # Output of nand gate 3 with input of nand gate 2 (Q output)
neuronT1_4_7.connect_with_neuron(neuronT1_1_1)    # Output of nand gate 4 with input of nand gate 1 (~Q output)
neuronT1_4_7.connect_with_neuron(neuronT1_3_1)    # Output of nand gate 4 with input of nand gate 1 (~Q output)

# Flip Flop T2

# 1st NAND Gate
neuronT2_1_1 = Excitatory_Neuron(res, 3, 4)
neuronT2_1_1.set_weights([6.5,6.5,6.5])

neuronT2_1_2 = Excitatory_Neuron(res, 1, 1)
neuronT2_1_2.set_weights([15])

neuronT2_1_3 = Inhibitory_Neuron(res, 3, 1)
neuronT2_1_3.set_weights([15,15,15])

neuronT2_1_4 = Inhibitory_Neuron(res, 1, 1)
neuronT2_1_4.set_weights([15])

neuronT2_1_5 = Excitatory_Neuron(res, 2, 2)
neuronT2_1_5.set_weights([15,15])

neuronT2_1_6 = Excitatory_Neuron(res, 1, 2)
neuronT2_1_6.set_weights([15])

neuronT2_1_7 = Excitatory_Neuron(res, 4, 1)
neuronT2_1_7.set_weights([15,15,8,8])

# Establish connections between neurons inside the nand gate
neuronT2_1_1.connect_with_neuron(neuronT2_1_2)
neuronT2_1_1.connect_with_neuron(neuronT2_1_3)
neuronT2_1_1.connect_with_neuron(neuronT2_1_3)
neuronT2_1_1.connect_with_neuron(neuronT2_1_3)
neuronT2_1_2.connect_with_neuron(neuronT2_1_4)
neuronT2_1_3.connect_with_neuron(neuronT2_1_7)
neuronT2_1_4.connect_with_neuron(neuronT2_1_7)
neuronT2_1_5.connect_with_neuron(neuronT2_1_6)
neuronT2_1_5.connect_with_neuron(neuronT2_1_7)
neuronT2_1_6.connect_with_neuron(neuronT2_1_5)
neuronT2_1_6.connect_with_neuron(neuronT2_1_7)

# Prevent any other neurons from connecting to the remaining dendrite from neuronT2_1_5
# This dendrite is the one activating the oscillator inside the nand gate
neuronT2_1_5.taken_inputs[1] = 1

# 2nd NAND Gate
neuronT2_2_1 = Excitatory_Neuron(res, 3, 4)
neuronT2_2_1.set_weights([6.5,6.5,6.5])

neuronT2_2_2 = Excitatory_Neuron(res, 1, 1)
neuronT2_2_2.set_weights([15])

neuronT2_2_3 = Inhibitory_Neuron(res, 3, 1)
neuronT2_2_3.set_weights([15,15,15])

neuronT2_2_4 = Inhibitory_Neuron(res, 1, 1)
neuronT2_2_4.set_weights([15])

neuronT2_2_5 = Excitatory_Neuron(res, 2, 2)
neuronT2_2_5.set_weights([15,15])

neuronT2_2_6 = Excitatory_Neuron(res, 1, 2)
neuronT2_2_6.set_weights([15])

neuronT2_2_7 = Excitatory_Neuron(res, 4, 1)
neuronT2_2_7.set_weights([15,15,8,8])

# Establish connections between neurons inside the nand gate
neuronT2_2_1.connect_with_neuron(neuronT2_2_2)
neuronT2_2_1.connect_with_neuron(neuronT2_2_3)
neuronT2_2_1.connect_with_neuron(neuronT2_2_3)
neuronT2_2_1.connect_with_neuron(neuronT2_2_3)
neuronT2_2_2.connect_with_neuron(neuronT2_2_4)
neuronT2_2_3.connect_with_neuron(neuronT2_2_7)
neuronT2_2_4.connect_with_neuron(neuronT2_2_7)
neuronT2_2_5.connect_with_neuron(neuronT2_2_6)
neuronT2_2_5.connect_with_neuron(neuronT2_2_7)
neuronT2_2_6.connect_with_neuron(neuronT2_2_5)
neuronT2_2_6.connect_with_neuron(neuronT2_2_7)

# Prevent any other neurons from connecting to the remaining dendrite from neuronT2_2_5
# This dendrite is the one activating the oscillator inside the nand gate
neuronT2_2_5.taken_inputs[1] = 1

# 3rd NAND Gate
neuronT2_3_1 = Excitatory_Neuron(res, 2, 4)
neuronT2_3_1.set_weights([7.5,7.5])

neuronT2_3_2 = Excitatory_Neuron(res, 1, 1)
neuronT2_3_2.set_weights([15])

neuronT2_3_3 = Inhibitory_Neuron(res, 3, 1)
neuronT2_3_3.set_weights([15,15,15])

neuronT2_3_4 = Inhibitory_Neuron(res, 1, 1)
neuronT2_3_4.set_weights([15])

neuronT2_3_5 = Excitatory_Neuron(res, 2, 2)
neuronT2_3_5.set_weights([15,15])

neuronT2_3_6 = Excitatory_Neuron(res, 1, 2)
neuronT2_3_6.set_weights([15])

neuronT2_3_7 = Excitatory_Neuron(res, 4, 1)
neuronT2_3_7.set_weights([15,15,8,8])

neuronT2_3_8 = Excitatory_Neuron(res, 1, 1) # Neuron to provide a delay between NAND gates 3 and 4
neuronT2_3_8.set_weights([15])

# Establish connections between neurons inside the nand gate
neuronT2_3_1.connect_with_neuron(neuronT2_3_2)
neuronT2_3_1.connect_with_neuron(neuronT2_3_3)
neuronT2_3_1.connect_with_neuron(neuronT2_3_3)
neuronT2_3_1.connect_with_neuron(neuronT2_3_3)
neuronT2_3_2.connect_with_neuron(neuronT2_3_4)
neuronT2_3_3.connect_with_neuron(neuronT2_3_7)
neuronT2_3_4.connect_with_neuron(neuronT2_3_7)
neuronT2_3_5.connect_with_neuron(neuronT2_3_6)
neuronT2_3_5.connect_with_neuron(neuronT2_3_7)
neuronT2_3_6.connect_with_neuron(neuronT2_3_5)
neuronT2_3_6.connect_with_neuron(neuronT2_3_7)

# Prevent any other neurons from connecting to the remaining dendrite from neuronT2_3_5
# This dendrite is the one activating the oscillator inside the nand gate
neuronT2_3_5.taken_inputs[1] = 1

# 4th NAND Gate
neuronT2_4_1 = Excitatory_Neuron(res, 2, 4)
neuronT2_4_1.set_weights([7.5,7.5])

neuronT2_4_2 = Excitatory_Neuron(res, 1, 1)
neuronT2_4_2.set_weights([15])

neuronT2_4_3 = Inhibitory_Neuron(res, 3, 1)
neuronT2_4_3.set_weights([15,15,15])

neuronT2_4_4 = Inhibitory_Neuron(res, 1, 1)
neuronT2_4_4.set_weights([15])

neuronT2_4_5 = Excitatory_Neuron(res, 2, 2)
neuronT2_4_5.set_weights([15,15])

neuronT2_4_6 = Excitatory_Neuron(res, 1, 2)
neuronT2_4_6.set_weights([15])

neuronT2_4_7 = Excitatory_Neuron(res, 4, 1)
neuronT2_4_7.set_weights([15,15,8,8])

# Establish connections between neurons inside the nand gate
neuronT2_4_1.connect_with_neuron(neuronT2_4_2)
neuronT2_4_1.connect_with_neuron(neuronT2_4_3)
neuronT2_4_1.connect_with_neuron(neuronT2_4_3)
neuronT2_4_1.connect_with_neuron(neuronT2_4_3)
neuronT2_4_2.connect_with_neuron(neuronT2_4_4)
neuronT2_4_3.connect_with_neuron(neuronT2_4_7)
neuronT2_4_4.connect_with_neuron(neuronT2_4_7)
neuronT2_4_5.connect_with_neuron(neuronT2_4_6)
neuronT2_4_5.connect_with_neuron(neuronT2_4_7)
neuronT2_4_6.connect_with_neuron(neuronT2_4_5)
neuronT2_4_6.connect_with_neuron(neuronT2_4_7)

# Prevent any other neurons from connecting to the remaining dendrite from neuronT2_4_5
# This dendrite is the one activating the oscillator inside the nand gate
neuronT2_4_5.taken_inputs[1] = 1

# Establish connections between neurons for the Flip-Flop T
neuronT2_1_7.connect_with_neuron(neuronT2_3_1)    # Output of nand gate 1 with input of nand gate 3
neuronT2_2_7.connect_with_neuron(neuronT2_4_1)    # Output of nand gate 2 with input of nand gate 4
neuronT2_3_7.connect_with_neuron(neuronT2_3_8)    # Delay neuron
neuronT2_3_8.connect_with_neuron(neuronT2_2_1)    # Output of nand gate 3 with input of nand gate 2 (Q output)
neuronT2_3_8.connect_with_neuron(neuronT2_4_1)    # Output of nand gate 3 with input of nand gate 2 (Q output)
neuronT2_4_7.connect_with_neuron(neuronT2_1_1)    # Output of nand gate 4 with input of nand gate 1 (~Q output)
neuronT2_4_7.connect_with_neuron(neuronT2_3_1)    # Output of nand gate 4 with input of nand gate 1 (~Q output)

# Neurons for the counter

# Neurons for providing a constant train of pulses
neuronC_1 = Excitatory_Neuron(res, 2, 3)
neuronC_1.set_weights([15,15])

neuronC_2 = Excitatory_Neuron(res, 1, 1)
neuronC_2.set_weights([15])

# Neuron for the AND gate inside the counter
neuronC_3 = Excitatory_Neuron(res, 2, 2)
neuronC_3.set_weights([8,8])

#neuronC_4 = Excitatory_Neuron(res, 1, 1)
#neuronC_4.set_weights([15])

#neuronC_5 = Excitatory_Neuron(res, 2, 2)
#neuronC_5.set_weights([15,15])

# Connections between neurons for the Counter

# The inputs for the counter's AND gate are Q0 and Q1
# (Flip Flops T0 and T1 respectively)
neuronT0_3_8.connect_with_neuron(neuronC_3)
neuronT1_3_8.connect_with_neuron(neuronC_3)

# This connections are so that neuronC_5 can provide 2 pulses to Flip Flop T2
#neuronC_3.connect_with_neuron(neuronC_4)
#neuronC_3.connect_with_neuron(neuronC_5)
#neuronC_4.connect_with_neuron(neuronC_5)

# The output of the counter's AND gate is the input for Flip Flop T2
neuronC_3.connect_with_neuron(neuronT2_1_1)
neuronC_3.connect_with_neuron(neuronT2_2_1)

# Input for Flip Flop T1
neuronT0_3_8.connect_with_neuron(neuronT1_1_1)
neuronT0_3_8.connect_with_neuron(neuronT1_2_1)

# Neurons providing a train of pulses to Flip Flop T0 (logic 1)
neuronC_1.connect_with_neuron(neuronT0_1_1)
neuronC_1.connect_with_neuron(neuronT0_2_1)
neuronC_1.connect_with_neuron(neuronC_2)
neuronC_2.connect_with_neuron(neuronC_1)

# Prevent any other neurons from connecting to the remaining dendrite from neuronC_1
# This dendrite is the one activating the oscillator providing a constant train 
# of pulses for Flip Flop T0
neuronC_1.taken_inputs[1] = 1

# Create the neural network
brain = [neuronT2_1_1, neuronT2_1_2, neuronT2_1_3, neuronT2_1_4, neuronT2_1_5, neuronT2_1_6, neuronT2_1_7,
         neuronT2_2_1, neuronT2_2_2, neuronT2_2_3, neuronT2_2_4, neuronT2_2_5, neuronT2_2_6, neuronT2_2_7,
         neuronT2_3_1, neuronT2_3_2, neuronT2_3_3, neuronT2_3_4, neuronT2_3_5, neuronT2_3_6, neuronT2_3_7,
         neuronT2_4_1, neuronT2_4_2, neuronT2_4_3, neuronT2_4_4, neuronT2_4_5, neuronT2_4_6, neuronT2_4_7, neuronT2_3_8,
         neuronT1_1_1, neuronT1_1_2, neuronT1_1_3, neuronT1_1_4, neuronT1_1_5, neuronT1_1_6, neuronT1_1_7,
         neuronT1_2_1, neuronT1_2_2, neuronT1_2_3, neuronT1_2_4, neuronT1_2_5, neuronT1_2_6, neuronT1_2_7,
         neuronT1_3_1, neuronT1_3_2, neuronT1_3_3, neuronT1_3_4, neuronT1_3_5, neuronT1_3_6, neuronT1_3_7,
         neuronT1_4_1, neuronT1_4_2, neuronT1_4_3, neuronT1_4_4, neuronT1_4_5, neuronT1_4_6, neuronT1_4_7, neuronT1_3_8,
         neuronT0_1_1, neuronT0_1_2, neuronT0_1_3, neuronT0_1_4, neuronT0_1_5, neuronT0_1_6, neuronT0_1_7,
         neuronT0_2_1, neuronT0_2_2, neuronT0_2_3, neuronT0_2_4, neuronT0_2_5, neuronT0_2_6, neuronT0_2_7,
         neuronT0_3_1, neuronT0_3_2, neuronT0_3_3, neuronT0_3_4, neuronT0_3_5, neuronT0_3_6, neuronT0_3_7,
         neuronT0_4_1, neuronT0_4_2, neuronT0_4_3, neuronT0_4_4, neuronT0_4_5, neuronT0_4_6, neuronT0_4_7, neuronT0_3_8,
         neuronC_1, neuronC_2, neuronC_3]

inputs = np.zeros([sim_time,2])            #Initialize V.

# inputs[0] = T input, inputs[1] = clock signal, inputs[2] = starting signal for oscillators of each nand gate

inputs[1] = [0,1]

# Needs two consecutive pulses 110 apart from each other to work
# inputs[700] = [1,0]
# inputs[810] = [1,0]
# inputs[1700] = [1,0]
# inputs[1810] = [1,0]
# inputs[2700] = [1,0]
# inputs[2810] = [1,0]
# inputs[3700] = [1,0]
# inputs[3810] = [1,0]
# inputs[4700] = [1,0]
# inputs[4810] = [1,0]
# inputs[5700] = [1,0]
# inputs[5810] = [1,0]
# inputs[6700] = [1,0]
# inputs[6810] = [1,0]
# inputs[7700] = [1,0]
# inputs[7810] = [1,0]
# inputs[8700] = [1,0]
# inputs[8810] = [1,0]
# inputs[9700] = [1,0]
# inputs[9810] = [1,0]

for i in range(sim_time): 
    if i %1000 == 700 or i%1000 == 810 : 
        inputs[i] = [1,0]

# Inhibitory neurons may be needed to block the inputs and prevent other neurons from firing
# once the desired output is obtained

k=1

while k < sim_time:
    neuron_count = 0

    # Set inputs for the oscillators on each 5th dendrite of each nand gate
    # and for neuronC1
    neuronT0_1_5.inputs[1] = inputs[k][1]
    neuronT0_2_5.inputs[1] = inputs[k][1]
    neuronT0_3_5.inputs[1] = inputs[k][1]
    neuronT0_4_5.inputs[1] = inputs[k][1]
    neuronT1_1_5.inputs[1] = inputs[k][1]
    neuronT1_2_5.inputs[1] = inputs[k][1]
    neuronT1_3_5.inputs[1] = inputs[k][1]
    neuronT1_4_5.inputs[1] = inputs[k][1]
    neuronT2_1_5.inputs[1] = inputs[k][1]
    neuronT2_2_5.inputs[1] = inputs[k][1]
    neuronT2_3_5.inputs[1] = inputs[k][1]
    neuronT2_4_5.inputs[1] = inputs[k][1]
    neuronC_1.inputs[1] = inputs[k][1]

    # Set inputs (clock signal only) for flip flops (neurons TX_1_1 and TX_2_1)
    neuronT0_1_1.inputs[2] = inputs[k][0]
    neuronT0_2_1.inputs[2] = inputs[k][0]
    neuronT1_1_1.inputs[2] = inputs[k][0]
    neuronT1_2_1.inputs[2] = inputs[k][0]
    neuronT2_1_1.inputs[2] = inputs[k][0]
    neuronT2_2_1.inputs[2] = inputs[k][0]

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

    if i == 28 or i == 57 or i == 86 or i == 89:
#    if i == 4 or i == 11 or i == 18 or i == 25: # oscillators for flip flop T2
#    if i == 33 or i == 40 or i == 47 or i == 54: # oscillators for flip flop T1
#    if i == 62 or i == 69 or i == 76 or i == 83: # oscillators for flip flop T0
        plt.figure()                         #Plot the results.
        plt.plot(t,V[i])
        plt.xlabel('Time [ms]')
        plt.ylabel('Voltage [mV]')
        ax = plt.gca()
        ax.set_ylim([-40, 100])
        plt.show()

print([el.name for el in brain])

o = Organ()
for neuron in brain:
    o.add_to_brain(neuron)

o.build_and_display_neuron_graph()
