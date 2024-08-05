from Neuroscience.structures.Organ import Organ
from Neuroscience.structures.Excitatory_Neuron import Excitatory_Neuron
from Neuroscience.structures.Inhibitory_Neuron import Inhibitory_Neuron

import numpy as np


class Tunable_Oscillator(Organ) :

    

    def __init__ (self, neuron1=None, neuron2=None, neuron3=None,res = None,type = 1):
        super().__init__()

        if res is not None :
            neuron1 = Excitatory_Neuron(res, 2, 2)
            neuron1.set_weights([15,15])

            neuron2 = Excitatory_Neuron(res, 1, 2)
            neuron2.set_weights([15])

            if type == 1: 
                neuron3 = Excitatory_Neuron(res, 2, 1)
                neuron3.set_weights([7.8,7.8])

            if type == -1: 
                neuron3 = Inhibitory_Neuron(res, 2, 1)
                neuron3.set_weights([7.8,7.8])

        if neuron1 and neuron2 and neuron3:
            self.brain.append(neuron1)
            self.brain.append(neuron2)
            self.brain.append(neuron3)


            self.brain[0].connect_with_neuron(self.brain[1])
            self.brain[0].connect_with_neuron(self.brain[2])
            self.brain[1].connect_with_neuron(self.brain[0])
            self.brain[1].connect_with_neuron(self.brain[2])


            self.input_neuron = [neuron1]
            self.output_neuron = [neuron3]

        else:
            raise ValueError("Invalid initialization parameters")
    
