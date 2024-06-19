

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

    max_frequency = 90.09009009009007

    def __init__(self,res,list_neurons):
        self.internal_time = 0
        self.resolution = res
        self.watch_neurons = list_neurons
        self.len = len(list_neurons)
        self.timestamp = [-1]*self.len 
        self.frequency = [0]*self.len
        self.max_sum_frequency = self.max_frequency*self.len

    def update_firing_rate(self):
        for i in range(self.len):
            cur_neur = self.watch_neurons[i]
            if cur_neur.max_active_potential:
                if self.timestamp[i] == -1 : 
                    self.timestamp[i] = self.internal_time
                else : 
                    if isinstance(cur_neur, Inhibitory_Neuron):
                        self.frequency[i] = -1 / ((self.internal_time-self.timestamp[i])*self.resolution)
                    if isinstance(cur_neur, Excitatory_Neuron):
                        self.frequency[i] = 1 / ((self.internal_time-self.timestamp[i])*self.resolution)
                    self.timestamp[i] = self.internal_time

        self.internal_time+=1

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
        return self.sum_frequencies() / (self.max_sum_frequency)
    
    def convert_to_motion(self,motor):
        #suppose range of movement is the same for everyone.
        #simple routing
        ratio = self.frequency_ratio()
        return self.motions[motor][0]*ratio - self.motions[motor][1]
