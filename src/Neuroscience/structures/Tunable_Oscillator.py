from Neuroscience.structures.Organ import Organ
from Neuroscience.structures.Excitatory_Neuron import Excitatory_Neuron
from Neuroscience.structures.Inhibitory_Neuron import Inhibitory_Neuron

import numpy as np

class Tunable_Oscillator(Organ):
    """
    A class representing a tunable neural oscillator composed of excitatory and inhibitory neurons.

    The `Tunable_Oscillator` class models a neural oscillator whose output can be tuned by adjusting the weights
    of the excitatory and inhibitory neurons. This class extends the `Organ` class and can be used to simulate
    rhythmic neural activity in a neural network.

    Attributes
    ----------
    name : str
        The name of the oscillator, initialized as "Tunable_Oscillator".
    
    to_watch : int
        Indicates which neuron to monitor for output, where 1 corresponds to the excitatory neuron and 0 to the inhibitory neuron.
    
    input_neuron : list of Abstract_Neuron
        A list containing the input neuron(s) of the oscillator.
    
    output_neuron : list of Abstract_Neuron
        A list containing the output neurons of the oscillator.
    """

    len = 4
    """
    The default number of neurons in the oscillator. This should be updated if the number of neurons changes.
    """

    def __init__(self, neuron0=None, neuron1=None, neuron2_Excitatory=None, neuron2_Inhibitory=None, res=None):
        """
        Initializes the Tunable_Oscillator with specified neurons or default neurons based on the resolution.

        :param neuron0: The first neuron in the oscillator, typically an excitatory neuron, defaults to None.
        :type neuron0: Excitatory_Neuron, optional
        :param neuron1: The second neuron in the oscillator, typically an excitatory neuron, defaults to None.
        :type neuron1: Excitatory_Neuron, optional
        :param neuron2_Excitatory: The third neuron, an excitatory output neuron, defaults to None.
        :type neuron2_Excitatory: Excitatory_Neuron, optional
        :param neuron2_Inhibitory: The fourth neuron, an inhibitory output neuron, defaults to None.
        :type neuron2_Inhibitory: Inhibitory_Neuron, optional
        :param res: The resolution for initializing default neurons, required if neurons are not provided, defaults to None.
        :type res: int, optional

        :raises ValueError: If neurons are not provided and resolution is not specified, or if an invalid combination of neurons is provided.
        """
        super().__init__()
        self.name = "Tunable_Oscillator"
        self.to_watch = 1  # 1: watch excitatory, 0: watch inhibitory neuron

        if res is not None:
            neuron0 = Excitatory_Neuron(res, 2, 3)
            neuron0.set_weights([15, 15])

            neuron1 = Excitatory_Neuron(res, 1, 3)
            neuron1.set_weights([15])

            neuron2_Excitatory = Excitatory_Neuron(res, 2, 1)
            neuron2_Excitatory.set_weights([0, 0])

            neuron2_Inhibitory = Inhibitory_Neuron(res, 2, 1)
            neuron2_Inhibitory.set_weights([0, 0])

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
        
    def tune_oscillator(self, list_weights, sign):
        """
        Tunes the oscillator by setting the weights of the output neurons based on the sign.

        The output neuron corresponding to the sign is activated with the specified weights, while the other output neuron is deactivated.

        :param list_weights: The list of weights to be set for the active output neuron.
        :type list_weights: list of float
        :param sign: Determines which neuron to activate; positive for excitatory, negative for inhibitory.
        :type sign: int
        """
        self.change_to_watch_neuron(sign)
        self.output_neuron[self.to_watch].set_weights(list_weights)
        self.output_neuron[(self.to_watch + 1) % 2].set_weights([0, 0])

    def change_to_watch_neuron(self, sign):
        """
        Changes the neuron being monitored based on the sign.

        :param sign: Determines which neuron to monitor; positive for excitatory, negative for inhibitory.
        :type sign: int
        """
        self.to_watch = 0 if sign > 0 else 1
