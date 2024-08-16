import os
import sys


project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(project_root)

from Neuroscience.structures.Flip_FLop_T import Flip_Flop_T
from Neuroscience.structures.Tunable_Oscillator import Tunable_Oscillator
from Neuroscience.structures.Gate_NAND import Gate_NAND
from Neuroscience.structures.Organ import Organ
from Neuroscience.structures.Excitatory_Neuron import Excitatory_Neuron
from Neuroscience.structures.Inhibitory_Neuron import Inhibitory_Neuron


class Counter_1_bit(Organ):


    def pass_inputs(self,inputs, k):
        self.T0.pass_inputs_oscillators(inputs,k)
        self.neuronC_1.inputs[1] = inputs[k][1]
        self.T0.pass_inputs_selfputs(inputs,k)

    def __init__(self,res):
        #mettre en place les noms et vérifier la fonction de débug
        super().__init__()

        self.T0 = Flip_Flop_T(res)


        # Neurons for providing a constant train of pulses
        self.neuronC_1 = Excitatory_Neuron(res, 2, 3)
        self.neuronC_1.set_weights([15,15])

        self.neuronC_2 = Excitatory_Neuron(res, 1, 1)
        self.neuronC_2.set_weights([15])

        
        # The output of the counter's AND gate is the input for Flip Flop T2



        
        # Neurons providing a train of pulses to Flip Flop T0 (logic 1)
        self.neuronC_1.connect_with_neuron(self.T0.brain[0])
        self.neuronC_1.connect_with_neuron(self.T0.brain[7])
        self.neuronC_1.connect_with_neuron(self.neuronC_2)
        self.neuronC_2.connect_with_neuron(self.neuronC_1)
 
        self.output_neurons = [self.T0.brain[-1]]
        self.brain = self.T0.brain + [self.neuronC_1, self.neuronC_2]

        
