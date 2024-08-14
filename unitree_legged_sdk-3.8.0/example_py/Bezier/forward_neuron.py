#!/usr/bin/python
import os 
import sys
import time
import math
import numpy as np
import matplotlib.pyplot as plt

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))
sys.path.append(project_root)

from utils import *
from foot_trajectory import *
from computation_neuron import *
from error_calculation import *
from plot_neurons import *
from main_loop import *





from Neuroscience.structures.Controller import Controller
from Neuroscience.structures.Frequency_Detector import Frequency_Detector


sys.path.append('../../lib/python/amd64')
import robot_interface as sdk


N_REPEAT = Controller.N_REPEAT 

if __name__ == '__main__':

    parts = ['FR','FL','RR','RL'] 
    # generation of the foot trajectory 

    NUM_POINTS_BEZIER = 50
    NUM_POINTS_STANCE = 50

    trajectory = foot_trajectory(NUM_POINTS_BEZIER, NUM_POINTS_STANCE)

    #----------------


    # generation of the stand up and lie down trajectory (not computed with neurons)
    stand_up_2 = {'FR' : [0, theta_thigh(0,trajectory[0][0],trajectory[0][1]), theta_calf(0,trajectory[0][0],trajectory[0][1])] , 
                  'FL' : [0, theta_thigh(0,trajectory[0][0],trajectory[0][1]), theta_calf(0,trajectory[0][0],trajectory[0][1])] ,
                  'RR' : [0, theta_thigh(0,trajectory[0][0],trajectory[0][1]), theta_calf(0,trajectory[0][0],trajectory[0][1])] , 
                  'RL' : [0, theta_thigh(0,trajectory[0][0],trajectory[0][1]), theta_calf(0,trajectory[0][0],trajectory[0][1])] 
                  }
    # a little bit dumb but stays as it is for the moment
    stand_up_1 = stand_up_2
    stand_up_3 = stand_up_2


    #------------------------------------

    #Phase shifting of the trajectory of different members so that they move in a coordinated
    # manner thus generating a gate

    offset_cycle_FR = 0
    offset_cycle_FL = 1
    offset_cycle_RR = 1
    offset_cycle_RL = 0
    TOTAL_OFFSET = 1

    FR_trajectory = unphase(0,trajectory)
    FL_trajectory = unphase(0,trajectory)
    RR_trajectory = unphase(0,trajectory)
    RL_trajectory = unphase(0,trajectory)

    trajectories = {'FR': [trajectory[0]]* len(trajectory) * offset_cycle_FR +  FR_trajectory + [trajectory[0]]* len(trajectory) * (TOTAL_OFFSET - offset_cycle_FR ) ,
                    'FL': [trajectory[0]]* len(trajectory) * offset_cycle_FL +  FL_trajectory + [trajectory[0]]* len(trajectory) * (TOTAL_OFFSET - offset_cycle_FL ),
                    'RR': [trajectory[0]]* len(trajectory) * offset_cycle_RR +  RR_trajectory + [trajectory[0]]* len(trajectory) * (TOTAL_OFFSET - offset_cycle_RR ),
                    'RL': [trajectory[0]]* len(trajectory) * offset_cycle_RL +  RL_trajectory + [trajectory[0]]* len(trajectory) * (TOTAL_OFFSET - offset_cycle_RL )
                    }
    

        # FR hip :  -0.3161579668521881
        # FR tihgh :  1.208921194076538
        # FR calf :  -2.7958271503448486
        # FL hip :  0.30471307039260864
        # FL tihgh :  1.2391986846923828
        # FL calf :  -2.8132669925689697
        # RR hip :  -0.3770763576030731
        # RR tihgh :  1.22036612033844
        # RR calf :  -2.797118902206421
        # RL hip :  0.35830429196357727
        # RL tihgh :  1.224181056022644
        # RL calf :  -2.787914514541626
    #-----------------------


    #building the neuron network ------------------------

    res = 0.1

    controllers = { part : [Controller(res),
                            Controller(res),
                            Controller(res)]
                    for part in parts }
    
    # associates a controller to each articulation
    [[controllers[part][i].create_oscillators(0.25) for part in parts ] for i in range(3) ]

    #mock V
    V = [[np.zeros([(20000),1])] for _ in range (16) ]

    #associates a frequency detector to each articulation
    watchers = { part : [Frequency_Detector(res ,controller = controllers[part][0]),
                         Frequency_Detector(res ,controller = controllers[part][1]),
                         Frequency_Detector(res ,controller = controllers[part][2])] 
                for part in parts }

    #simulates the neurons on the trajectory
    compute_simulation = False


    if (compute_simulation):
        neurons_coords, command_coords, frequency_parts, command, inside_oscillator = compute_neurons(trajectories, controllers, watchers,V)

        #saves the neurons coords array so that you can lauch exeperiments wihtout always make the whole simulation again and again
        json_path = "data/neurons_coords.json"
        with open(json_path,"w") as json_file: 
            json.dump(neurons_coords,json_file) 

        #plot the coords from neurons : 
        plot_everything(neurons_coords, command_coords, frequency_parts, command, inside_oscillator)

        #compute error
        print("\n\n -------- compute error ---------- \n\n")

        oscillator1_data = np.array(inside_oscillator['FR'][1])
        freq_command1 = np.array(command['FR'][1])

        maximum_error, result_MAE, result_MSE, relative_MAE  = error(oscillator1_data,freq_command1)

        print("maximum error : ",maximum_error)
        print("MAE : ", result_MAE)
        print("MSE : ", result_MSE)
        print("relative MAE (percentage) : ", str(relative_MAE*100)[:5], "%")
        input("To begin the walking gait, press enter")

    #----------------------------------------------
    print("\n\n -------- main loop ---------- \n\n")

    ## main loop
    distance = 0
    #uses the last saved neuron coords array
    if not compute_simulation : 
        json_path = "data/neurons_coords.json"
        with open(json_path,"r") as json_file: 
            neurons_coords = json.load(json_file) 


    main_loop(trajectories,trajectory,TOTAL_OFFSET,neurons_coords,parts,stand_up_1,stand_up_2,stand_up_3)



