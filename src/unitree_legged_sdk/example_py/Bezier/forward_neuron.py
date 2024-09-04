#!/usr/bin/python
import os 
import sys
import numpy as np

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))
sys.path.append(project_root)

from utils import *
from unitree_legged_sdk.example_py.Bezier.foot_trajectory import *
from unitree_legged_sdk.example_py.Bezier.computation_neuron import *
from unitree_legged_sdk.example_py.Bezier.error_calculation import *
from unitree_legged_sdk.example_py.Bezier.plot_neurons import *
from unitree_legged_sdk.example_py.Bezier.main_loop import *
# from unitree_legged_sdk.example_py.Bezier.main_loop_v2 import *

from Neuroscience.structures.Controller import Controller
from Neuroscience.structures.Frequency_Detector import Frequency_Detector

N_REPEAT = Controller.N_REPEAT 

if __name__ == '__main__':

    parts = ['FR','FL','RR','RL'] 
    # Generation of the foot trajectory
    NUM_POINTS_BEZIER = 5
    NUM_POINTS_STANCE = 5

    trajectory = foot_trajectory(NUM_POINTS_BEZIER, NUM_POINTS_STANCE)

    # Generation of the stand up and lie down trajectory (not computed with neurons)
    stand_up_2 = {
        'FR' : [0, theta_thigh(0, trajectory[0][0], trajectory[0][1]), theta_calf(0, trajectory[0][0], trajectory[0][1])], 
        'FL' : [0, theta_thigh(0, trajectory[0][0], trajectory[0][1]), theta_calf(0, trajectory[0][0], trajectory[0][1])],
        'RR' : [0, theta_thigh(0, trajectory[0][0], trajectory[0][1]), theta_calf(0, trajectory[0][0], trajectory[0][1])], 
        'RL' : [0, theta_thigh(0, trajectory[0][0], trajectory[0][1]), theta_calf(0, trajectory[0][0], trajectory[0][1])]
    }

    # Phase shifting of the trajectory of different members so that they move in a coordinated manner, generating a gait
    offset_cycle_FR = 0
    offset_cycle_FL = 1
    offset_cycle_RR = 1
    offset_cycle_RL = 0
    TOTAL_OFFSET = 1

    FR_trajectory = unphase(0, trajectory)
    FL_trajectory = unphase(0, trajectory)
    RR_trajectory = unphase(0, trajectory)
    RL_trajectory = unphase(0, trajectory)

    trajectories = {
        'FR': [trajectory[0]] * len(trajectory) * offset_cycle_FR + FR_trajectory + [trajectory[0]] * len(trajectory) * (TOTAL_OFFSET - offset_cycle_FR),
        'FL': [trajectory[0]] * len(trajectory) * offset_cycle_FL + FL_trajectory + [trajectory[0]] * len(trajectory) * (TOTAL_OFFSET - offset_cycle_FL),
        'RR': [trajectory[0]] * len(trajectory) * offset_cycle_RR + RR_trajectory + [trajectory[0]] * len(trajectory) * (TOTAL_OFFSET - offset_cycle_RR),
        'RL': [trajectory[0]] * len(trajectory) * offset_cycle_RL + RL_trajectory + [trajectory[0]] * len(trajectory) * (TOTAL_OFFSET - offset_cycle_RL)
    }


    # Building the neural network
    res = 0.1

    controllers = {
        part: [Controller(res, use_old_combinations=False),
               Controller(res, use_old_combinations=False),
               Controller(res, use_old_combinations=False)]
        for part in parts
    }

    # Associates a controller to each articulation
    [[controllers[part][i].create_oscillators(0.25) for part in parts] for i in range(3)]

    # Mock V
    V = [[np.zeros([(20000), 1])] for _ in range(16)]

    # Associates a frequency detector to each articulation
    watchers = {
        part: [Frequency_Detector(res, controller=controllers[part][0]),
               Frequency_Detector(res, controller=controllers[part][1]),
               Frequency_Detector(res, controller=controllers[part][2])]
        for part in parts
    }

    # Simulates the neurons on the trajectory
    compute_simulation = True

    if compute_simulation:
        neurons_coords, command_coords, frequency_parts, command, inside_oscillator = compute_neurons(trajectories, controllers, watchers, V)

        # Saves the neurons coords array so that you can launch experiments without always making the whole simulation again
        json_path = "data/neurons_coords.json"
        with open(json_path, "w") as json_file:
            json.dump(neurons_coords, json_file)

        # Plot the coords from neurons
        plot_everything(neurons_coords, command_coords, frequency_parts, command, inside_oscillator)

        # Compute error
        print("\n\n -------- compute error ---------- \n\n")

        oscillator1_data = np.array(inside_oscillator['FR'][1])
        freq_command1 = np.array(command['FR'][1])

        maximum_error, result_MAE, result_MSE, relative_MAE = error(oscillator1_data, freq_command1)

        print("Maximum error:", maximum_error)
        print("MAE:", result_MAE)
        print("MSE:", result_MSE)
        print("Relative MAE (percentage):", str(relative_MAE * 100)[:5], "%")
        input("To begin the walking gait, press enter")

    # Main loop
    print("\n\n -------- main loop ---------- \n\n")

    distance = 0

    # Uses the last saved neuron coords array
    if not compute_simulation:
        json_path = "data/neurons_coords.json"
        with open(json_path, "r") as json_file:
            neurons_coords = json.load(json_file)

    main_loop(trajectories, trajectory, TOTAL_OFFSET, neurons_coords, parts,stand_up_2)
