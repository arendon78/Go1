import numpy as np
import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(project_root)
from Neuroscience.structures.Organ import Organ

# Definition of class Excitatory_Neuron
class Abstract_Neuron(Organ):
    instanciation_counter = 0
    # For this model a tau of 1.0857 ms will be used
    # This means that EPSPs and IPSPs will take approx. 5.4 ms to charge, 5.4 ms to discharge,
    # and it will remain 3 ms in a constant value
#    tau = 2.1714
    tau = 1.0857

    # Membrane potential (initially zero)
    # As inputs arrive, membrane potential will increase and when it excedes 15 mV, the neuron will fire
    membrane_potential = 0

    # Duration of Excitatory Post-Synaptic Potential EPSP (every 15 ms)
    # Including charge (5.4 ms), stable response (3 ms) and discharge (5.4 ms)
    EPSP_time = 150

    # Duration of Inhibitory Post-Synaptic Potential EPSP (every 15 ms)
    # Including charge (5.4 ms), stable response (3 ms) and discharge (5.4 ms)
    IPSP_time = 150

    # Duration of an action potential pulse (5 ms)
    # Refractory period included
    Act_Pot_time = 50

    # Peak voltage during an action potential pulse (mV)
    Act_Pot_volt = 86.9

    # Threshold Voltage (mV) to fire the neuron
    Thres_Act_Pot_volt = 14.9
    
