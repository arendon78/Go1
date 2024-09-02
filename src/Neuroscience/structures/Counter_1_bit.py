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
    """
    A class representing a 1-bit counter implemented with neural network components.

    This class uses a `Flip_Flop_T` structure as the core of the counter, driven by excitatory neurons 
    to provide the necessary pulse train.

    :param res: Resolution or configuration parameter required to initialize the neural components.
    :type res: int


    """


    def pass_inputs(self,inputs, k):
        """
        Passes the input signals to the appropriate neural components of the 1-bit counter.
    
        This method routes the inputs to both the `Flip_Flop_T` structure and the relevant excitatory neurons 
        based on the current timestep `k`. It ensures that the neural components receive the correct input signals 
        at each step of the operation.
    
        :param inputs: A list or array of input signals where each entry corresponds to a different timestep.
        :type inputs: list
        :param k: The current timestep index, used to select the appropriate input signals.
        :type k: int
    
        .. note::
            - The `Flip_Flop_T` component handles the oscillatory inputs through the method 
              `pass_inputs_oscillators`, and `pass_inputs_selfputs`.
            - The second input to `neuronC_1` is directly set from the input at the current timestep.
        """

        self.T0.pass_inputs_oscillators(inputs,k)
        self.neuronC_1.inputs[1] = inputs[k][1]
        self.T0.pass_inputs_selfputs(inputs,k)

    def __init__(self,res):

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

        
