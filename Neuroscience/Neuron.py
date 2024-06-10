import matplotlib.pyplot as plt
import numpy as np

# Definition of class Neuron
class Neuron:
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

    # Duration of Inhibitory Post-Synaptic Potential IPSP (every 15 ms)
    # Including charge (5.4 ms), stable response (3 ms) and discharge (5.4 ms)
    IPSP_time = 150

    # Duration of an action potential pulse (5 ms)
    # Refractory period included
    Act_Pot_time = 50

    # Peak voltage during an action potential pulse (mV)
    Act_Pot_volt = 86.9

    # Threshold Voltage (mV) to fire the neuron
    Thres_Act_Pot_volt = 14.9

    # Number of dendrites in the neuron
    num_dendrites = 2

    # Number of axon terminals in the neuron
    num_axon_terminals = 5

    # Weights for the synapses at every dendrite
    weights = []

    # Variable that indicates if the Active Potential threshold has been reached and therefore,
    # an action potential is taking place in the neuron
    active_potential_bool = False

    # Variable that indicates if a Post-Synaptic Potential is taking place at any of the dendrites in the neuron at the moment
    active_PSP = []

    # Variable to keep track of the actual value of voltage in every dendrite
    dendrites = []

    # Variable to transmit an action potential to all connected neurons through the axon terminal of the neuron
    axon_terminals = []

    # Variable to keep track of the voltage for temporal summation
    # In case several EPSPs arrive within a short period of time (one for each dendrite)
    temp_summation = []

    # We need to have a time variable for every dendrite because inputs may arrive at different times
    time_dendrites = []

    # variable to keep track of the action potential time
    time_neuron = 0

    # Neuron's resolution
    resolution = 0

    def active_potential(self, t):
        # This action potential takes 5 ms in total
        # action potential + refractory period

        # If the active potential is over, then turn active_potential_bool off
        if t == self.Act_Pot_time/10:
            self.active_potential_bool = False

        self.membrane_potential = (np.sin(1.5*t)/(1.5*t)-0.1266)*100

        # If the signal has been sent to all axon terminals, then turn them off
        if np.all(self.axon_terminals):
            self.reset_axon_terminals()

        # If the neuron is at its peak voltage, then send signal to the axon terminals
        if self.membrane_potential > self.Act_Pot_volt:
            self.set_axon_terminals()

        return self.membrane_potential

    # Perform spatial summation on all dendrites of the neuron
    def spatial_summation(self):
        result = 0

        # Do spatial summation on the neuron's dendrites.
        for i in range(self.num_dendrites):
            # If the dendrite has an PSP active
            if self.active_PSP[i]:
                self.time_dendrites[i] += 1

                # Call to EPSP function
                self.dendrites[i] = self.EPSP(i, self.time_dendrites[i]*self.resolution, self.weights[i])
                result += self.dendrites[i]

                # If the active potential threshold has been reached, activate flag
                if self.membrane_potential > self.Thres_Act_Pot_volt:
                    self.active_potential_bool = True
                    self.time_neuron = 0
                    self.reset_PSP()

                # If the PSP is over, then turn active_PSP off
                if (self.time_dendrites[i]*self.resolution) == self.EPSP_time/10:
                    self.active_PSP[i] = False
                    self.dendrites[i] = 0
                    self.time_dendrites[i] = 0
                    self.temp_summation[i] = 0

        # Update membrane's potential
        self.membrane_potential = result

        return result

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

    def set_weights(self, values):
        # The weight(s) for synapses must be such that the output voltage remains
        # between 0.1 mV and 5 mV
        for i in range(self.num_dendrites):
            self.weights[i] = values[i]

    def reset_PSP(self):
        # Reset all PSP values to False
        for i in range(self.num_dendrites):
            self.active_PSP[i] = False
            self.dendrites[i] = 0
            self.time_dendrites[i] = 0
            self.temp_summation[i] = 0

    def set_axon_terminals(self):
        # Turn all axon terminals on
        for i in range(self.num_axon_terminals):
            self.axon_terminals[i] = 1

    def reset_axon_terminals(self):
        # Turn all axon terminals off
        for i in range(self.num_axon_terminals):
            self.axon_terminals[i] = 0

    def present_inputs(self, inputs):
        # Check that there's not an active potential occurring at the moment
        if not self.active_potential_bool:

            # Checks if there is an input at the present time at any of the dendrites of the neuron
            for i in range(len(inputs)):
                # if there's an input present: turn active_PSP on
                # initialize temp_summation array with current values for the dendrites,
                # and reset times for those dendrites with an input
                if inputs[i] == 1:
                    self.active_PSP[i] = True

                    self.temp_summation[i] = self.dendrites[i]
                    self.time_dendrites[i] = 0

    def __init__(self, res):
        # Initialize weights
        self.weights = np.zeros(self.num_dendrites)

        # Initialize dendrites
        self.dendrites = np.zeros(self.num_dendrites)

        # Initialize axon terminals
        self.axon_terminals = np.zeros(self.num_axon_terminals)

        # Initialize temporal summation for every dendrite
        self.temp_summation = np.zeros(self.num_dendrites)

        # Initialize active_PSP variable for every dendrite
        for i in range(self.num_dendrites):
            self.active_PSP.append(False)

        # Initialize all time variables for dendrites to zero
        self.time_dendrites = np.zeros(self.num_dendrites)

        # Set resolution
        self.resolution = res

# End of definition of class Neuron
