import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(project_root)

from Neuroscience.structures.Gate_NAND import Gate_NAND
from Neuroscience.structures.Excitatory_Neuron import Excitatory_Neuron
from Neuroscience.structures.Inhibitory_Neuron import Inhibitory_Neuron
from Neuroscience.structures.Organ import Organ

import numpy as np

class Flip_Flop_T(Organ):
    """
    A class representing a T-type flip-flop circuit constructed using NAND gates.

    The `Flip_Flop_T` class simulates the behavior of a T-type flip-flop using four NAND gates, with 
    each NAND gate composed of excitatory and inhibitory neurons. This class includes methods for 
    passing inputs, printing the state of the neurons, and connecting the flip-flop circuit.

    Attributes
    ----------
    name : str
        The name of the flip-flop circuit, initialized as "Flip_Flop".

    fst_NAND : Gate_NAND
        The first NAND gate in the flip-flop circuit.

    scd_NAND : Gate_NAND
        The second NAND gate in the flip-flop circuit.

    thrd_NAND : Gate_NAND
        The third NAND gate in the flip-flop circuit.

    fth_NAND : Gate_NAND
        The fourth NAND gate in the flip-flop circuit.

    output_neurons : list of Abstract_Neuron
        A list containing the output neurons of the flip-flop circuit.
    """

    def print(self):
        """
        Prints the details of all neurons in the flip-flop circuit.
        """
        for n in self.brain:
            n.print()
            print("")

    def pass_inputs_oscillators(self, inputs, k):
        """
        Sets the inputs for the oscillators in each NAND gate.

        :param inputs: A list of inputs to be passed to the oscillators.
        :type inputs: list of float
        :param k: The index of the current input set.
        :type k: int
        """
        self.fst_NAND.brain[4].inputs[1] = inputs[k][1]  # neuron1_5.inputs[1]
        self.scd_NAND.brain[4].inputs[1] = inputs[k][1]  # neuron2_5.inputs[1]
        self.thrd_NAND.brain[4].inputs[1] = inputs[k][1] # neuron3_5.inputs[1]
        self.fth_NAND.brain[4].inputs[1] = inputs[k][1]  # neuron4_5.inputs[1]

    def pass_inputs_selfputs(self, inputs, k):
        """
        Sets the self inputs for the first and second NAND gates.

        :param inputs: A list of inputs to be passed to the NAND gates.
        :type inputs: list of float
        :param k: The index of the current input set.
        :type k: int
        """
        self.fst_NAND.brain[0].inputs[2] = inputs[k][0]  # neuron1_1.inputs[2]
        self.scd_NAND.brain[0].inputs[2] = inputs[k][0]  # neuron2_1.inputs[2]

    def pass_inputs(self, inputs, k):
        """
        Passes the inputs to both oscillators and self inputs in the NAND gates.

        :param inputs: A list of inputs to be passed to the NAND gates.
        :type inputs: list of float
        :param k: The index of the current input set.
        :type k: int
        """
        self.pass_inputs_oscillators(inputs, k)
        self.pass_inputs_selfputs(inputs, k)

    def __init__(self, res):
        """
        Initializes the Flip_Flop_T instance with a specified resolution and constructs the NAND gates.

        :param res: The resolution of the simulation, affecting time steps.
        :type res: int
        """
        super().__init__()
        self.name = "Flip_Flop"

        # 1st NAND Gate -----------------------
        n1_0 = Excitatory_Neuron(res, 3, 4)
        n1_0.set_weights([6.5, 6.5, 6.5])
        n1_1 = Excitatory_Neuron(res, 1, 1)
        n1_1.set_weights([15])
        n1_2 = Inhibitory_Neuron(res, 3, 1)
        n1_2.set_weights([15, 15, 15])
        n1_3 = Inhibitory_Neuron(res, 1, 1)
        n1_3.set_weights([15])
        n1_4 = Excitatory_Neuron(res, 2, 2)
        n1_4.set_weights([15, 15])
        n1_5 = Excitatory_Neuron(res, 1, 2)
        n1_5.set_weights([15])
        n1_6 = Excitatory_Neuron(res, 4, 1)
        n1_6.set_weights([15, 15, 8, 8])

        self.fst_NAND = Gate_NAND(n1_0, n1_1, n1_2, n1_3, n1_4, n1_5, n1_6, res=res)

        # 2nd NAND Gate -----------------------
        n2_0 = Excitatory_Neuron(res, 3, 4)
        n2_0.set_weights([6.5, 6.5, 6.5])
        n2_1 = Excitatory_Neuron(res, 1, 1)
        n2_1.set_weights([15])
        n2_2 = Inhibitory_Neuron(res, 3, 1)
        n2_2.set_weights([15, 15, 15])
        n2_3 = Inhibitory_Neuron(res, 1, 1)
        n2_3.set_weights([15])
        n2_4 = Excitatory_Neuron(res, 2, 2)
        n2_4.set_weights([15, 15])
        n2_5 = Excitatory_Neuron(res, 1, 2)
        n2_5.set_weights([15])
        n2_6 = Excitatory_Neuron(res, 4, 1)
        n2_6.set_weights([15, 15, 8, 8])

        self.scd_NAND = Gate_NAND(n2_0, n2_1, n2_2, n2_3, n2_4, n2_5, n2_6, res=res)

        self.scd_NAND.brain[0].num_dendrites = 3
        self.scd_NAND.brain[0].num_axon_terminals = 4
        self.scd_NAND.brain[0].weights = np.zeros(3)
        self.scd_NAND.brain[0].inputs = np.zeros(3)
        self.scd_NAND.brain[0].set_weights([6.5, 6.5, 6.5])

        # 3rd NAND Gate -----------------------
        self.thrd_NAND = Gate_NAND(res=res)

        delay_neuron = Excitatory_Neuron(res, 1, 2)  # Neuron to provide a delay between NAND gates 3 and 4
        delay_neuron.set_weights([15])

        # 4th NAND Gate -----------------------
        self.fth_NAND = Gate_NAND(res=res)

        # Connection setup between the gates and neurons
        self.fst_NAND.connect(6, self.thrd_NAND.brain[0])  # Output of 1st NAND to input of 3rd NAND
        self.scd_NAND.connect(6, self.fth_NAND.brain[0])  # Output of 2nd NAND to input of 4th NAND
        self.thrd_NAND.connect(6, delay_neuron)  # Self-connection for delay in 3rd NAND
        delay_neuron.connect_with_neuron(self.scd_NAND.brain[0])  # Delayed output to input of 2nd NAND
        delay_neuron.connect_with_neuron(self.fth_NAND.brain[0])  # Delayed output to input of 4th NAND
        self.fth_NAND.connect(6, self.fst_NAND.brain[0])  # Output of 4th NAND to input of 1st NAND
        self.fth_NAND.connect(6, self.thrd_NAND.brain[0])  # Output of 4th NAND to input of 3rd NAND

        # Append to brain
        for el in [self.fst_NAND.brain, self.scd_NAND.brain, self.thrd_NAND.brain, self.fth_NAND.brain]:
            for neuron in el:
                self.add_to_brain(neuron)
        self.add_to_brain(delay_neuron)

        self.output_neurons = [delay_neuron]
