import numpy as np

#you havee to retrieve the trajectory of a foot in radian in a certain way
from Neuroscience.structures.Counter_1_bit import Counter_1_bit
from Neuroscience.structures.Activity_Detector import Activity_Detector


class Behavior_Walking_2_bits(): 
    """

    this class is made in a generic way, so that it can be easily generalized to handle more complex scenarios.
    So you can choose to factorize it by defining a super class, or keep it as it is if you don't want to explore instructions based on sensory inputs
    and finite state machines approach. (machines à états finis)
    However, it is not too general, because it would require time and make its understanding more difficult.

    """
    

    res = 0.1
    parts = ["FR", "FL", "RR", "RL"]
    MAX_SIM_TIME = 40000

    def __init__(self,trajectories):
        self.sensor_stack = ["FL foot detected"] #  sensory infromation stack. to generalize it, you need to do a list of stacks, each stack is a channel of sensory information
        self.counters = [Counter_1_bit(self.res)] # to generalize it, add more counters
        self.sim_index = [0 for _ in range(len(self.counters))]
        self.inputs = self.build_inputs()
        self.V = self.build_V()
        self.ready_for_command = True

        self.acts = [Activity_Detector(counter.output_neurons) for counter in self.counters]
        self.trajectories = trajectories # can be replaced by a set of movements, that you combine as you like.
                                         #Here we just have the complete trajectory of a 2-step walking gate cycle. (each pair of limb does 1 step)

    def initial_read_states() : 
        None

    def read_states():
        None

    def build_inputs(self) : 
        l = []  
        sim_time = self.MAX_SIM_TIME# default because after that, the counter just starts being incoherent (this means you can do at most 20 steps)
        for _ in range(len(self.counters)):
            inputs = np.zeros([sim_time, 2])  # Initialize inputs (inputs are always the same for every kind of counter)
            inputs[0] = [0,1]
            for i in range(sim_time): 
                if i % 1000 == 700 or i % 1000 == 810: 
                        inputs[i] = [1, 0]
            l.append(inputs)
        return l

    def build_V(self) : 
        l = []
        for i in range(len(self.counters)) : 
            V = []
            for j in range(len(self.counters[i].brain)): 
                sim_time = self.MAX_SIM_TIME
                V.insert(j, np.zeros([sim_time,1]))
            l.append(V)
        return l # l[0] is the entire activity of the first neural network. 
                 #l[0][0] is the activity of the first neuron of the first neural network over the sim_time period.

    def get_next_state(self, instruction): 
        for i in range (len(instruction)):
            if  instruction[i] == 1 : # go to the (n+1)%(2^N) bit
                counter = self.counters[i]
                act = self.acts[i]
                previous_bitcode = self.acts[i].get_activity()
                V = self.V[i]
                k = self.sim_index[i]
                initial_k = k
                inputs = self.inputs[i]
                
                
                while k < initial_k +3000 and k < 40000 : # do not simulate for too long (for a one bit counter the typical delay between 2 bits is 1000 steps)
                        
                        counter.pass_inputs(inputs, k)
                        counter.simulate(k, V)

                        act.update_activity()
                        bitcode = act.get_activity()
                        if bitcode != previous_bitcode:
                            if int(bitcode, 2) == (int(previous_bitcode, 2) + 1) % 2: # prevents artifacts of the counter 
                                previous_bitcode = bitcode
                                break
                        k +=1

                self.sim_index[i] = k

                if k >= 40000 : 
                    print(" the current counter reached its limit ! ")
                
                if k == initial_k + 3000 : 
                    print("the neural netwrok simulated for too long ! not normal...")
            elif instruction == 0 : 
                None
            else : 
                print("Bad value of instruction. The counter can only be incremented by one. Value of the instrction : ", instruction[i])
            if instruction[i] == 0 : 
                None
        


    def set_new_command(self) :
        if len(self.sensor_stack) != 0 and self.ready_for_command :
            sensory = self.sensor_stack.pop() # retrieve the last sensory information

            state = [self.acts[j].get_activity() for j in range (len(self.counters))] # retrieve the state of the system

            if sensory == "FL foot detected" and  state == ["0"]:  #routes the behavior based on the sensory infos and the actual state it is in
                print("etat : ", state)
                self.get_next_state([1]) # if you have multiple counters, you can chose which counter you increment
                state = [self.acts[j].get_activity() for j in range (len(self.counters))]
                if state == ["1"]:# verifies that the state has been updated 
                    response = {part : 
                                        self.trajectories[part][ : len(self.trajectories[part])//2] 
                                for part in self.parts
                                }
                    return response # send commands for performing a right foot

            elif sensory == "FR foot detected" and state == ["1"]: 
                print("etat : ", state)
                self.get_next_state([1])
                state = [self.acts[j].get_activity() for j in range (len(self.counters))]
                if state == ["0"]:
                    response = {part : 
                                        self.trajectories[part][ len(self.trajectories[part])//2 : ] 
                                for part in self.parts
                                }
                    return response #left foot  

            elif sensory == "FR foot detected" and  state == ["0"] :  # error case
                print("error : ",sensory, state)
            elif sensory == "FL foot detected" and  state == ["1"]: #error case
                print("error : ",sensory, state)
            else : 
                print("error, undefined state : ",sensory, state)
        else : 
            return []


    def push(self,sensory_info) : 
        if len(self.sensor_stack) == 0 : 
            self.sensor_stack.append(sensory_info)
        else : 
            self.sensor_stack[-1] = sensory_info
    
    def set_ready(self,bool): 
        self.ready_for_command = bool

    
    
