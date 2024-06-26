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


class Counter_3_bits(Organ):


    def pass_inputs(self,inputs, k):
        self.T0.pass_inputs_oscillators(inputs,k)
        self.T1.pass_inputs_oscillators(inputs,k)
        self.T2.pass_inputs_oscillators(inputs,k)
        self.neuronC_1.inputs[1] = inputs[k][1]
        self.T0.pass_inputs_selfputs(inputs,k)
        self.T1.pass_inputs_selfputs(inputs,k)
        self.T2.pass_inputs_selfputs(inputs,k)


    def __init__(self,res):
        #mettre en place les noms et vérifier la fonction de débug
        super().__init__()

        self.T0 = Flip_Flop_T(res)
        self.T1 = Flip_Flop_T(res)
        self.T2 = Flip_Flop_T(res)

        # Neurons for providing a constant train of pulses
        self.neuronC_1 = Excitatory_Neuron(res, 2, 3)
        self.neuronC_1.set_weights([15,15])

        self.neuronC_2 = Excitatory_Neuron(res, 1, 1)
        self.neuronC_2.set_weights([15])

        # Neuron for the AND gate inside the counter
        self.neuronC_3 = Excitatory_Neuron(res, 2, 2)
        self.neuronC_3.set_weights([8,8])

        # The inputs for the counter's AND gate are Q0 and Q1
        # (Flip Flops T0 and T1 respectively)


        self.T0.brain[-1].connect_with_neuron(self.neuronC_3)
        self.T1.brain[-1].connect_with_neuron(self.neuronC_3)

    # neuronT0_3_8.connect_with_neuron(neuronC_3)
    # neuronT1_3_8.connect_with_neuron(neuronC_3)
        
        # The output of the counter's AND gate is the input for Flip Flop T2

        self.neuronC_3.connect_with_neuron(self.T2.brain[0])
        self.neuronC_3.connect_with_neuron(self.T2.brain[7])
    # neuronC_3.connect_with_neuron(neuronT2_1_1)
    # neuronC_3.connect_with_neuron(neuronT2_2_1)
        
        # Input for Flip Flop T1
        self.T0.brain[-1].connect_with_neuron(self.T1.brain[0])
        self.T0.brain[-1].connect_with_neuron(self.T1.brain[7])
    # neuronT0_3_8.connect_with_neuron(neuronT1_1_1)
    # neuronT0_3_8.connect_with_neuron(neuronT1_2_1)


        
        # Neurons providing a train of pulses to Flip Flop T0 (logic 1)
        self.neuronC_1.connect_with_neuron(self.T0.brain[0])
        self.neuronC_1.connect_with_neuron(self.T0.brain[7])
        self.neuronC_1.connect_with_neuron(self.neuronC_2)
        self.neuronC_2.connect_with_neuron(self.neuronC_1)
    # neuronC_1.connect_with_neuron(neuronT0_1_1)
    # neuronC_1.connect_with_neuron(neuronT0_2_1)
    # neuronC_1.connect_with_neuron(neuronC_2)
    # neuronC_2.connect_with_neuron(neuronC_1)
        self.output_neurons = self.output_neurons = [self.T0.brain[-1], self.T1.brain[-1], self.T2.brain[-1]]
        self.brain = self.T2.brain + self.T1.brain + self.T0.brain + [self.neuronC_1, self.neuronC_2, self.neuronC_3]

        
