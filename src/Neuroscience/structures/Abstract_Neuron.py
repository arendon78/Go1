import numpy as np
import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(project_root)
from Neuroscience.structures.Organ import Organ

class Abstract_Neuron(Organ):
    """
    A class representing an abstract neuron model used in computational neuroscience.

    The `Abstract_Neuron` class simulates the behavior of a neuron, focusing on synaptic potentials, 
    membrane potential dynamics, and action potentials. It can be used as a building block for more 
    complex neural network structures.

    """


    instanciation_counter = 0
    """
    A class-level counter that tracks the number of Abstract_Neuron instances created.

    .
    """

    tau = 1.0857
    """
    Time constant (ms) used in the exponential functions for charging and discharging potentials. 
        This influences the duration of EPSPs and IPSPs.

    .
    """

    membrane_potential = 0
    """
     The membrane potential of the neuron, initially set to zero. The neuron fires when this potential 
        exceeds the threshold voltage.

    .
    """


    EPSP_time = 150
    """
     Duration (in simulation steps) of an Excitatory Post-Synaptic Potential (EPSP), including 
        charge, stable response, and discharge phases.

    .
    """

    IPSP_time = 150
    """
     Duration (in simulation steps) of an Inhibitory Post-Synaptic Potential (IPSP), including 
        charge, stable response, and discharge phases.

    .
    """

    Act_Pot_time = 50
    """
     Duration of an action potential pulse (in simulation steps), including the refractory period.
     
    .
    """

    Act_Pot_volt = 86.9
    """
    Peak voltage (mV) during an action potential.

    .
    """

    Thres_Act_Pot_volt = 14.9
    """
    Threshold voltage (mV) required to fire the neuron.
    
    .
    """

    res = 0.1
    """
     The resolution of the simulation, affecting the time steps.

    .
    """

    def __init__(self, res, inputs, outputs, instance_count=""):
        """
        Initializes the Abstract_Neuron instance with specific resolution, number of inputs (dendrites), 
        and outputs (axon terminals).

        :param res: The resolution of the simulation, affecting the time steps.
        :type res: int
        :param inputs: Number of dendrites (input connections) in the neuron.
        :type inputs: int
        :param outputs: Number of axon terminals (output connections) in the neuron.
        :type outputs: int
        :param instance_count: A string to distinguish different instances, default is an empty string.
        :type instance_count: str, optional

        .
        """
        super().__init__()

        self.instance_count = str(Abstract_Neuron.instanciation_counter)
        Abstract_Neuron.instanciation_counter += 1

        self.num_dendrites = inputs
        self.num_axon_terminals = outputs
        self.inputs = np.zeros(self.num_dendrites)
        self.taken_inputs = np.zeros(self.num_dendrites)
        self.weights = np.zeros(self.num_dendrites)
        self.active_potential_bool = False
        self.volt_dendrites = np.zeros(self.num_dendrites)
        self.temp_summation = np.zeros(self.num_dendrites)
        self.axon_terminals = []
        self.max_active_potential = False
        self.active_PSP = [False for _ in range(self.num_dendrites)]
        self.temp_inputs = np.zeros(self.num_dendrites)
        self.time_dendrites = np.zeros(self.num_dendrites)
        self.time_neuron = 0
        self.resolution = res
        self.brain = [self]

    def spatial_summation(self):
        """
        Performs spatial summation on all dendrites of the neuron.

        This method updates the membrane potential based on the combined inputs from all active synapses. 
        If the membrane potential exceeds the threshold, the neuron fires an action potential.

        :returns: The updated membrane potential after spatial summation.
        :rtype: float

        .
        """
        result = 0
        for i in range(self.num_dendrites):
            if self.active_PSP[i]:
                self.time_dendrites[i] += 1

                if self.temp_inputs[i] == 1:
                    self.volt_dendrites[i] = self.EPSP(i, self.time_dendrites[i] * self.resolution, self.weights[i])
                elif self.temp_inputs[i] == -1:
                    self.volt_dendrites[i] = self.IPSP(i, self.time_dendrites[i] * self.resolution, self.weights[i])

                result += self.volt_dendrites[i]

                if self.membrane_potential > self.Thres_Act_Pot_volt:
                    self.active_potential_bool = True
                    self.time_neuron = 0
                    self.reset_PSP()

                if (self.time_dendrites[i] * self.resolution) == self.EPSP_time / 10:
                    self.active_PSP[i] = False
                    self.volt_dendrites[i] = 0
                    self.time_dendrites[i] = 0
                    self.temp_summation[i] = 0
                    self.temp_inputs[i] = 0

        self.membrane_potential = result
        return result

    def get_voltage(self):
        """
        Gets the current voltage values for each dendrite.

        :returns: An array of voltage values for each dendrite.
        :rtype: numpy.ndarray

        .
        """
        return self.volt_dendrites

    def active_potential(self, t):
        """
        Simulates the action potential over the time period `t`.

        This method includes both the action potential and the refractory period.

        :param t: Time step for which the action potential is being calculated.
        :type t: float
        :returns: The membrane potential at time `t` during the action potential.
        :rtype: float

        .
        """
        if t == self.Act_Pot_time / 10:
            self.active_potential_bool = False

        self.membrane_potential = (np.sin(1.5 * t) / (1.5 * t) - 0.1266) * 100

        if self.max_active_potential:
            self.max_active_potential = False

        if self.membrane_potential > self.Act_Pot_volt:
            self.max_active_potential = True

        return self.membrane_potential

    def EPSP(self, index, t, weight):
        """
        Calculates the Excitatory Post-Synaptic Potential (EPSP) for a given dendrite.

        This method simulates the potential that will be added up, and if the threshold is reached (15 mV), 
        it fires the neuron.

        :param index: Index of the dendrite receiving the EPSP.
        :type index: int
        :param t: Time step at which the EPSP is calculated.
        :type t: float
        :param weight: Synaptic weight associated with the dendrite.
        :type weight: float
        :returns: The voltage change due to the EPSP at the specified dendrite.
        :rtype: float

        .
        """
        if t < self.EPSP_time / 30 + 3:
            value = weight * (1 - np.exp(-(t / self.tau))) + self.temp_summation[index]
        else:
            value = weight * np.exp(-((t - 7.9) / self.tau))

        return value

    def IPSP(self, index, t, weight):
        """
        Calculates the Inhibitory Post-Synaptic Potential (IPSP) for a given dendrite.

        This method simulates the potential that will be subtracted, and if the threshold is reached (15 mV), 
        it fires the neuron.

        :param index: Index of the dendrite receiving the IPSP.
        :type index: int
        :param t: Time step at which the IPSP is calculated.
        :type t: float
        :param weight: Synaptic weight associated with the dendrite.
        :type weight: float
        :returns: The voltage change due to the IPSP at the specified dendrite.
        :rtype: float

        .
        """
        if t < self.EPSP_time / 30 + 3:
            value = -weight * (1 - np.exp(-(t / self.tau))) + self.temp_summation[index]
        else:
            value = -weight * np.exp(-((t - 7.9) / self.tau))

        return value

    def set_weights(self, values):
        """
        Sets the synaptic weights for each dendrite.

        The weights must be such that the output voltage remains within physiological limits.

        :param values: List of weights to be set for each dendrite.
        :type values: list of float

        .
        """
        for i in range(self.num_dendrites):
            self.weights[i] = values[i]

    def reset_PSP(self):
        """
        Resets all Post-Synaptic Potentials (PSPs) to their default (inactive) states.
        
        .
        """
        for i in range(self.num_dendrites):
            self.active_PSP[i] = False
            self.volt_dendrites[i] = 0
            self.time_dendrites[i] = 0
            self.temp_summation[i] = 0
            self.temp_inputs[i] = 0

    def reset_axon_terminals(self):
        """
        Turns off all axon terminals, indicating no active signaling.

        .
        """
        for i in range(self.num_axon_terminals):
            self.axon_terminals[i][1] = 0

    def present_inputs(self, inputs):
        """
        Processes incoming inputs at the current time step.

        This method checks if an active potential is occurring, and if not, updates the neuron's state 
        based on the inputs.

        :param inputs: List of inputs for each dendrite. Values should be 1 for excitatory input, 
                       -1 for inhibitory input, or 0 for no input.
        :type inputs: list of int

        .
        """
        if not self.active_potential_bool:
            for i in range(len(inputs)):
                if inputs[i] == 1 or inputs[i] == -1:
                    self.active_PSP[i] = True
                    self.temp_summation[i] = self.volt_dendrites[i]
                    self.temp_inputs[i] = inputs[i]
                    self.time_dendrites[i] = 0

    def connect_with_neuron(self, target_neuron):
        """
        Establishes a connection between this neuron and a target neuron.

        This is done by linking an axon terminal to the target neuron's dendrite.

        :param target_neuron: The target neuron to connect to.
        :type target_neuron: Abstract_Neuron

        .
        """
        index = target_neuron.assign_input()
        if index != -1:
            self.axon_terminals.append([target_neuron, index])

    def is_connected(self, n):
        """
        Checks if this neuron is already connected to the given neuron `n`.

        :param n: The neuron to check connection with.
        :type n: Abstract_Neuron
        :returns: True if connected, False otherwise.
        :rtype: bool
        
        .
        """
        return n in [el[0] for el in self.axon_terminals]

    def assign_input(self):
        """
        Assigns an available dendrite to a connecting neuron.

        :returns: The index of the assigned dendrite. Returns -1 if no dendrite is available.
        :rtype: int

        .
        """ 
        for i in range(self.num_dendrites):
            if self.taken_inputs[i] == 0:
                self.taken_inputs[i] = 1
                return i
        return -1
