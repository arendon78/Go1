import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(project_root)

from Neuroscience.structures.Organ import Organ
from Neuroscience.structures.Excitatory_Neuron import Excitatory_Neuron
from Neuroscience.structures.Inhibitory_Neuron import Inhibitory_Neuron

class Gate_NAND(Organ):
    """
    A class representing a NAND gate constructed using a network of neurons.

    The `Gate_NAND` class models a digital NAND gate using excitatory and inhibitory neurons. It can be 
    initialized with default neurons or with specific neuron instances. This class extends the `Organ` 
    class and is part of a neural network simulation.

    Attributes
    ----------
    name : str
        The name of the gate, initialized as "NAND_Gate".

    brain : list of Abstract_Neuron
        The list of neurons that make up the NAND gate.

    output_neurons : list of Abstract_Neuron
        The list containing the output neuron(s) of the NAND gate.
    """

    def __init__(self, neuron0=None, neuron1=None, neuron2=None, neuron3=None, neuron4=None, neuron5=None, neuron6=None, res=None, name=""):
        """
        Initializes a Gate_NAND instance, either with specific neurons or with default neurons based on the given resolution.

        :param neuron0: The first neuron in the NAND gate, defaults to None.
        :type neuron0: Excitatory_Neuron, optional
        :param neuron1: The second neuron in the NAND gate, defaults to None.
        :type neuron1: Excitatory_Neuron, optional
        :param neuron2: The third neuron in the NAND gate, defaults to None.
        :type neuron2: Inhibitory_Neuron, optional
        :param neuron3: The fourth neuron in the NAND gate, defaults to None.
        :type neuron3: Inhibitory_Neuron, optional
        :param neuron4: The fifth neuron in the NAND gate, defaults to None.
        :type neuron4: Excitatory_Neuron, optional
        :param neuron5: The sixth neuron in the NAND gate, defaults to None.
        :type neuron5: Excitatory_Neuron, optional
        :param neuron6: The seventh neuron in the NAND gate, defaults to None.
        :type neuron6: Excitatory_Neuron, optional
        :param res: The resolution for initializing default neurons, required if neurons are not provided, defaults to None.
        :type res: int, optional
        :param name: The name of the NAND gate, defaults to an empty string.
        :type name: str, optional

        :raises ValueError: If neurons are not provided and resolution is not specified, or if an invalid combination of neurons is provided.
        """
        super().__init__()
        self.name = "NAND_Gate"

        if res is not None and neuron0 is None:
            neuron0 = Excitatory_Neuron(res, 2, 4)
            neuron0.set_weights([7.5, 7.5])

            neuron1 = Excitatory_Neuron(res, 1, 1)
            neuron1.set_weights([15])

            neuron2 = Inhibitory_Neuron(res, 3, 1)
            neuron2.set_weights([15, 15, 15])

            neuron3 = Inhibitory_Neuron(res, 1, 1)
            neuron3.set_weights([15])

            neuron4 = Excitatory_Neuron(res, 2, 2)
            neuron4.set_weights([15, 15])

            neuron5 = Excitatory_Neuron(res, 1, 2)
            neuron5.set_weights([15])

            neuron6 = Excitatory_Neuron(res, 4, 1)
            neuron6.set_weights([15, 15, 8, 8])

        if neuron0 and neuron1 and neuron2 and neuron3 and neuron4 and neuron5 and neuron6:
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
            self.output_neurons = [neuron6]
        else:
            raise ValueError("Invalid initialization parameters")