# redundant
    # # Neuron's resolution
    # resolution = 0

    # Perform spatial summation on all dendrites of the neuron
    def spatial_summation(self):

        result = 0
        # Do spatial summation on the neuron's dendrites.
        for i in range(self.num_dendrites):
            # If the dendrite has an PSP active
            if self.active_PSP[i]:
                self.time_dendrites[i] += 1

                # If the input comes from an excitatory dendrite, Call to EPSP function

                if self.temp_inputs[i] == 1:
                    self.volt_dendrites[i] = self.EPSP(i, self.time_dendrites[i]*self.resolution, self.weights[i])
                # If the input comes from an inhibitory dendrite, Call to IPSP function
                elif self.temp_inputs[i] == -1:
                    self.volt_dendrites[i] = self.IPSP(i, self.time_dendrites[i]*self.resolution, self.weights[i])

                # Update potential due to this dendrite
                result += self.volt_dendrites[i]

                # If the active potential threshold has been reached, activate flag
                if self.membrane_potential > self.Thres_Act_Pot_volt:
                    self.active_potential_bool = True
                    self.time_neuron = 0
                    self.reset_PSP()

                # If the PSP is over, then turn active_PSP off
                if (self.time_dendrites[i]*self.resolution) == self.EPSP_time/10:
                    self.active_PSP[i] = False
                    self.volt_dendrites[i] = 0
                    self.time_dendrites[i] = 0
                    self.temp_summation[i] = 0
                    self.temp_inputs[i] = 0

        # Update membrane's potential
        self.membrane_potential = result

        return result
    

    def get_voltage(self):
        return self.volt_dendrites


    def active_potential(self, t):
        # This action potential takes 5 ms in total
        # action potential + refractory period

        # If the active potential is over, then turn active_potential_bool off
        if t == self.Act_Pot_time/10:
            self.active_potential_bool = False

        self.membrane_potential = (np.sin(1.5*t)/(1.5*t)-0.1266)*100

        # If the signal has reached its peak, then turn max_active_potential off
        if self.max_active_potential:
            self.max_active_potential = False

        # If the neuron is at its peak voltage, then send signal to the axon terminals
        if self.membrane_potential > self.Act_Pot_volt:
            self.max_active_potential = True

        return self.membrane_potential

    def EPSP(self, index, t, weight):
        # Excitatory Post-Synaptic Potential
        # These are the pulses that will be added up and if the threshold is reached (15 mV), fire the neuron
        # 5.4 ms to charge, 5.4 ms to discharge, and 3 ms in a constant value

        # Charge curve
        if t < self.EPSP_time/30 + 3: # 5 ms approx of charge + 3 ms of constant value
            value = weight * (1 - np.exp(-(t/self.tau))) + self.temp_summation[index]
        # Discharge curve
        else: # At time = 8 ms from the start of the EPSP, start discharge
            value = weight * np.exp(-((t-7.9)/self.tau))

        return value

    def IPSP(self, index, t, weight):
        # Inhibitory Post-Synaptic Potential
        # These are the pulses that will be added up and if the threshold is reached (15 mV), fire the neuron
        # 5.4 ms to charge, 5.4 ms to discharge, and 3 ms in a constant value

        # Discharge curve
        if t < self.EPSP_time/30 + 3: # 5 ms approx of discharge + 3 ms of constant value
            value = -weight * (1 - np.exp(-(t/self.tau))) + self.temp_summation[index]
        # Charge curve
        else: # At time = 8 ms from the start of the IPSP, start charge
            value = -weight * np.exp(-((t-7.9)/self.tau))

        return value

    def set_weights(self, values):
        # The weight(s) for synapses must be such that the output voltage remains
        # between 0.1 mV and 5 mV
        for i in range(self.num_dendrites):
            self.weights[i] = values[i]

    def reset_PSP(self):
        # Reset all PSP values to False
        for i in range(self.num_dendrites):
            self.active_PSP[i] = False
            self.volt_dendrites[i] = 0
            self.time_dendrites[i] = 0
            self.temp_summation[i] = 0
            self.temp_inputs[i] = 0

    def reset_axon_terminals(self):
        # Turn all axon terminals off
        for i in range(self.num_axon_terminals):
            self.axon_terminals[i][1] = 0

    def present_inputs(self, inputs):
        # Check that there's not an active potential occurring at the moment
        if not self.active_potential_bool:

            # Checks if there is an input at the present time at any of the dendrites of the neuron
            for i in range(len(inputs)):
                # if there's an input present: turn active_PSP on
                # initialize temp_summation array with current values for the dendrites,
                # and reset times for those dendrites with an input
                if inputs[i] == 1 or inputs[i] == -1:
                    self.active_PSP[i] = True

                    self.temp_summation[i] = self.volt_dendrites[i]
                    self.temp_inputs[i] = inputs[i]
                    self.time_dendrites[i] = 0

    def connect_with_neuron(self, target_neuron):
        # Gets the next available index of the inputs variable for the target neuron
        index = target_neuron.assign_input()

        # Adds a new connection to axon_terminals
        if index != -1:
            # print(self.axon_terminals)
            self.axon_terminals.append([target_neuron,index])

    def assign_input(self):
        # Check for an available dendrite(input) to link it with the calling neuron
        for i in range(self.num_dendrites):
            # Return the index if it's available
            if self.taken_inputs[i] == 0:
                self.taken_inputs[i] = 1
                return i

        # This indicates no indexes are available for this neuron
        return -1


    def __init__(self, res, inputs, outputs, name=""):
        super().__init__()
        self.name = str(Abstract_Neuron.instanciation_counter)
        Abstract_Neuron.instanciation_counter +=1
        
        # Initialize number of dendrites (inputs) in the neuron
        self.num_dendrites = inputs

        # Initialize number of axon terminals (outputs) in the neuron
        self.num_axon_terminals = outputs

        # Variable to store incoming inputs from connected neurons
        self.inputs = np.zeros(self.num_dendrites)

        # Variable to check which inputs(dendrites) have already been taken by a connected neuron
        self.taken_inputs = np.zeros(self.num_dendrites)

        # Initialize weights for the synapses at every dendrite
        self.weights = np.zeros(self.num_dendrites)

        # Variable that indicates if the Active Potential threshold has been reached and therefore,
        # an action potential is taking place in the neuron
        self.active_potential_bool = False

        # Variable to keep track of the actual value of voltage in every dendrite
        self.volt_dendrites = np.zeros(self.num_dendrites)

        # Variable to keep track of the voltage for temporal summation
        # In case several EPSPs arrive within a short period of time (one for each dendrite)
        self.temp_summation = np.zeros(self.num_dendrites)

        # Variable to transmit an action potential to all connected neurons through the axon terminal of the neuron
        self.axon_terminals = []

        # Variable to know if the neuron's potential has reached it's maximum
        self.max_active_potential = False

        # Variable that indicates if a Post-Synaptic Potential is taking place at any of the dendrites in the neuron at the moment
        # Initialize active_PSP variable for every dendrite
        self.active_PSP = []
        for i in range(self.num_dendrites):
            self.active_PSP.append(False)

        # This variable keeps track of wether the last input was excitatory or inhibitory so that when temporal
        # summation takes place, the program will know if it should add or substract a potential
        self.temp_inputs = np.zeros(self.num_dendrites)

        # We need to have a time variable for every dendrite because inputs may arrive at different times
        self.time_dendrites = np.zeros(self.num_dendrites)

        # variable to keep track of the action potential time
        self.time_neuron = 0

        # Set resolution
        self.resolution = res

        self.brain = [self]
# End of definition of class Excitatory_Neuron