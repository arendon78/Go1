import numpy as np
import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(project_root)

from Neuroscience.structures.Excitatory_Neuron import Excitatory_Neuron
from Neuroscience.structures.Inhibitory_Neuron import Inhibitory_Neuron
from Neuroscience.structures.Controller import Controller

class Frequency_Detector:
    """
    A class to detect and calculate the firing frequency of neurons in a neural network.

    The `Frequency_Detector` class monitors the activity of a set of neurons and computes their firing 
    frequency. It provides methods to update firing rates, calculate frequencies, and convert these 
    frequencies into different formats.

    Attributes
    ----------
    name : str
        The name of the frequency detector, initialized as "Frequency_Detector".
    
    watch_neurons : list of Abstract_Neuron
        The list of neurons being monitored for their firing frequency.

    len : int
        The number of neurons being monitored.

    resolution : int
        The resolution of the simulation, affecting time steps.

    timestamps : numpy.ndarray
        A 2D array to track the last two spike times for each neuron.

    frequency : numpy.ndarray
        An array to store the calculated firing frequency for each neuron.

    max_sum_frequency : float
        The maximum possible sum of frequencies based on the number of neurons being monitored.

    delta_t : int
        The time threshold after which a neuron's frequency is reset if no spike is detected.

    controller : object
        A reference to the controller managing the neurons, if applicable.

    time : int
        A variable to track the time in the simulation.

    timer_active : bool
        A flag to indicate whether the timer is active or not.
    
    spike_detector : bool
        A flag to indicate whether the spike detector mode is active.
    
    clock : list of int
        A list to track the timing for each neuron, relevant when the spike detector is active.
    """

    max_frequency = 9.00900900900901
    """
    The maximum possible frequency for a neuron, in spike/thousand steps of simulation.
    """

    def __init__(self, res, list_neurons=[], controller=None, delta_t=690, spike_detector=False):
        """
        Initializes the Frequency_Detector with a specified resolution and optionally a list of neurons or a controller.

        :param res: The resolution of the simulation, affecting time steps.
        :type res: int
        :param list_neurons: A list of neurons to be monitored, defaults to an empty list.
        :type list_neurons: list of Abstract_Neuron, optional
        :param controller: A controller managing the neurons, defaults to None.
        :type controller: object, optional
        :param delta_t: The time threshold after which a neuron's frequency is reset if no spike is detected, defaults to 690.
        :type delta_t: int, optional
        :param spike_detector: Flag to indicate if the spike detector mode is active, defaults to False.
        :type spike_detector: bool, optional
        """
        self.name = "Frequency_Detector"
        self.previous_to_watch = []
        if controller:
            self.watch_neurons = [oscillator.output_neuron[oscillator.to_watch] for oscillator in controller.oscillators]
            self.to_watch = [oscillator.to_watch for oscillator in controller.oscillators]
            self.len = len(self.watch_neurons)
        else:
            self.watch_neurons = list_neurons
            self.len = len(self.watch_neurons)
            self.clock = [-1 for _ in range(self.len)]
        self.spike_detector = spike_detector

        self.resolution = res
        self.timestamps = np.zeros((self.len, 2)) - 1
        self.frequency = np.zeros(self.len)
        self.max_sum_frequency = self.max_frequency * self.len
        self.delta_t = delta_t
        self.controller = controller
        self.time = 0
        self.timer_active = False

    def new_init_(self, controller, new_to_watch):
        """
        Re-initializes the Frequency_Detector with a new set of neurons to monitor.

        :param controller: A controller managing the neurons.
        :type controller: object
        :param new_to_watch: The new list of indices of neurons to watch.
        :type new_to_watch: list of int
        """
        self.watch_neurons = [oscillator.output_neuron[oscillator.to_watch] for oscillator in controller.oscillators]
        self.to_watch = new_to_watch
        self.len = len(self.watch_neurons)
        self.timestamps = np.zeros((self.len, 2)) - 1
        self.frequency = np.zeros(self.len)

    def update_firing_rate(self, k):
        """
        Updates the firing rate of the monitored neurons based on their activity.

        :param k: The current time step in the simulation.
        :type k: int
        """
        for f in self.frequency:
            if f == 1:
                print("\n\n\n  ERROR ! frequency of 1000  !\n\n\n")

        if self.controller:
            new_to_watch = [oscillator.to_watch for oscillator in self.controller.oscillators]
            if new_to_watch != self.to_watch:
                self.new_init_(self.controller, new_to_watch)

        for i in range(self.len):
            cur_neur = self.watch_neurons[i]

            if abs(self.timestamps[i, 0] - k) > self.delta_t:
                self.frequency[i] = 0

            if cur_neur.max_active_potential:
                self.timestamps[i] = np.roll(self.timestamps[i], 1)
                self.timestamps[i, 0] = k

                if self.spike_detector:
                    if self.clock[i] == -1:
                        self.clock[i] = self.delta_t
                    elif self.clock[i] == 0:
                        self.calculate_frequency(i)
                    else:
                        pass
                else:
                    self.calculate_frequency(i)

    def calculate_frequency(self, index):
        """
        Calculates the firing frequency for a specific neuron.

        :param index: The index of the neuron in the watch list.
        :type index: int
        """
        valid_timestamps = self.timestamps[index][self.timestamps[index] > 0]
        if len(valid_timestamps) > 1:
            intervals = np.diff(valid_timestamps)
            avg_interval = np.mean(intervals)
            if isinstance(self.watch_neurons[index], Inhibitory_Neuron):
                self.frequency[index] = -1 / avg_interval
            elif isinstance(self.watch_neurons[index], Excitatory_Neuron):
                self.frequency[index] = 1 / avg_interval

    def get_freq(self, index):
        """
        Gets the frequency of a specific neuron, scaled by 1000.

        :param index: The index of the neuron in the watch list.
        :type index: int
        :returns: The firing frequency of the neuron.
        :rtype: float
        """
        return self.frequency[index] * 1000

    def print_frequency(self):
        """
        Prints the frequency of each monitored neuron.
        """
        [print(self.get_freq(i)) for i in range(self.len)]
        print("\n\n")

    def sum_frequencies(self):
        """
        Sums the frequencies of all monitored neurons, scaled by 1000.

        :returns: The total sum of frequencies.
        :rtype: float
        """
        sum_freq = 0
        for el, neur in zip(self.frequency, self.watch_neurons):
            sum_freq += el * 1000
        return sum_freq

    def frequency_ratio(self, lower_bound=-2, upper_bound=2):
        """
        Calculates the normalized frequency ratio based on the sum of neuron frequencies.

        :param lower_bound: The lower bound for normalization, defaults to -2.
        :type lower_bound: float, optional
        :param upper_bound: The upper bound for normalization, defaults to 2.
        :type upper_bound: float, optional
        :returns: The normalized frequency ratio.
        :rtype: float
        """
        new_center = (upper_bound + lower_bound) / 2
        amplitude = (upper_bound - lower_bound) / 2

        if self.max_sum_frequency == 0:
            return 0

        raw_ratio = self.sum_frequencies() / (self.max_sum_frequency )#* Controller.N_REPEAT)
        normalized_ratio = raw_ratio * amplitude
        centered_ratio = normalized_ratio + new_center
    
        return centered_ratio

    def convert_to_motion(self, motor):
        """
        Converts the frequency ratio to a motion value for a specified motor.

        :param motor: The motor for which the motion value is to be calculated.
        :type motor: int
        :returns: The calculated motion value.
        :rtype: float
        """
        ratio = self.frequency_ratio()
        return self.motions[motor][0] * ratio - self.motions[motor][1]  

    def is_firing(self, index):
        """
        Checks if a specific neuron is firing.

        :param index: The index of the neuron in the watch list.
        :type index: int
        :returns: True if the neuron is firing, False otherwise.
        :rtype: bool
        """
        return abs(self.frequency[index]) > 0

    def neurons_fire_string(self):
        """
        Generates a string representation of the firing status of all monitored neurons.

        :returns: A string where each character represents the firing status of a neuron ('1' for firing, '0' for not firing).
        :rtype: str
        """
        s = ""
        for i in range(len(self.watch_neurons)):
            if self.is_firing(i):
                s += "1"
            else:
                s += "0"
        return s
