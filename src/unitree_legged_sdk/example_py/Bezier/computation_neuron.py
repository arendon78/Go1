#!/usr/bin/python
import os 
import sys
import json
import numpy as np

from utils import *
from unitree_legged_sdk.example_py.Bezier.foot_trajectory import *

from Neuroscience.structures.Excitatory_Neuron import Excitatory_Neuron 
from Neuroscience.structures.Controller import Controller
from Neuroscience.structures.Tunable_Oscillator import Tunable_Oscillator


project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))
sys.path.append(project_root)


sys.path.append('../../lib/python/amd64')
# import robot_interface as sdk 

def compute_neurons(trajectories, controllers, watchers, V):
    """
    Computes the neuron activities, commands, and frequencies for a given set of trajectories.

    This function simulates the behavior of neural networks controlling a robot's limbs based on provided
    trajectories. The simulation runs for a specified simulation time and updates the neural activities,
    commands, and frequencies for each limb part.

    Parameters
    ----------
    trajectories : dict
        A dictionary containing the trajectory data for each part of the robot. The keys are 'FR', 'FL',
        'RR', 'RL', and the values are lists of coordinates.
    
    controllers : dict
        A dictionary containing the controllers for each part of the robot. The keys are 'FR', 'FL',
        'RR', 'RL', and the values are lists of three controllers for hip, thigh, and calf.
    
    watchers : dict
        A dictionary containing the watchers for each part of the robot. The keys are 'FR', 'FL',
        'RR', 'RL', and the values are lists of three watchers for hip, thigh, and calf.
    
    V : dict
        A dictionary containing the voltage matrices used in the simulation. It is updated during the
        simulation to reflect the neural activities.

    Returns
    -------
    neurons_coords : dict
        A dictionary containing the coordinates of the neurons' activities for each part of the robot.
        The keys are 'FR', 'FL', 'RR', 'RL', and the values are lists of tuples (hip, thigh, calf) representing
        the frequency ratios of the respective neurons.
    
    command_coords : dict
        A dictionary containing the commanded positions for each part of the robot. The keys are 'FR', 'FL',
        'RR', 'RL', and the values are lists of tuples (hip, thigh, calf) representing the target positions.
    
    frequency_parts : dict
        A dictionary containing the frequency ratios for each part of the robot. The keys are 'FR', 'FL',
        'RR', 'RL', and the values are lists of frequency ratios for the hip, thigh, and calf neurons.
    
    command : dict
        A dictionary containing the commands sent to each part of the robot during the simulation.
        The keys are 'FR', 'FL', 'RR', 'RL', and the values are lists of commands for the hip, thigh, and calf.
    
    inside_oscillator : dict
        A dictionary containing the internal oscillator states for each part of the robot. The keys are 'FR', 'FL',
        'RR', 'RL', and the values are lists of oscillator states for the hip, thigh, and calf.
    """

    SIM_TIME = 700  # Number of time steps for each simulation
    N_STEPS = len(trajectories['FR'])  # Number of steps in the provided trajectory
    parts = ['FR', 'FL', 'RR', 'RL']  # Parts of the robot (Front Right, Front Left, Rear Right, Rear Left)

    # Initialize dictionaries to store neuron coordinates, commands, and frequency data
    neurons_coords = {part: [] for part in parts}
    command_coords = {part: [] for part in parts}
    frequency_parts = {part: [[], [], []] for part in parts}
    command = {part: [[], [], []] for part in parts}
    inside_oscillator = {part: [[], [], []] for part in parts}

    # Update the adjacency matrix for each controller
    for part in parts:
        for n in range(3):
            controllers[part][n].update_adjacency_matrix()

    # Initialize data structure to store simulation data
    data_json = {
        part: {
            n: [controllers[part][n].adjacency, [np.zeros([(SIM_TIME * N_STEPS), 2]) for _ in range(controllers[part][n].adjacency.size)], 
                [1 if isinstance(neuron, Excitatory_Neuron) else 0 for neuron in controllers[part][n].brain]]
            for n in range(3)
        }
        for part in parts
    }

    internal_times = {part: 0 for part in parts}  # Initialize internal simulation time for each part

    # Main computation loop
    for i in range(N_STEPS):
        coords = {part: trajectories[part][i] for part in parts}  # Get the current step's coordinates
        print(i)
        for part in parts:
            x, y, z = coords[part][0], coords[part][1], 0
            hip = theta_hip(x, y, z)
            thigh = theta_thigh(x, y, z)
            calf = theta_calf(x, y, z)

            # Simulate the oscillators and update frequency and command data
            for j, angle in enumerate([hip, thigh, calf]):
                inside_oscillator_state = controllers[part][j].create_oscillators(angle)[0]
                if i == 0:
                    controllers[part][j].pass_inputs(1)
                else:
                    controllers[part][j].pass_inputs(0)
                controllers[part][j].simulate(internal_times[part], data_json[part][j][1])
                frequency_parts[part][j].append(watchers[part][j].frequency_ratio())
                command[part][j].append(angle)
                inside_oscillator[part][j].append(inside_oscillator_state)

            internal_times[part] += 1

            # Additional simulation steps for each neuron
            for j in range(SIM_TIME):
                for k, angle in enumerate([hip, thigh, calf]):
                    watchers[part][k].update_firing_rate(j)
                    controllers[part][k].pass_inputs(0)
                    if j > 0:
                        controllers[part][k].simulate(internal_times[part], data_json[part][k][1])
                    frequency_parts[part][k].append(watchers[part][k].frequency_ratio())
                    command[part][k].append(angle)

                if j > 0:
                    internal_times[part] += 1

            neuron_hip = watchers[part][0].frequency_ratio()
            neuron_thigh = watchers[part][1].frequency_ratio()
            neuron_calf = watchers[part][2].frequency_ratio()

            neurons_coords[part].append((neuron_hip, neuron_thigh, neuron_calf))
            command_coords[part].append((hip, thigh, calf))

    # Ensure consistency across parts of the robot
    assert (frequency_parts['FR'] == frequency_parts['RL'])
    assert (frequency_parts['RR'] == frequency_parts['FL'])

    # Convert numpy arrays to lists for JSON serialization
    for part in parts:
        for n in range(3):
            for i in range(Controller.N_REPEAT * Tunable_Oscillator.len):
                data_json[part][n][1][i] = data_json[part][n][1][i].tolist()
                if i == 0:
                    data_json[part][n][0] = data_json[part][n][0].matrix.tolist()

    json_file_path = 'data/neuron_activity.json'
    with open(json_file_path, 'w') as json_file:
        json.dump(data_json, json_file)

    return neurons_coords, command_coords, frequency_parts, command, inside_oscillator
