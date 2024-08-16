

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

#new version -------------------

    def __init__(self, res, list_neurons=[], controller=None,delta_t = 700, spike_detector = False ):
        self.previous_to_watch = []
        if controller:
            self.watch_neurons = [oscillator.output_neuron [ oscillator.to_watch ] for oscillator in controller.oscillators]
            self.to_watch = [ oscillator.to_watch for oscillator in controller.oscillators ]
            self.len = len(self.watch_neurons)
        else:
            self.watch_neurons = list_neurons
            self.len = len(self.watch_neurons)
            self.clock = [-1 for _ in range(self.len)]
        self.spike_detector = spike_detector

        # self.internal_time = 0
        self.resolution = res
        self.timestamps = np.zeros((self.len, 2)) - 1  # initialise timestamps to -1
        self.frequency = np.zeros(self.len)
        self.max_sum_frequency = self.max_frequency * self.len
        self.delta_t = delta_t
        self.controller = controller
        self.time = 0
        self.timer_active = False

    def new_init_(self, controller, new_to_watch):
        self.watch_neurons = [oscillator.output_neuron [ oscillator.to_watch ] for oscillator in controller.oscillators]
        self.to_watch = new_to_watch
        self.len = len(self.watch_neurons)
        self.timestamps = np.zeros((self.len, 2)) - 1  # reinitialise timestamps to -1
        self.frequency = np.zeros(self.len)


    #main method
    def update_firing_rate(self,k):
        for f in self.frequency :
            if f == 1 :
                print("\n\n\n  ERROR ! frequency of 1000  !\n\n\n")

        if self.controller: 
            new_to_watch = [oscillator.to_watch for oscillator in self.controller.oscillators]
            if new_to_watch != self.to_watch :
                # print("changing ! ",new_to_watch,self.to_watch)
                self.new_init_(self.controller,new_to_watch)


        for i in range(self.len) :
            cur_neur = self.watch_neurons[i]

            # if self.clock[i] > 0:
                # self.clock[i]-=1
            if abs(self.timestamps[i, 0] - k) > self.delta_t :
                self.frequency[i] = 0
                # self.clock[i]= -1 
                #warning : if a signals lasts less than 
            if cur_neur.max_active_potential == True :
                self.timestamps[i] = np.roll(self.timestamps[i], 1)
                self.timestamps[i, 0] = k
                
                if self.spike_detector :
                    if self.clock[i] == -1 : #first time he sees a spike, He starts the clock
                        self.clock[i] = self.delta_t
                    elif self.clock[i] == 0 :#once the clock is over, immediatly calculate frequency. This allows to have a constant offset between the detection phase and the no detection phase.
                        self.calculate_frequency(i)
                    else : 
                        None


                else :          
                    self.calculate_frequency(i)


    def calculate_frequency(self, index):
     valid_timestamps = self.timestamps[index][self.timestamps[index] > 0]
     if len(valid_timestamps) > 1:
         intervals = np.diff(valid_timestamps)
         avg_interval = np.mean(intervals)
         if isinstance(self.watch_neurons[index], Inhibitory_Neuron):
             self.frequency[index] = -1 / avg_interval
         elif isinstance(self.watch_neurons[index], Excitatory_Neuron):
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
            sum_freq += el*1000
        return sum_freq


    def frequency_ratio(self, lower_bound=-2, upper_bound=2):
        new_center = (upper_bound + lower_bound)/2
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