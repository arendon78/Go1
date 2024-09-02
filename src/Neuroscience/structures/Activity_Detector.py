

import numpy as np
import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(project_root)

from Neuroscience.structures.Excitatory_Neuron import Excitatory_Neuron
from Neuroscience.structures.Inhibitory_Neuron import Inhibitory_Neuron
from Neuroscience.structures.Abstract_Neuron import Abstract_Neuron


class  Activity_Detector:
    """
    A class that monitors and detects the activity of neurons in a neural network.

    The `Activity_Detector` class keeps track of the membrane potential of a set of neurons and records 
    whether each neuron is active or inactive. It uses timeouts to determine the activity state based on 
    the neuron's potential compared to the action potential threshold.

    The important property of the Activity Detector compared to the Frequency Detector is that it notices     
    activity with a constant offset of [DELAY] thus the period of activity and inactivity remains the same as originally. On the other hand,     
    the Frequency detector notices the frequence as soon as it noticed two spikes and the frequence comes back to 0 once [DELAY] has passed.  

    Attributes
    -----------
    
    name : str
        The name of the activity detector, initialized as "Activity Detector".
      
    watch_neurons : list of Abstract_Neuron
        The list of neurons being monitored by the activity detector.
     
    len : int
        The number of neurons being monitored.
    
    inactive_timeout : list of int
        A list that tracks the inactive timeout for each neuron. Initialized to -1.
    
    active_timeout : list of int
        A list that tracks the active timeout for each neuron. Initialized to -1.
    
    active_neurons : list of str
        A list that records the activity state ("0" for inactive, "1" for active) of each neuron.
    """

    DELAY = 800
    """
    The delay period (in simulation steps) used to determine the transition between active and inactive states.
    
    .
    """

    def __init__(self,watch_neurons):
        """
        Initializes the Activity_Detector instance with a list of neurons to monitor.

        :param watch_neurons: The list of neurons to be monitored for activity.
        :type watch_neurons: list of Abstract_Neuron

        :raises AssertionError: If the list of watch_neurons is empty.

        .
        """
        self.name = "Activity Detector"
        self.watch_neurons = watch_neurons
        self.len = len(self.watch_neurons)
        assert self.len!=0

        self.inactive_timeout = [-1 for _ in range(self.len)] 
        self.active_timeout = [-1 for _ in range(self.len)] 
        self.active_neurons = ["0" for _ in range(self.len)]


    def update_activity(self):
        """
        Updates the activity status of the monitored neurons.

        This method checks each neuron s membrane potential and updates its activity state based on the action 
        potential threshold. The state is updated using timeouts to manage transitions between active and 
        inactive states.

        .
        """ 
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
        """
        Returns the current activity status of the monitored neurons as a string.

        :returns: A string representing the activity status of each neuron ("0" for inactive, "1" for active).
        :rtype: str

        .
        """
        return ''.join(self.active_neurons)
    
    def get_activity(self) : 
        """
        Gets the current activity status of the monitored neurons.

        :returns: A string representing the activity status of each neuron ("0" for inactive, "1" for active).
        :rtype: str

        .
        """
        return  ''.join(self.active_neurons)
            

# neuron.membrane_potential