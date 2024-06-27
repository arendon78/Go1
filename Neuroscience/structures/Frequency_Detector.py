

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

    def __init__(self, res, list_neurons = [], controller = None, ):
        if controller :
            self.watch_neurons = [neur.brain[2] for neur in controller.oscillators]
            self.len = len(self.watch_neurons)
        else : 
            self.watch_neurons = list_neurons
            self.len = len(self.watch_neurons)

        self.internal_time = 0
        self.resolution = res
        self.timestamp = [-1]*self.len
        self.frequency = [0]*self.len
        self.max_sum_frequency = self.max_frequency*self.len
        self.delta_t = 330
        self.controller = controller

    def new_init_(self,controller):
        self.watch_neurons = [neur.brain[2] for neur in controller.oscillators]
        self.len = len(self.watch_neurons)
        self.internal_time = 0
        self.timestamp = [-1]*self.len
        self.controller = controller
    
        
    def update_firing_rate(self):
        if self.controller : 
            if self.controller.get_changed_instance() : #tells whether the instances inside the controller changed or not 
                self.new_init_(self.controller)
                self.controller.set_changed_instance(False)# sets changed instance to false

        self.internal_time +=1
        for i in range(self.len):
            cur_neur = self.watch_neurons[i]
            if cur_neur.max_active_potential:
                if self.timestamp[i] == -1 : 
                    self.timestamp[i] = self.internal_time
                else : 
                    if isinstance(cur_neur, Inhibitory_Neuron):
                        self.frequency[i] = -1 / ((self.internal_time-self.timestamp[i]))
                    if isinstance(cur_neur, Excitatory_Neuron):
                        self.frequency[i] = 1 / ((self.internal_time-self.timestamp[i]))
                    self.timestamp[i] = self.internal_time
            # if (self.internal_time-self.timestamp[i]) > self.delta_t :
                # self.frequency[i] = 0



    def get_freq_hertz(self,index):
        return self.frequency[index]*1000
    
    def print_frequency(self):
        return [self.get_freq_hertz(i) for i in range(self.len)]

    def sum_frequencies (self):
        sum_freq =0
        for (el,neur) in zip (self.frequency,self.watch_neurons):
            # print("el:",el)
            sum_freq += el*1000
        # print(sum_freq)
        return sum_freq

    def frequency_ratio(self):
        if self.max_sum_frequency == 0:
            return 0
        return self.sum_frequencies() / (self.max_sum_frequency)
    
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



