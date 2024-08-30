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
        """
        @brief Initializes the 1-bit counter with a Flip-Flop T and necessary neurons.

        @param res Resolution or configuration parameter required to initialize the neural components.

        @section Components
        - **Flip-Flop T:** A toggle flip-flop providing the core functionality of the counter.
        - **Excitatory Neurons:** Two neurons (`neuronC_1` and `neuronC_2`) that generate a pulse train to drive the flip-flop.

        @section Neural Connections
        - **neuronC_1 -> T0.brain[0], T0.brain[7], neuronC_2:** Connects the first neuron to the flip-flop and the second neuron.
        - **neuronC_2 -> neuronC_1:** Reciprocally connects the second neuron to the first.

        @section Output
        The counter's output neuron is the Q output of the Flip-Flop T, accessed via `self.output_neurons`.
        """

        super().__init__()
        self.name = "Counter_1_bit"

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
 
        # self.output_neurons = [self.T0.brain[-1]]
        self.output_neurons = [ self.T0.output_neurons[0]] # This is the Q output
        self.brain = self.T0.brain + [self.neuronC_1, self.neuronC_2]

        
