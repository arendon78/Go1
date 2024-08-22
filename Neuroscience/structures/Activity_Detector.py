

import numpy as np
import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(project_root)

from Neuroscience.structures.Excitatory_Neuron import Excitatory_Neuron
from Neuroscience.structures.Inhibitory_Neuron import Inhibitory_Neuron
from Neuroscience.structures.Abstract_Neuron import Abstract_Neuron


class  Activity_Detector:

    DELAY = 800

    def __init__(self,watch_neurons):
        self.name = "Activity Detector"
        self.watch_neurons = watch_neurons
        self.len = len(self.watch_neurons)
        assert self.len!=0

        self.inactive_timeout = [-1 for _ in range(self.len)] 
        self.active_timeout = [-1 for _ in range(self.len)] 
        self.active_neurons = ["0" for _ in range(self.len)]


    def update_activity(self): 
        for i in range(self.len): 
        
            curr_neur = self.watch_neurons[i]
            pot = curr_neur.membrane_potential

            if self.inactive_timeout[i] == 0: #if it's zero then the neuron is put as inactive
                self.active_neurons[i] = "0"
                self.inactive_timeout[i] = -1

            if self.active_timeout[i] == 0:  
                self.active_neurons[i] = "1"
                self.active_timeout[i]= -1


            if self.inactive_timeout[i]  > 0 :   
                self.inactive_timeout[i] -= 1

            if self.active_timeout[i] > 0:  
                self.active_timeout[i] -=  1
            
            if pot > Abstract_Neuron.Act_Pot_volt  : 
                if self.active_timeout[i] == -1:
                    self.active_timeout[i] = Activity_Detector.DELAY
                self.inactive_timeout[i] = Activity_Detector.DELAY

            if pot <= Abstract_Neuron.Act_Pot_volt:
                if self.inactive_timeout [i] ==-1 :
                    self.inactive_timeout[i] = Activity_Detector.DELAY

    def print_activity(self) : 
        return ''.join(self.active_neurons)
    
    def get_activity(self) : 
        return  ''.join(self.active_neurons)
            

# neuron.membrane_potential