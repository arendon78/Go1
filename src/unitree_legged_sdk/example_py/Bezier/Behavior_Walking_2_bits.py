import numpy as np
from Neuroscience.structures.Counter_1_bit import Counter_1_bit
from Neuroscience.structures.Activity_Detector import Activity_Detector

class Behavior_Walking_2_bits:
    """
    A class to simulate the walking behavior of a robot using a simple 2-bit finite state machine.

    The `Behavior_Walking_2_bits` class manages a set of neural network counters and activity detectors to 
    simulate walking behavior. The walking pattern is controlled by sensory inputs and the state of the 
    system, which determines the next movement command.


    Attributes
    ----------
    sensor_stack : list of str
        A stack to store sensory information, starting with "FL foot detected".
    
    counters : list of Counter_1_bit
        A list of 1-bit counters used in the simulation.
    
    sim_index : list of int
        A list of simulation indices, initialized to 0 for each counter.
    
    inputs : list of numpy.ndarray
        A list of input arrays for each counter, generated by `build_inputs`.
    
    V : list of list of numpy.ndarray
        A list of voltage matrices for each counter, generated by `build_V`.
    
    ready_for_command : bool
        A flag indicating whether the system is ready to receive a new command, initialized to True.
    
    acts : list of Activity_Detector
        A list of activity detectors associated with each counter.
    
    trajectories : dict
        A dictionary containing the movement trajectories for each part of the robot.
    """

    res = 0.1
    parts = ["FR", "FL", "RR", "RL"]
    MAX_SIM_TIME = 40000

    def __init__(self, trajectories):
        """
        Initializes the Behavior_Walking_2_bits class with the provided trajectories.

        :param trajectories: A dictionary containing the movement trajectories for each part of the robot.
        :type trajectories: dict
        """
        self.sensor_stack = ["FL foot detected"]
        self.counters = [Counter_1_bit(self.res)]
        self.sim_index = [0 for _ in range(len(self.counters))]
        self.inputs = self.build_inputs()
        self.V = self.build_V()
        self.ready_for_command = True
        self.acts = [Activity_Detector(counter.output_neurons) for counter in self.counters]
        self.trajectories = trajectories

    def initial_read_states(self):
        """
        Placeholder for reading initial states of the system.
        """
        None

    def read_states(self):
        """
        Placeholder for reading the current states of the system.
        """
        None

    def build_inputs(self):
        """
        Builds the input arrays for each counter over the maximum simulation time.

        :returns: A list of input arrays for each counter.
        :rtype: list of numpy.ndarray
        """
        l = []  
        sim_time = self.MAX_SIM_TIME
        for _ in range(len(self.counters)):
            inputs = np.zeros([sim_time, 2])
            inputs[0] = [0, 1]
            for i in range(sim_time): 
                if i % 1000 == 700 or i % 1000 == 810: 
                    inputs[i] = [1, 0]
            l.append(inputs)
        return l

    def build_V(self):
        """
        Builds the voltage matrices for each counter over the maximum simulation time.

        :returns: A list of voltage matrices for each counter.
        :rtype: list of list of numpy.ndarray
        """
        l = []
        for i in range(len(self.counters)):
            V = []
            for j in range(len(self.counters[i].brain)):
                sim_time = self.MAX_SIM_TIME
                V.insert(j, np.zeros([sim_time, 2]))
            l.append(V)
        return l

    def get_next_state(self, instruction):
        """
        Advances the state of the counters based on the given instruction.

        :param instruction: A list of instructions for each counter; 1 to increment, 0 to do nothing.
        :type instruction: list of int
        """
        for i in range(len(instruction)):
            if instruction[i] == 1:
                counter = self.counters[i]
                act = self.acts[i]
                previous_bitcode = act.get_activity()
                V = self.V[i]
                k = self.sim_index[i]
                initial_k = k
                inputs = self.inputs[i]

                while k < initial_k + 3000 and k < 40000:
                    counter.pass_inputs(inputs, k)
                    counter.simulate(k, V)
                    act.update_activity()
                    bitcode = act.get_activity()
                    if bitcode != previous_bitcode:
                        if int(bitcode, 2) == (int(previous_bitcode, 2) + 1) % 2:
                            previous_bitcode = bitcode
                            break
                    k += 1

                self.sim_index[i] = k

                if k >= 40000:
                    print("The current counter reached its limit!")
                
                if k == initial_k + 3000:
                    print("The neural network simulated for too long! Not normal...")
            elif instruction[i] == 0:
                None
            else:
                print("Bad value of instruction. The counter can only be incremented by one. Value of the instruction:", instruction[i])

    def set_new_command(self):
        """
        Sets a new command based on the sensory input and current state of the system.

        :returns: A dictionary with the trajectories for each part, or an empty list if no command is ready.
        :rtype: dict or list
        """
        if len(self.sensor_stack) != 0 and self.ready_for_command:
            sensory = self.sensor_stack.pop()
            state = [self.acts[j].get_activity() for j in range(len(self.counters))]

            if sensory == "FL foot detected" and state == ["0"]:
                print("State:", state)
                self.get_next_state([1])
                state = [self.acts[j].get_activity() for j in range(len(self.counters))]
                if state == ["1"]:
                    response = {part: self.trajectories[part][:len(self.trajectories[part])//2] for part in self.parts}
                    return response

            elif sensory == "FR foot detected" and state == ["1"]:
                print("State:", state)
                self.get_next_state([1])
                state = [self.acts[j].get_activity() for j in range(len(self.counters))]
                if state == ["0"]:
                    response = {part: self.trajectories[part][len(self.trajectories[part])//2:] for part in self.parts}
                    return response

            elif sensory == "FR foot detected" and state == ["0"]:
                print("Error:", sensory, state)
            elif sensory == "FL foot detected" and state == ["1"]:
                print("Error:", sensory, state)
            else:
                print("Error, undefined state:", sensory, state)
        else:
            return []

    def push(self, sensory_info):
        """
        Pushes new sensory information onto the stack.

        :param sensory_info: The sensory information to push onto the stack.
        :type sensory_info: str
        """
        if len(self.sensor_stack) == 0:
            self.sensor_stack.append(sensory_info)
        else:
            self.sensor_stack[-1] = sensory_info
    
    def set_ready(self, ready):
        """
        Sets the readiness of the system to receive new commands.

        :param ready: True if ready to receive new commands, False otherwise.
        :type ready: bool
        """
        self.ready_for_command = ready
