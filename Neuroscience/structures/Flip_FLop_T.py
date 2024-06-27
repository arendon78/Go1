import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(project_root)

from Neuroscience.structures.Gate_NAND import Gate_NAND
from Neuroscience.structures.Excitatory_Neuron import Excitatory_Neuron
from Neuroscience.structures.Inhibitory_Neuron import Inhibitory_Neuron
from Neuroscience.structures.Organ import Organ

import numpy as np

class Flip_Flop_T(Organ) : 

    def print(self):
        for n in self.brain : 
            n.print()
            print("")

    def pass_inputs_oscillators(self, inputs, k):
        # Set inputs for the oscillators on each 5th dendrite of each NAND gate
        self.fst_NAND.brain[4].inputs[1] = inputs[k][1]  # neuron1_5.inputs[1]
        self.scd_NAND.brain[4].inputs[1] = inputs[k][1]  # neuron2_5.inputs[1]
        self.thrd_NAND.brain[4].inputs[1] = inputs[k][1] # neuron3_5.inputs[1]
        self.fth_NAND.brain[4].inputs[1] = inputs[k][1]  # neuron4_5.inputs[1]

    def pass_inputs_selfputs(self,inputs,k):
        # Set selfputs for NAND gates 1 and 2 (neurons 1_1 and 2_1)
        self.fst_NAND.brain[0].inputs[2] = inputs[k][0]  # neuron1_1.inputs[2]
        self.scd_NAND.brain[0].inputs[2] = inputs[k][0]  # neuron2_1.inputs[2]

    def pass_inputs(self,inputs,k): 
        self.pass_inputs_oscillators(inputs,k)
        # Set selfputs for NAND gates 1 and 2 (neurons 1_1 and 2_1)
        self.pass_inputs_selfputs(inputs,k)

    def __init__(self,res): 

        super().__init__()

    #1st NAND Gate -----------------------

        n1_0 = Excitatory_Neuron(res, 3, 4, name = "n1_0")
        n1_0.set_weights([6.5,6.5,6.5])
        n1_1 = Excitatory_Neuron(res, 1, 1,  name = "n1_1")
        n1_1.set_weights([15])
        n1_2 = Inhibitory_Neuron(res, 3, 1,  name = "n1_2")
        n1_2.set_weights([15,15,15])
        n1_3 = Inhibitory_Neuron(res, 1, 1,  name = "n1_3")
        n1_3.set_weights([15])
        n1_4 = Excitatory_Neuron(res, 2, 2,  name = "n1_4")
        n1_4.set_weights([15,15])
        n1_5 = Excitatory_Neuron(res, 1, 2,  name = "n1_5")
        n1_5.set_weights([15])
        n1_6 = Excitatory_Neuron(res, 4, 1,  name = "n1_6")
        n1_6.set_weights([15,15,8,8])
        
        self.fst_NAND = Gate_NAND(n1_0,n1_1,n1_2,n1_3,n1_4,n1_5,n1_6,res = res)
        
    #2nd NAND Gate -----------------------

        n2_0 = Excitatory_Neuron(res, 3, 4, name = "n2_0")
        n2_0.set_weights([6.5,6.5,6.5])
        n2_1 = Excitatory_Neuron(res, 1, 1,  name = "n2_1")
        n2_1.set_weights([15])
        n2_2 = Inhibitory_Neuron(res, 3, 1,  name = "n2_2")
        n2_2.set_weights([15,15,15])
        n2_3 = Inhibitory_Neuron(res, 1, 1,  name = "n2_3")
        n2_3.set_weights([15])
        n2_4 = Excitatory_Neuron(res, 2, 2,  name = "n2_4")
        n2_4.set_weights([15,15])
        n2_5 = Excitatory_Neuron(res, 1, 2,  name = "n2_5")
        n2_5.set_weights([15])
        n2_6 = Excitatory_Neuron(res, 4, 1,  name = "n2_6")
        n2_6.set_weights([15,15,8,8])

        self.scd_NAND = Gate_NAND(n2_0,n2_1,n2_2,n2_3,n2_4,n2_5,n2_6,res = res)

    
        self.scd_NAND.brain[0].num_dendrites = 3
        self.scd_NAND.brain[0].num_axon_terminals = 4
        self.scd_NAND.brain[0].weights = np.zeros(3)
        self.scd_NAND.brain[0].inputs = np.zeros(3)
        self.scd_NAND.brain[0].set_weights([6.5,6.5,6.5])

    #3rd NAND Gate -----------------------
        self.thrd_NAND = Gate_NAND(res = res , name = "n3_")
    
        delay_neuron = Excitatory_Neuron(res, 1, 1, name = "delay neuron") # Neuron to provide a delay between NAND gates 3 and 4
        delay_neuron.set_weights([15])

    #4th NAND Gate -----------------------
        self.fth_NAND = Gate_NAND(res = res, name = "n4_")
        

    #connection
        self.fst_NAND.connect(6, self.thrd_NAND.brain[0])    # Output of First NAND gate (neuron1_7) to input of Second NAND gate (neuron2_1)
        self.scd_NAND.connect(6, self.fth_NAND.brain[0])    # Output of Second NAND gate (neuron2_7) to input of Fourth NAND gate (neuron4_1)
        self.thrd_NAND.connect(6, delay_neuron)  # Self-connection for delay in Third NAND gate (neuron3_7 to neuron3_8)
        delay_neuron.connect_with_neuron(self.scd_NAND.brain[0])   # Delayed output of Third NAND gate (neuron3_8) to input of Second NAND gate (neuron2_2)
        delay_neuron.connect_with_neuron(self.fth_NAND.brain[0])   # Delayed output of Third NAND gate (neuron3_8) to input of Fourth NAND gate (neuron4_2)
        self.fth_NAND.connect(6, self.fst_NAND.brain[0])    # Output of Fourth NAND gate (neuron4_7) to input of First NAND gate (neuron1_1)
        self.fth_NAND.connect(6, self.thrd_NAND.brain[0])   # Output of Fourth NAND gate (neuron4_7) to input of Third NAND gate (neuron3_1)

    #append ton brain
        for el in [self.fst_NAND.brain,self.scd_NAND.brain,self.thrd_NAND.brain, self.fth_NAND.brain ]:
            for neuron in el: 
                self.add_to_brain(neuron)
        self.add_to_brain(delay_neuron)
        # [print(el.name) for el in self.brain]



#brain = [
# n1_0,   n2_0,   n3_0,   n4_0,    
# n1_1,   n2_1,   n3_1,   n4_1,    
# n1_2,   n2_2,   n3_2,   n4_2,    
# n1_3,   n2_3,   n3_3,   n4_3,    
# n1_4,   n2_4,   n3_4,   n4_4,    
# n1_5,   n2_5,   n3_5,   n4_5,    
# n1_6,   n2_6,   n3_6,   n4_6,    
# 
# delay neuron]

