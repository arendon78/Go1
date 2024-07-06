

import numpy as np
import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(project_root)

from Neuroscience.structures.Excitatory_Neuron import Excitatory_Neuron
from Neuroscience.structures.Inhibitory_Neuron import Inhibitory_Neuron

class Frequency_Detector : 
    SOULDER_EXTENSION = 0
    SHOULDER_ABDUCTION = 1
    ELBOW = 2


    range0 = 1.8
    offset0 = 0.5

    range1=4.7
    offset1 = 0.7

    range2=2.3
    offset2= 3.0

    motions = [(range0,offset0), (range1,offset1),(range2,offset2)]

    max_frequency = 9.00900900900901


# --------------------old version
    # def __init__(self, res, list_neurons = [], controller = None, ):
    #     if controller :
    #         self.watch_neurons = [neur.brain[2] for neur in controller.oscillators]
    #         self.len = len(self.watch_neurons)
    #     else : 
    #         self.watch_neurons = list_neurons
    #         self.len = len(self.watch_neurons)

    #     self.internal_time = 0
    #     self.resolution = res
    #     self.timestamp = [-1]*self.len
    #     self.frequency = [0]*self.len
    #     self.max_sum_frequency = self.max_frequency*self.len
    #     self.delta_t = 330
    #     self.controller = controller

    # def new_init_(self,controller):
    #     self.watch_neurons = [neur.brain[2] for neur in controller.oscillators]
    #     self.len = len(self.watch_neurons)
    #     self.internal_time = 0
    #     self.timestamp = [-1]*self.len
    #     self.controller = controller
    
        
    # def update_firing_rate(self):
    #     if self.controller : 
    #         if self.controller.get_changed_instance() : #tells whether the instances inside the controller changed or not 
    #             self.new_init_(self.controller)
    #             self.controller.set_changed_instance(False)# sets changed instance to false

    #     self.internal_time +=1
    #     for i in range(self.len):
    #         cur_neur = self.watch_neurons[i]
    #         if cur_neur.max_active_potential:
    #             if self.timestamp[i] == -1 : 
    #                 self.timestamp[i] = self.internal_time
    #             else : 
    #                 # print(len(self.frequency))
    #                 # print(self.frequency[0])
    #                 # print(self.timestamp[0])
    #                 if isinstance(cur_neur, Inhibitory_Neuron):
    #                     self.frequency[i] = -1 / ((self.internal_time-self.timestamp[i]))
    #                 if isinstance(cur_neur, Excitatory_Neuron):
    #                     self.frequency[i] = 1 / ((self.internal_time-self.timestamp[i]))
    #                 self.timestamp[i] = self.internal_time
    #         # if (self.internal_time-self.timestamp[i]) > self.delta_t :
    #             # self.frequency[i] = 0

#new version -------------------

    def __init__(self, res, list_neurons=[], controller=None):
        if controller:
            self.watch_neurons = [neur.brain[2] for neur in controller.oscillators]
            self.len = len(self.watch_neurons)
        else:
            self.watch_neurons = list_neurons
            self.len = len(self.watch_neurons)

        # self.internal_time = 0
        self.resolution = res
        self.timestamps = np.zeros((self.len, 100)) - 1  # initialise timestamps to -1
        self.frequency = np.zeros(self.len)
        self.max_sum_frequency = self.max_frequency * self.len
        self.delta_t = 700
        self.controller = controller
        self.time = 0
        self.timer_active = False

    def new_init_(self, controller):
        self.watch_neurons = [neur.brain[2] for neur in controller.oscillators]
        self.len = len(self.watch_neurons)
        # self.internal_time = 0
        self.timestamps = np.zeros((self.len, 100)) - 1  # reinitialise timestamps to -1
        self.controller = controller

    def update_firing_rate(self,k):

        for f in self.frequency : 
            if f == 1 : 
                print("\n\n\n  ERROR ! frequency of 1000  !\n\n\n")
        if self.controller: 
            if self.controller.get_changed_instance():
                print(" updated ! ",k)
                self.new_init_(self.controller)
                self.controller.set_changed_instance(False)

        # self.internal_time += 1
        for i in range(self.len):
            cur_neur = self.watch_neurons[i]
            if abs(self.timestamps[i, -1] - k) > self.delta_t:
                self.frequency[i] = 0
            if cur_neur.max_active_potential == True:
                # print("internal time : " ,self.internal_time)
                self.timestamps[i] = np.roll(self.timestamps[i], -1)
                # self.timestamps[i, -1] = self.internal_time
                self.timestamps[i, -1] = k
                self.calculate_frequency(i)

    # def set_timer(self,time): 
    #     if self.time == 0 and self.timer_active: 
    #         self.timer_active = False
    #         return True
        
    #     if self.time == 0 and  not self.timer_active: 
    #         self.timer_active = True 
    #         self.time = time - 1
    #         return False


    #     if self.time > 0 and self.timer_active: 
    #         self.time -=1
    #         return False
        


    def calculate_frequency(self, index):
     valid_timestamps = self.timestamps[index][self.timestamps[index] > 0]
     if len(valid_timestamps) > 1:
         intervals = np.diff(valid_timestamps)
         avg_interval = np.mean(intervals)
         if isinstance(self.watch_neurons[index], Inhibitory_Neuron):
             self.frequency[index] = -1 / avg_interval
         elif isinstance(self.watch_neurons[index], Excitatory_Neuron):
            #  print("average : ",avg_interval)
             self.frequency[index] = 1 / avg_interval

# --------------------------


    def get_freq(self,index):
        return self.frequency[index]*1000
    
    def print_frequency(self):
        [print(self.get_freq(i)) for i in range(self.len)]
        print("\n\n")

    def sum_frequencies (self):
        sum_freq =0
        for (el,neur) in zip (self.frequency,self.watch_neurons):
            # print(el)
            sum_freq += el*1000
        return sum_freq

    # def frequency_ratio(self):
    #     if self.max_sum_frequency == 0:
    #         return 0
    #     print(self.sum_frequencies())
    #     print(self.max_sum_frequency)
    #     return (self.sum_frequencies() / (self.max_sum_frequency)*0.40) # here it is so that the neurons can produce a number between 0 and 4

    def frequency_ratio(self, lower_bound=-2, upper_bound=2):
        new_center = (upper_bound + lower_bound)/2
        # print("new center : ",new_center)
        amplitude = (upper_bound - lower_bound)/2

        if self.max_sum_frequency == 0:
            return 0
        
        # Calculer le ratio brut
        raw_ratio = self.sum_frequencies() / self.max_sum_frequency
        
        
        normalized_ratio = raw_ratio * amplitude
        
        # Centrer autour de `center`
        centered_ratio = normalized_ratio + new_center
        
        return centered_ratio
    
    def convert_to_motion(self,motor):
        #suppose range of movement is the same for everyone.
        #simple routing
        ratio = self.frequency_ratio()
        return self.motions[motor][0]*ratio - self.motions[motor][1]
    

    def is_firing(self, index):
        return abs(self.frequency[index]) > 0 

    def neurons_fire_string(self):
        s = ""
        for i in range (len(self.watch_neurons)) : 
            if (self.is_firing(i)): 
                s+= "1"
            else: 
                s+="0"
        return s



