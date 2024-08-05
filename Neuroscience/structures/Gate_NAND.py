import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(project_root)

from Neuroscience.structures.Organ import Organ
from Neuroscience.structures.Excitatory_Neuron import Excitatory_Neuron
from Neuroscience.structures.Inhibitory_Neuron import Inhibitory_Neuron




class Gate_NAND(Organ):

    def __init__(self,neuron0 = None,neuron1 = None,neuron2 = None,neuron3 = None,neuron4 = None,neuron5 = None,neuron6 = None, res = None,name = ""):
        #builds a default NAND Gate

        super().__init__()

        if res is not None:
            neuron0 = Excitatory_Neuron(res, 2, 4, name = name + "0")
            neuron0.set_weights([7.5,7.5])

            neuron1 = Excitatory_Neuron(res, 1, 1,  name = name + "1")
            neuron1.set_weights([15])

            neuron2 = Inhibitory_Neuron(res, 3, 1,  name = name + "2")
            neuron2.set_weights([15,15,15])

            neuron3 = Inhibitory_Neuron(res, 1, 1,  name = name + "3")
            neuron3.set_weights([15])

            neuron4 = Excitatory_Neuron(res, 2, 2,  name = name + "4")
            neuron4.set_weights([15,15])

            neuron5 = Excitatory_Neuron(res, 1, 2,  name = name + "5")
            neuron5.set_weights([15])

            neuron6 = Excitatory_Neuron(res, 4, 1,  name = name + "6")
            neuron6.set_weights([15,15,8,8])
        if neuron0 and neuron1 and neuron2 and neuron3 and neuron4 and neuron5 and neuron6 :

            self.brain.append(neuron0)
            self.brain.append(neuron1)
            self.brain.append(neuron2)
            self.brain.append(neuron3)
            self.brain.append(neuron4)
            self.brain.append(neuron5)
            self.brain.append(neuron6)

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

            neuron4.taken_inputs[1] = 1


        else : 
            raise ValueError("Invalid initialization parameters")

    

        

