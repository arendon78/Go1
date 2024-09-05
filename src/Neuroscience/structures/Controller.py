import os
import sys
from itertools import product


project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(project_root)

from Neuroscience.structures.Organ import Organ
from Neuroscience.structures.Tunable_Oscillator import Tunable_Oscillator


class Controller(Organ):
    """
    A class that controls and manages the configuration of tunable oscillators within a neural network.

    The `Controller` class is responsible for building frequency combinations, managing oscillators, and
    determining the optimal configuration for neuron activation. It interacts with a set of `Tunable_Oscillator`
    instances to simulate complex neural behaviors.

    Attributes
    ----------
    res : int
        The resolution of the simulation, affecting time steps.
    
    oscillators : list of Tunable_Oscillator
        A list of `Tunable_Oscillator` instances managed by the Controller.

    brain : list of Abstract_Neuron
        A list of neurons extracted from the oscillators to form the Controller's "brain".
    """

    main_list = []
    """
    A class-level list that stores the precomputed frequency combinations used by the Controller.
    """

    frequencies = [
        0,
        3.003003003003003,
        3.6032217041119123,
        4.504504504504505,
        6.005384137502588,
        9.00900900900901
    ]
    """
    A predefined list of frequencies (in spike/thousand steps of simulation) used to configure the oscillators.

    Note: The theoretical minimum interval of convergence is approximately 600 steps.
    """

    N_REPEAT = 4
    """
    The number of oscillators to be used in generating frequency combinations.
    """

    def pass_inputs(self, input):
        """
        Passes input values to all oscillators managed by the Controller.

        :param input: The input value to be applied to the oscillators.
        :type input: float
        """
        for os in self.oscillators:
            os.brain[0].inputs[1] = input

    def find_combination_index(self, ratio):
        """
        Finds the index of the closest frequency combination to a given ratio.

        :param ratio: The target frequency ratio.
        :type ratio: float
        :returns: The index and distance of the closest combination.
        :rtype: tuple(int, float)
        """
        distance =2 
        index = 0
        for i in range(len(Controller.main_list)):
            new_d = abs(ratio - Controller.main_list[i][0])
            if new_d < distance:
                index = i
                distance = new_d
        return index, distance

    def find_combination(self, ratio):
        """
        Finds the best frequency combination and its corresponding ratio for a given target ratio.

        :param ratio: The target frequency ratio.
        :type ratio: float
        :returns: The best combination and its ratio.
        :rtype: tuple(list, float)
        """
        i, d = self.find_combination_index(ratio)
        return Controller.main_list[i][1], Controller.main_list[i][0]

    def build_combinations_raw(self, lower_bound=-2, upper_bound=2):
        """
        Builds raw frequency combinations within a specified range.

        This method generates all possible combinations of frequencies (with repetition) and applies a set 
        of signs to them. The results are then normalized according to the specified bounds.

        :param lower_bound: The lower bound for normalization, defaults to -2.
        :type lower_bound: float, optional
        :param upper_bound: The upper bound for normalization, defaults to 2.
        :type upper_bound: float, optional
        :returns: A list of normalized frequency combinations and their associated triples.
        :rtype: list of tuple(float, tuple)
        """
        new_center = (upper_bound + lower_bound) / 2
        amplitude = (upper_bound - lower_bound) / 2

        numbers = self.frequencies
        comb_of_six_with_repetition = list(product(numbers, repeat=self.N_REPEAT))
        results_with_triples = set()
        sign_combinations = list(product([1, -1], repeat=self.N_REPEAT))

        for combo in comb_of_six_with_repetition:
            for signs in sign_combinations:
                numbers = sum(sign * num for sign, num in zip(signs, combo))
                operation_triple = tuple(sign * num for sign, num in zip(signs, combo))
                results_with_triples.add((numbers, operation_triple))

        sorted_results_with_triples = sorted(results_with_triples)
        max_sum_frequency = self.frequencies[-1] * self.N_REPEAT
        normalized_results_with_triples = []

        for value, triple in sorted_results_with_triples:
            raw_ratio = value / max_sum_frequency
            normalized_ratio = raw_ratio * amplitude
            centered_ratio = normalized_ratio + new_center
            normalized_results_with_triples.append((centered_ratio, triple))

        return normalized_results_with_triples

    def f(e):
        """
        Counts the number of elements in the combination that have the same sign as the command.

        :param e: A tuple containing the ratio and combination.
        :type e: tuple
        :returns: The count of elements with the same sign as the command.
        :rtype: int
        """
        f = e[0]
        c = 0
        for n in e[1]:
            if n * f > 0:
                c += 1
        return c

    def build_combinations(self):
        """
        Reduces the number of elements in the Controller's main list by removing duplicates and selecting 
        elements that maximize a specific function.

        The function `f` is designed to ensure that for negative movements, inhibitory neurons are used 
        predominantly, and excitatory neurons are used for positive movements.

        :returns: A list of optimized frequency combinations.
        :rtype: list
        """
        Controller.main_list = self.build_combinations_raw()

        setA = set()
        for i in range(len(Controller.main_list)):
            setA.add(Controller.main_list[i][0])

        listA = list(setA)
        index_dict = {value: idx for idx, value in enumerate(listA)}

        for i in range(len(listA)):
            listA[i] = [listA[i], 0, 0]

        for i in range(len(Controller.main_list)):
            e = Controller.main_list[i]
            corresp_index = index_dict[e[0]]
            val = Controller.f(e)
            if val >= listA[corresp_index][1]:
                listA[corresp_index][1] = val
                listA[corresp_index][2] = e

        new_l = []
        for i in range(len(listA)):
            new_l.append(listA[i][2])

        set_l = set(new_l)
        print(len(new_l))
        return new_l

    def create_oscillators(self, ratio):
        """
        Creates and configures oscillators based on the given frequency ratio.

        :param ratio: The target frequency ratio for configuring the oscillators.
        :type ratio: float
        :returns: The true value of the ratio and the corresponding frequency combination.
        :rtype: tuple(float, tuple)
        """
        tuple, true_val = self.find_combination(ratio)

        assert len(tuple) == self.N_REPEAT
        i = 0
        for j in tuple:
            if j == 0:
                sign = 1
            else:
                sign = j // abs(j)

            current = self.oscillators[i]

            if abs(j) == self.frequencies[0]:
                current.tune_oscillator([0.015, 0.015], sign)

            if abs(j) == self.frequencies[1]:
                current.tune_oscillator([7.5, 7.5], sign)

            if abs(j) == self.frequencies[2]:
                current.tune_oscillator([7.65, 7.65], sign)

            if abs(j) == self.frequencies[3]:
                current.tune_oscillator([7.8, 7.8], sign)

            if abs(j) == self.frequencies[4]:
                current.tune_oscillator([8.325, 8.325], sign)

            if abs(j) == self.frequencies[5]:
                current.tune_oscillator([10.65, 10.65], sign)

            i += 1

        return true_val, tuple

    def __init__(self, res, use_old_combinations=False):
        """
        Initializes the Controller instance with specified resolution and oscillator configuration.

        :param res: The resolution of the simulation, affecting time steps.
        :type res: int
        :param use_old_combinations: Flag to determine whether to use old frequency combinations, defaults to False.
        :type use_old_combinations: bool, optional
        """
        super().__init__()
        self.name = "Controller"
        self.res = res
        self.oscillators = [Tunable_Oscillator(res=self.res) for i in range(self.N_REPEAT)]
        if Controller.main_list == []:
            if use_old_combinations:
                Controller.main_list = self.build_combinations_raw()
            else:
                Controller.main_list = self.build_combinations()
        self.brain = [neuron for oscillator in self.oscillators for neuron in oscillator.brain]
