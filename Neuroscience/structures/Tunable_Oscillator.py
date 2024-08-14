from Neuroscience.structures.Organ import Organ
from Neuroscience.structures.Excitatory_Neuron import Excitatory_Neuron
from Neuroscience.structures.Inhibitory_Neuron import Inhibitory_Neuron

import numpy as np


class Tunable_Oscillator(Organ) :

    

    def __init__ (self, neuron0=None, neuron1=None, neuron2_Excitatory=None,neuron2_Inhibitory=None,res = None):

        super().__init__()

        self.to_watch =  1 # True : watch excitatory. False : watch Inhibitory neuron

        if res is not None :

            neuron0 = Excitatory_Neuron(res, 2, 3)
            neuron0.set_weights([15,15])

            neuron1 = Excitatory_Neuron(res, 1, 3)
            neuron1.set_weights([15])

            neuron2_Excitatory = Excitatory_Neuron(res, 2, 1)
            neuron2_Excitatory.set_weights([0,0])

            neuron2_Inhibitory = Inhibitory_Neuron(res, 2, 1)
            neuron2_Inhibitory.set_weights([0,0])

            # both output neurons are initialised with weights = 0
            # when you instanciate them, you must initialise them one time with a create_oscillator call.
            # if you use them outside the Controller, just tune them manually.

        if neuron0 and neuron1 and neuron2_Excitatory and neuron2_Inhibitory:
            self.brain.append(neuron0)
            self.brain.append(neuron1)
            
            self.brain.append(neuron2_Inhibitory)
            self.brain.append(neuron2_Excitatory)

            
            neuron0.connect_with_neuron(neuron1)
            neuron1.connect_with_neuron(neuron0)
            
            neuron0.connect_with_neuron(neuron2_Excitatory)
            neuron1.connect_with_neuron(neuron2_Excitatory)

            neuron0.connect_with_neuron(neuron2_Inhibitory)
            neuron1.connect_with_neuron(neuron2_Inhibitory)


            self.input_neuron = [neuron0]
            self.output_neuron = [neuron2_Inhibitory, neuron2_Excitatory]

        else:
            raise ValueError("Invalid initialization parameters")
        
    
    def tune_oscillator(self, list_weights,sign):
        self.change_to_watch_neuron(sign)
        self.output_neuron[self.to_watch].set_weights(list_weights)
        self.output_neuron[(self.to_watch+1)%2].set_weights([0,0])

    def change_to_watch_neuron(self,sign):
        self.to_watch = 0 if sign>0 else 1